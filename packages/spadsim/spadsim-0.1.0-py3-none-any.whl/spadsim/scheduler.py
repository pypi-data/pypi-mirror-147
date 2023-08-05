"""
The Scheduler class is included to provide a convenient way to run the
Simulator class in parallel.
"""

import dask
from distributed import Client, LocalCluster
import pandas as pd
from spadsim import Simulator


class Scheduler:
    """
    Class to wrap Dask's scheduler and provide a simple interface to run
    simulations in parallel. Also provides a basic summary of the results.
    """

    def __init__(
        self,
        num_workers,
        num_runs_per_worker,
        data_file,
        pgen_file,
        param_file,
        test_suite=False,
        test_coord=None,
        rng_seed=None,
    ):
        """
        Initialise the Scheduler class.

        Parameters
        ----------
        num_workers : int
            Number of workers to use. Should be equal to the number of cores
            available. This is also the number of Simulator classes that will
            be run in parallel.
        num_runs_per_worker : int
            Number of runs for each Simulator. This is the number of times
            the simulation will be run for each Simulator.
        data_file : str
            Path to the data file. See Simulator.__init__ docstring for more
            details.
        pgen_file : str
            Path to the pgen file. See Simulator.__init__ docstring for more
            details.
        param_file : str
            Path to the param file. See Simulator.__init__ docstring for more
            details.
        test_suite : bool, optional
            Whether to run the test suite. See Simulator.__init__ docstring
            for more details. Default is False.
        test_coord : ndarray of shape (2,), optional
            Coordinates of the test point. See Simulator.__init__ docstring
            for more details. Default is None.
        rng_seed : int, optional
            Seed for the random number generator. Note that setting this will
            result in ALL simulators returning the exact same result. Default
            is None.
        """

        if not isinstance(num_workers, int):
            raise TypeError("num_workers must be an integer")
        if isinstance(num_workers, bool):
            raise TypeError("num_workers must be an integer")
        if num_workers < 1:
            raise ValueError("num_workers must be an integer >= 1")
        if not isinstance(num_runs_per_worker, int):
            raise TypeError("num_runs_per_worker must be an integer")
        if isinstance(num_runs_per_worker, bool):
            raise TypeError("num_runs_per_worker must be an integer")
        if num_runs_per_worker < 1:
            raise ValueError("num_runs_per_worker must be an integer >= 1")

        if rng_seed:
            print("PLEASE NOTE THAT SETTING A SEED WILL RESULT IN ALL"
                  "PARALLEL SIMULATORS RETURNING IDENTICAL RESULTS. THIS IS"
                  "ONLY INTENDED AS A DEBUGGING/ TESTING TOOL.")

        self.num_workers = num_workers
        self.num_runs_per_worker = num_runs_per_worker

        self.data_file = data_file
        self.pgen_file = pgen_file
        self.param_file = param_file

        self.test_suite = test_suite
        self.test_coord = test_coord
        self.rng_seed = rng_seed

        cluster = LocalCluster(n_workers=self.num_workers, threads_per_worker=1)
        self.client = Client(cluster)

        self.all_futures = None
        self._all_results = None
        self._results_df = None
        self._exit_df = None
        self._deadspace_df = None
        self._pgen_coords_df = None

        self.__done = False

        port = self.client.scheduler_info()["services"]["dashboard"]
        print(f"\nScheduler GUI:\nhttp://127.0.0.1:{port}/status\n")

    @staticmethod
    @dask.delayed
    def _create_simulator(
        data_file,
        pgen_file,
        param_file,
        test_suite,
        test_coord,
        rng_seed,
    ):
        """
        Delayed function to create a Simulator object.

        Parameters
        ----------
        data_file : str
            Path to the data file. See Simulator.__init__ docstring for more
            details.
        pgen_file : str
            Path to the pgen file. See Simulator.__init__ docstring for more
            details.
        param_file : str
            Path to the param file. See Simulator.__init__ docstring for more
            details.
        test_suite : bool
            Whether to run the test suite. See Simulator.__init__ docstring
            for more details.
        test_coord : ndarray of shape (2,)
            Coordinates of the test point. See Simulator.__init__ docstring
            for more details.
        rng_seed : int
            Seed for the random number generator.

        Returns
        -------
        simulator : dask.delayed.Delayed
            dask.delayed initialised Simulator object.
        """

        return Simulator(
            data_file,
            pgen_file,
            param_file,
            test_suite,
            test_coord,
            rng_seed,
        )

    @staticmethod
    @dask.delayed
    def _run_simulator(_Simulator, num_runs_per_worker):
        """
        Delayed function to lazily run a Simulator object. This does not
        actually run the simulation, but instead returns a dask.delayed object
        that can be run later.

        Parameters
        ----------
        Simulator : dask.delayed.Delayed
            dask.delayed initialised Simulator object.
        num_runs_per_worker : int
            Number of runs for each Simulator. This is the number of times
            the simulation will be run for each Simulator.

        Returns
        -------
        result : dask.delayed.Delayed
            dask.delayed object that returns the result of running the
            simulation the specified number of times.
        """

        return _Simulator.run_sequence(num_runs_per_worker)

    def run_all(self):
        """
        Run all simulations.
        """
        self.__done = False
        results = []
        for _ in range(self.num_workers):
            _Simulator = self._create_simulator(
                self.data_file,
                self.pgen_file,
                self.param_file,
                self.test_suite,
                self.test_coord,
                self.rng_seed,
            )
            results.append(
                self._run_simulator(_Simulator, self.num_runs_per_worker)
            )

        self.all_futures = self.client.compute(results)

    def gather_results(self):
        """
        Gather the results of the simulations.
        """
        self._all_results = self.client.gather(self.all_futures)
        result_list = []
        exit_list = []
        deadspace_list = []
        pgen_coords_list = []

        for result in self._all_results:
            result_list.append(result[0])
            exit_list.append(result[1])
            deadspace_list.append(result[2])
            pgen_coords_list.append(result[3])

        results_df = pd.concat(result_list)
        exit_df = pd.concat(exit_list)
        deadspace_df = pd.concat(deadspace_list)
        pgen_coords_df = pd.concat(pgen_coords_list)

        results_df.reset_index(inplace=True, drop=True)
        exit_df.reset_index(inplace=True, drop=True)
        deadspace_df.reset_index(inplace=True, drop=True)
        pgen_coords_df.reset_index(inplace=True, drop=True)

        self._results_df = results_df
        self._exit_df = exit_df
        self._deadspace_df = deadspace_df
        self._pgen_coords_df = pgen_coords_df

        self.__done = True

    @property
    def num_runs(self):
        """
        Total number of Simulator runs.
        """

        return self.num_workers * self.num_runs_per_worker

    @property
    def pde(self):
        """
        Photon Detection Efficiency in percentage. If the simulation is not
        finished, this will create a blocking call to the gather_results
        method.
        """
        if not self.__done:
            self.gather_results()

        try:
            success = self._results_df["Avalanche"].value_counts()[True]
        except KeyError:
            success = 0

        pde = success / len(self._results_df)

        return pde*100

    @property
    def pde_std_error(self):
        """
        Photon Detection Efficiency std error in percent. If the simulation is
        not finished, this will create a blocking call to the gather_results
        method.
        """
        pde = self.pde/100
        std_error = (pde * (1-pde) / self.num_runs)**0.5

        return std_error*100

    @property
    def avalanche_success_compute_time(self):
        """
        Mean and std dev of compute time for successful avalanches. If the
        simulation is not finished, this will create a blocking call to the
        gather_results method.
        """
        if not self.__done:
            self.gather_results()

        avalanche_true_mask = self._results_df["Avalanche"]
        avalanche_success_compute_time_mean = round(
            self._results_df[avalanche_true_mask]["Compute Time (s)"].mean(), 2
        )
        avalanche_success_compute_time_sd = round(
            self._results_df[avalanche_true_mask]["Compute Time (s)"].std(), 2
        )

        return (
            avalanche_success_compute_time_mean,
            avalanche_success_compute_time_sd,
        )

    @property
    def avalanche_fail_compute_time(self):
        """
        Mean and std dev of compute time for failed avalanches. If the
        simulation is not finished, this will create a blocking call to the
        gather_results method.
        """
        if not self.__done:
            self.gather_results()

        avalanche_true_mask = self._results_df["Avalanche"]
        avalanche_false_mask = avalanche_true_mask == False  # noqa, pylint: disable=C0121

        avalanche_fail_compute_time_mean = round(
            self._results_df[avalanche_false_mask]["Compute Time (s)"].mean(), 2
        )
        avalanche_fail_compute_time_sd = round(
            self._results_df[avalanche_false_mask]["Compute Time (s)"].std(), 2
        )

        return (
            avalanche_fail_compute_time_mean,
            avalanche_fail_compute_time_sd,
        )

    @property
    def avalanche_results(self):
        """
        Returns a pandas.DataFrame with the following information:
            Index:
                RangeIndex
            Columns:
                Name: Avalanche, dtype=object
                Name: Rand Walk, dtype=object
                Name: Diffusion Time (ps), dtype=float64
                Name: Avalanche Time (ps), dtype=float64
                Name: Alive Charges, dtype=object
                Name: Dead Charges, dtype=object
                Name: Compute Time (s), dtype=float64

        If the simulation is not finished, this will create a blocking call to
        the gather_results method.
        """
        if not self.__done:
            self.gather_results()

        return self._results_df

    @property
    def exit_results(self):
        """
        Returns a pd.DataFrame of the exit locations of the charges in the
        simulation. See `Simulator.show_escape_regions()` for information about
        how the locations are defined. If the simulation is not finished, this
        will create a blocking call to the gather_results method.
        """
        if not self.__done:
            self.gather_results()

        return self._exit_df

    @property
    def deadspace_results(self):
        """
        Returns a pd.DataFrame of the deadspace results of the charges in the
        simulation. Use `Simulator.show_escape_regions()` for information about
        how the locations are defined. If the simulation is not finished, this
        will create a blocking call to the gather_results method.
        """
        if not self.__done:
            self.gather_results()

        return self._deadspace_df

    @property
    def pgen_initial_coords(self):
        """
        Returns a pd.DataFrame of the initial coordinates of the photogenerated
        charge in the simulation. If the simulation is not finished, this will
        create a blocking call to the gather_results method.
        """
        if not self.__done:
            self.gather_results()

        return self._pgen_coords_df

    @property
    def summary(self):
        """
        Return a summary DataFrame of the simulation. If the simulation is not
        finished, this will create a blocking call to the `gather_results`
        method.
        """
        keys = ["Num Runs", "PDE (%)", "Param File", "Pgen File", "Data File",
                "Successful Avalanche (s)", "Unsuccessful Avalanche (s)"]

        asct, asct_sd = self.avalanche_success_compute_time
        afct, afct_sd = self.avalanche_fail_compute_time
        values = [
            self.num_runs,
            f"{self.pde:.2f} {chr(177)} {self.pde_std_error:.2f}",
            self.param_file, self.pgen_file, self.data_file,
            f"{asct:.2f} {chr(177)} {asct_sd:.2f}",
            f"{afct:.2f} {chr(177)} {afct_sd:.2f}",
        ]

        summary_df = pd.DataFrame(data=values, index=keys, columns=["Results"])

        return summary_df

    def close(self):
        """
        Gracefully closes the Dask scheduler.
        """
        self.client.shutdown()
        self.client.close()
