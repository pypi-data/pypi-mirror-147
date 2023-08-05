"""
Simulator class for running the Monte Carlo avalanche simulation.
"""

import configparser as cp
from itertools import count
import time
from urllib.parse import urlparse
import urllib.request
import matplotlib.pyplot as plt
from numba import njit
import numpy as np
import pandas as pd
from tqdm import tqdm


class Simulator:
    """
    Monte Carlo Simulator class
    """

    # Constants
    e = 1.602176634e-19
    k = 1.380649e-23

    # Convert ionization threshold energies from eV to J
    e_ionization_threshold = 1.103 * e  #: e- ionization threshold energy (J)
    h_ionization_threshold = 1.269 * e  #: Hole ionization threshold energy (J)

    cm_to_nm = 1e7

    _escape_regions = """
                  _____3____
            2    |          |   4
         ________|     0    |________
    1   |        .          .        |   5
        |________.__________.________|
            8          7        6
    """

    def __init__(
        self,
        sim_datafile,
        pgen_datafile,
        parameter_file,
        test_suite=False,
        test_coord=None,
        rng_seed=None,
        disable_tqdm=True,
    ):
        """
        Initializes the Simulator class.

        Parameters
        ----------
        sim_datafile : str
            Path to the simulation data file. Can be local or remote. This file
            should contain the following 12 data columns:
            - x, y (cm) : Coordinates of the 2D simulation grid
            - Weighting Field x,y (V/cm) : Weighting field
            - Efield x,y (V/cm) : Electric field
            - ionization coeff e-,h+ : Electron and hole ionization coefficients
            - mobility e-,h+ (cm^2/Vs) : Electron and hole mobility
            - drift velocity e-,h+ (cm/s) : Electron and hole drift velocity
        - pgen_datafile : str
            Path to the pgen data file. Can be local or remote. This file
            should contain the following 3 data columns:
            - x, y (um) : coordinates of the 2D simulation grid
            - cumulative probability : Cumulative probability of photon
            absorption
        - parameter_file : str
            Path to the parameter file. Can be local or remote. This file
            will be parsed by the configparser module. The following 10
            parameters are required:
            - E-Field Threshold (V/cm) : Threshold e-field to determine if an
            injected/ photogenerated charge has reached the avalanche
            multiplication region and triggers the RPL calculations
            - Avalanche Threshold (A) : Threshold current to determine if an
            avalanche has been achieved.
            - RandWalk Maxtime (s) : Maximum time for a random walk before
            considering the simulation to be dead.
            - RandWalk Stepsize (cm) : Stepsize for random walk.
            - Sim Timestep (s) : Simulation timestep.
            - Sim Max Time (s) : Simulation maximum time.
            - x Core Left (cm) : Left boundary of the device core.
            - x Core Right (cm) : Right boundary of the device core.
            - WG Rib y-Coord (cm) : y-coordinate of the waveguide rib.
        - test_suite : bool, optional
            If True, the simulation will be run in test mode. The simulation
            will be run with a single charge carrier at the specified test_coord
            (optional) and a plot of the charge injection point and final
            position after the random walk will be generated. Default is False.
        - test_coord : np.ndarray of shape (2,), optional
            x & y coordinates of the injected charge carrier in cm, useful for
            testing. If not specified, a random test_coord will be generated.
            Default is None.
        - rng_seed : int, optional
            Random number generator seed. Useful for reproducibility during
            testing. Default is None.
        - disable_tqdm : bool, optional
            If True, tqdm progress bar will not be displayed. Useful for
            debugging. Should set to False only when running single simulations
            or only a few runs without any parallelisation. Do not set to True
            when running in parallel. Default is True.
        """

        if not isinstance(sim_datafile, str):
            raise TypeError("sim_datafile must be a string")
        if not isinstance(pgen_datafile, str):
            raise TypeError("pgen_datafile must be a string")
        if not isinstance(parameter_file, str):
            raise TypeError("parameter_file must be a string")
        if test_suite is not None:
            if not isinstance(test_suite, bool):
                raise TypeError("test_suite must be a boolean")
        if test_coord is not None:
            if isinstance(test_coord, (list, tuple)):
                if len(test_coord) != 2:
                    raise ValueError("test_coord must be a 2D vector")
                if not isinstance(test_coord[0], float):
                    raise ValueError("test_coord must be a 2D vector")
                if not isinstance(test_coord[1], float):
                    raise ValueError("test_coord must be a 2D vector")
            elif isinstance(test_coord, np.ndarray):
                if test_coord.shape != (2,):
                    raise ValueError("test_coord must be a 2D vector")
            else:
                raise TypeError("test_coord must be a list-like object")
        if rng_seed is not None:
            if not isinstance(rng_seed, int):
                raise TypeError("rng_seed must be an integer")
            if isinstance(rng_seed, bool):
                raise TypeError("rng_seed must be an integer")
            if rng_seed < 0:
                raise ValueError("rng_seed must be an integer >= 0")
        if not isinstance(disable_tqdm, bool):
            raise TypeError("disable_tqdm must be a boolean")

        self.disable_tqdm = disable_tqdm

        if rng_seed is not None:
            self.random = np.random.default_rng(rng_seed)
        else:
            self.random = np.random.default_rng()

        # --- Reading Input Files ---
        self.pgen = pd.read_csv(pgen_datafile, delimiter=" ", header=None,
                                comment="#").to_numpy()
        self.sim_data = pd.read_csv(sim_datafile, delimiter=" ", header=None,
                                    comment="#").to_numpy()

        # Need this because configparser cannot read remote files
        if urlparse(parameter_file).scheme == "":
            with open(parameter_file, "r", encoding="utf-8") as file:
                self._init_params(file.read())
        else:
            u = urllib.request.Request(parameter_file)
            with urllib.request.urlopen(u) as resp:
                p = resp.read()
            self._init_params(str(p, "utf-8"))  # Read param file

        # --- Debugging Parameters ---
        self.test_suite = test_suite
        if self.test_suite:
            if test_coord is not None:
                self.test_injection_coord = np.array(test_coord)

        # --- Extracting info from data file ---
        # Spatial coordinates, cm
        self.x = self.sim_data[:, 0].astype(float)
        self.y = self.sim_data[:, 1].astype(float)

        self.xy_all = np.column_stack((self.x, self.y))

        # Weighting field, V/cm
        weight_Ex = self.sim_data[:, 2].astype(float)
        weight_Ey = self.sim_data[:, 3].astype(float)
        self.weights_xy_all = np.column_stack((weight_Ex, weight_Ey))

        # Electric field, V/cm
        Ex = self.sim_data[:, 4].astype(float)
        Ey = self.sim_data[:, 5].astype(float)
        self.efield_xy_all = np.column_stack((Ex, Ey))

        # Ionization coefficients, dimensionless
        self.ion_e = self.sim_data[:, 6].astype(float)
        self.ion_h = self.sim_data[:, 7].astype(float)

        # Mobilities, cm^2/Vs
        self.mob_e = self.sim_data[:, 8].astype(float)
        self.mob_h = self.sim_data[:, 9].astype(float)

        # Drift velocities, cm/s
        self.driftv_e = self.sim_data[:, 10].astype(float)
        self.driftv_h = self.sim_data[:, 11].astype(float)

        # --- Define simulation boundaries ---
        self.x_uni, self.x_uni_idx = np.unique(self.x, return_index=True)
        self.y_uni = np.unique(self.y)
        self.x_device_right = self.x_uni[-1]  # cm
        self.x_device_left = self.x_uni[0]  # cm
        self.y_core_top = self.y_uni[-1]  # cm
        self.y_core_bottom = self.y_uni[0]  # cm

        # --- Lookup parameters ---
        self.x_min = self.x_uni[0]
        self.y_min = self.y_uni[0]
        # Doing -1 below here because all operations later require it
        self.num_xvals = len(self.x_uni) - 1
        self.num_yvals = len(self.y_uni) - 1

        # Here we want to do (max-min)/(#elements-1), except that the -1 has
        # been done above.
        self.resolution_x = (self.x_uni[-1] - self.x_uni[0]) / (self.num_xvals)
        self.resolution_y = (self.y_uni[-1] - self.y_uni[0]) / (self.num_yvals)
        self.gap = self.x_uni_idx[1] - self.x_uni_idx[0]

        # This is to reduce the number of arguments passed to the jitted
        # lookup method and to reduce memory access time for these constants
        # by making them a contiguous array
        self.lookup_jit_params = np.array(
            [
                self.x_min,
                self.y_min,
                self.resolution_x,
                self.resolution_y,
                self.num_xvals,
                self.num_yvals,
                self.gap,
            ]
        )

        # --- Initialising remaining variables ---
        self.charge_carriers = {}
        self.dead_charges = set()

        self.d_list = []  # To store diffusion constants
        # Deadspace is the distance travelled by a charge before ionizing.
        self.deadspace = None
        self.deadspace_start_coord = None
        self.deadspace_end_coord = None
        self.randwalk_timesteps = 0
        self.randwalk_finalcoord = np.zeros(2, dtype=np.float64)
        self.exit_list = np.zeros(9, dtype=np.int32)  # Keep track of exits
        self.diffusion_time = 0

        # This is to reduce the number of arguments passed to the jitted
        # escape_region method, similar to the lookup_jit_params above.
        self.escape_params = np.array(
            [
                self.x_device_left,
                self.x_device_right,
                self.x_core_left,
                self.x_core_right,
                self.y_core_top,
                self.y_core_bottom,
                self.wg_rib_y_coord,
            ]
        )

        self.injection_coord_raw = None
        self.injection_coord = None
        self.all_electrons = None
        self.all_holes = None
        self.total_timesteps = None
        self.charges_at_every_step = {}

        # --- Charge ID counter ---
        self._ids = count(0)

    def _init_params(self, param_file):
        """
        Parses data from the parameter file and stores them as attributes of
        this class.

        Parameters
        ----------
        param_file : str
            Path to the parameter file. Can be a local file or a remote URL.

        Returns
        -------
        None
        """
        config = cp.ConfigParser()
        config.read_string(param_file)
        self.dep_edge_efield_mag = float(
            config.get("Parameters", "E-Field Threshold")
        )
        self.temp = float(
            config.get("Parameters", "Temperature")
        )
        self.avalanche_threshold = float(
            config.get("Parameters", "Avalanche Threshold")
        )
        self.randwalk_maxtime = float(
            config.get("Parameters", "RandWalk Maxtime")
        )
        self.randwalk_stepsize = float(
            config.get("Parameters", "RandWalk Stepsize")
        )
        self.timestep = float(config.get("Parameters", "Sim Timestep"))
        self.maxtime = float(config.get("Parameters", "Sim Maxtime"))
        self.x_core_left = float(config.get("Parameters", "x Core Left"))
        self.x_core_right = float(config.get("Parameters", "x Core Right"))
        self.wg_rib_y_coord = float(config.get("Parameters", "WG Rib y-Coord"))

    @staticmethod
    @njit(fastmath=True)
    def lookup(pos, lookup_jit_params):
        """
        Maps the given position to the nearest [x,y] coordinate provided in the
        data file to perform a lookup of data at that coordinate.

        Parameters
        ----------
        pos : np.ndarray of shape (2,)
            The current position in the form [x,y] in cm.
        lookup_jit_params : np.ndarray of shape (7,)
            The parameters used to perform the lookup, defined in the __init__
            method. This is to make the lookup function faster.

        Returns
        -------
        field_idx : int
            The index of the nearest [x,y] coordinate in the data file.
        """

        idx = round((pos[0] - lookup_jit_params[0]) / lookup_jit_params[2])
        idy = round((pos[1] - lookup_jit_params[1]) / lookup_jit_params[3])

        if idx < 0:
            idx = 0
        elif idx > lookup_jit_params[4]:
            idx = lookup_jit_params[4]

        if idy < 0:
            idy = 0
        elif idy > lookup_jit_params[5]:
            idy = lookup_jit_params[5]

        return int(idx * lookup_jit_params[6] + idy)

    def get_injection_point(self, pgen_array):
        """
        Randomly generates the coordinates (cm) of the initial charge carrier
        injection point. Called at the start of main simulation routine.

        Parameters
        ----------
        pgen_array : np.ndarray
            Array that contains all the data from the pgen file.

        Returns
        -------
        Injection point : tuple of shape (2,)
            Coordinates in the form (x,y) in cm
        """

        r = self.random.uniform(0, 1)
        idx = np.where(pgen_array[:, 2] > r)[0][0]

        return (
            self.pgen[idx][0] * 1e-4,
            self.pgen[idx][1] * 1e-4,
        )  # Convert units from um to cm

    @classmethod
    def show_escape_regions(cls):
        """
        Prints a visualisation of the escape regions.
        """
        print(cls._escape_regions)

    @staticmethod
    @njit(fastmath=True)
    def escape_region(coord, exit_params):
        """
        Determines if charge is still within bounds of the device. Called
        whenever a charge changes its position to ensure it hasn't gone out of
        bounds. Use the `show_escape_regions()` method for a visualisation of
        the naming convention.

        Parameters
        ----------
        coord : np.ndarray of shape (2,)
            Position (cm) of the charge.

        Returns
        -------
        code : int from 0 to 9.
            0: Charge is still within bounds of the device.
            1-8: Charge has escaped the device from the respective edges.
        """

        x, y = coord[0], coord[1]

        if x < exit_params[0]:
            return 1
        if (exit_params[0] <= x <= exit_params[2]) and (y > exit_params[6]):
            return 2
        if (exit_params[2] < x < exit_params[3]) and (y > exit_params[4]):
            return 3
        if (exit_params[3] <= x <= exit_params[1]) and (y > exit_params[6]):
            return 4
        if x > exit_params[1]:
            return 5
        if (exit_params[3] <= x <= exit_params[1]) and (y < exit_params[5]):
            return 6
        if (exit_params[2] < x < exit_params[3]) and (y < exit_params[5]):
            return 7
        if (exit_params[0] <= x <= exit_params[2]) and (y < exit_params[5]):
            return 8

        return 0

    def diffusion(self, pos, sign):
        """
        Determines the diffusion parameters at a current position for a hole or
        electron in the neutral region.

        Parameters
        ----------
        pos : np.ndarray of shape (2,)
            Position (cm) of the charge.
        sign : int, either 1 or -1
            -1: electron
            1: hole

        Returns
        -------
        mobility : float
            Mobility of the charge in cm^2/Vs
        diffusion_coeff : float
            Diffusion coefficient of the charge in cm^2/s
        """
        e = 1.602176634e-19
        k = 1.380649e-23
        idx = self.lookup(pos, self.lookup_jit_params)
        mobility = self.mob_e[idx] if sign == -1 else self.mob_h[idx]

        return mobility, mobility * k * self.temp / e

    @staticmethod
    @njit(fastmath=True)
    def calc_drift_xy(sign, current_time_step, drift_v_mag_xy, efield_xy):
        """
        Calculates the drift displacement in x and y.

        Parameters
        ----------
        sign : int, either 1 or -1
            -1: electron
            1: hole
        current_time_step : float
            Duration of 1 time step in seconds
        drift_v_mag_xy : np.ndarray of shape (2,)
            Drift velocities in the x and y direction in cm/s^2
        efield_xy : np.ndarray of shape (2,)
            Electric field magnitude in the x and y direction in V/cm

        Returns
        -------
        Drift displacement: np.ndarray of shape (2,)
            Drift displacement in the x and y direction in cm
        """
        return sign * current_time_step * drift_v_mag_xy * np.sign(efield_xy)

    @staticmethod
    @njit(fastmath=True)
    def electron_impact(initial_energy, e_ionization_threshold):
        """
        Determines secondary electron and hole energies after electron impact
        ionization.

        Parameters
        ----------
        initial_energy : float
            Initial energy of electron in J.
        e_ionization_threshold : float
            Energy threshold for electron impact ionization in J.

        Returns
        -------
        secondary_electron_energy : float
            Energy of secondary electron in J.
        secondary_hole_energy : float
            Energy of secondary hole in J.
        """
        e = 1.602176634e-19
        energy_in_eV = initial_energy / e
        secondary_electron_energy = 0.29 * energy_in_eV - 0.32  # in eV
        secondary_hole_energy = (
            -1 * (-0.31 * energy_in_eV - 0.92) - e_ionization_threshold
        )  # in eV

        return (
            secondary_electron_energy * e,
            secondary_hole_energy * e,
        )

    @staticmethod
    @njit(fastmath=True)
    def hole_impact(initial_energy, h_ionization_threshold):
        """
        Determines secondary electron and hole energies after hole impact
        ionization.

        Parameters
        ----------
        initial_energy : float
            Initial energy of hole in J.
        h_ionization_threshold : float
            Energy threshold for hole impact ionization in J.

        Returns
        -------
        secondary_electron_energy : float
            Energy of secondary electron in J.
        secondary_hole_energy : float
            Energy of secondary hole in J.
        """
        e = 1.602176634e-19
        energy_in_eV = initial_energy / e
        secondary_hole_energy = 0.375 * energy_in_eV - 0.476  # in eV
        secondary_electron_energy = (
            -1 * (-0.314 * energy_in_eV - 0.860) - h_ionization_threshold
        )  # in eV

        return (
            secondary_electron_energy * e,
            secondary_hole_energy * e,
        )

    @staticmethod
    @njit(fastmath=True, inline="always")
    def charge_energy(efield_xy, drift_v_mag_xy, timestep):
        """
        Caclulates the energy possesed by an individual charge.

        Parameters
        ----------
        efield_xy : np.ndarray of shape (2,)
            Electric field magnitude in the x and y direction in V/cm
        drift_v_mag_xy : np.ndarray of shape (2,)
            Drift velocities in the x and y direction in cm/s^2
        timestep : float
            Duration of 1 RPL time step in seconds

        Returns
        -------
        Energy : float
            Energy of the charge in J.
        """
        e = 1.602176634e-19
        return (
            e * dot(np.abs(efield_xy), drift_v_mag_xy) * timestep
        )

    @staticmethod
    @njit(fastmath=True, inline="always")
    def charge_current(drift_v_mag, efield_xy, weights_xy):
        """
        Calculates the current contribution by an individual charge.

        Parameters
        ----------
        drift_v_mag : float
            Drift velocity magnitude in cm/s
        efield_xy : np.ndarray of shape (2,)
            Electric field magnitude in the x and y direction in V/cm
        weights_xy : np.ndarray of shape (2,)
            Weighting field in the x and y direction

        Returns
        -------
        Current : float
            Current contribution of the charge in A.
        """
        e = 1.602176634e-19
        return (
            -1
            * e
            * drift_v_mag
            * dot(efield_xy / norm(efield_xy), weights_xy)
        )

    @staticmethod
    @njit(fastmath=True, inline="always")
    def calc_cum_exponent(local_ion_coeff, drift_v_mag_xy, timestep):
        """
        Calculates the ionisation cumulative probability density of a charge
        carrier.

        Parameters
        ----------
        local_ion_coeff : float
            Ionisation coefficient of the charge carrier in cm^2/s
        drift_v_mag_xy : np.ndarray of shape (2,)
            Drift velocities in the x and y direction in cm/s^2
        timestep : float
            Duration of 1 RPL time step in seconds

        Returns
        -------
        Cumulative probability density : float
            Ionisation cumulative probability density of the charge carrier.
        """
        return local_ion_coeff * norm(drift_v_mag_xy) * timestep

    @staticmethod
    @njit(fastmath=True, inline="always")
    def calc_cum_prob(
        local_ion_coeff, charge_cum_expt, drift_v_mag_xy, timestep
    ):
        """
        Calculates the cumulative probability of ionisation of a charge
        carrier.

        Parameters
        ----------
        local_ion_coeff : float
            Ionisation coefficient of the charge carrier in cm^2/s
        charge_cum_expt : float
            Ionisation cumulative probability density of the charge carrier.
        drift_v_mag_xy : np.ndarray of shape (2,)
            Drift velocities in the x and y direction in cm/s^2
        timestep : float
            Duration of 1 RPL time step in seconds

        Returns
        -------
        Cumulative probability : float
            Ionisation cumulative probability of the charge carrier.
        """
        return (
            local_ion_coeff
            * np.exp(-1 * charge_cum_expt)
            * norm(drift_v_mag_xy)
            * timestep
        )

    @staticmethod
    @njit(fastmath=True, inline="always")
    def calc_drift_v_mag_xy(drift_v_mag, efield_xy):
        """
        Calculates the drift velocity magnitude in x and y directions.

        Parameters
        ----------
        drift_v_mag : float
            Drift velocity magnitude in cm/s
        efield_xy : np.ndarray of shape (2,)
            Electric field magnitude in the x and y direction in V/cm

        Returns
        -------
        drift_v_mag_xy : np.ndarray of shape (2,)
            Drift velocities in the x and y direction in cm/s^2
        """
        norm_efield_xy = norm(efield_xy)
        return drift_v_mag * np.abs(efield_xy) / norm_efield_xy, norm_efield_xy

    @staticmethod
    @njit(fastmath=True)
    def calc_xy_new(
        charge_pos, timestep, charge_sign, drift_v_mag_xy, efield_xy
    ):
        """
        Calculates new position of a charge carrier after moving due to drift
        velocity.

        Parameters
        ----------
        charge_pos : np.ndarray of shape (2,)
            Position of the charge carrier in the x and y directions in cm.
        timestep : float
            Duration of 1 RPL time step in seconds
        charge_sign : int
            Sign of the charge carrier.
        drift_v_mag_xy : np.ndarray of shape (2,)
            Drift velocities in the x and y direction in cm/s^2
        efield_xy : np.ndarray of shape (2,)
            Electric field magnitude in the x and y direction in V/cm

        Returns
        -------
        new_charge_pos : np.ndarray of shape (2,)
            New position of the charge carrier in the x and y directions in cm.
        """
        return (
            charge_pos
            + timestep * charge_sign * drift_v_mag_xy * np.sign(efield_xy)
        )

    def add_charge_carrier(
        self,
        id_num,
        name,
        pos,
        start_t,
        rand_uniform,
        energy=0.0,
        cum_prob=0.0,
        cum_exponent=0.0,
        current=0.0,
    ):
        """
        Adds a new charge carrier to a dictionary of charge carriers.

        Parameters
        ----------
        id_num : int
            Unique identifier of the charge carrier.
        name : str, either "electron" or "hole"
            Name of the charge carrier.
        pos : np.ndarray of shape (2,)
            Position of the charge carrier in the x and y directions in cm.
        start_t : float
            Time at which the charge carrier is created in seconds.
        rand_uniform : float
            Random number used to determine if impact ionisation is successful.
        energy : float
            Energy of the charge carrier in J.
        cum_prob : float
            Ionisation cumulative probability of the charge carrier.
        cum_exponent : float
            To calculate ionisation cumulative probability density of the
            charge carrier.
        current : float
            Current contribution of the charge carrier in A.

        Returns
        -------
        None
        """
        sign = 1 if name == "hole" else -1

        new_charge = {
            "name": name,
            "sign": sign,
            "pos": pos,
            "random": rand_uniform,
            "energy": energy,
            "cum_prob": cum_prob,
            "cum_exponent": cum_exponent,
            "current": current,
            "start_pos": pos,
            "start_t": start_t,
            "threshold_pos": np.zeros(2, dtype=np.float64),
            "threshold_t": 0.0,
            "impact_pos": np.zeros(2, dtype=np.float64),
            "impact_t": 0.0,
            "travelled_distance": 0.0,
            "dead": False,
            "crossed_thresh": False,
        }

        self.charge_carriers[id_num] = new_charge

    def threshold_check(self, pos):
        """
        Checks if threshold E-field has been encountered.

        Parameters
        ----------
        pos : np.ndarray of shape (2,)
            Position of the charge carrier in the x and y directions in cm.

        Returns
        -------
        result: bool
            True if threshold E-field has been encountered, else False.
        """
        idx = self.lookup(pos, self.lookup_jit_params)
        e_field = self.efield_xy_all[idx]
        return norm(e_field) > self.dep_edge_efield_mag

    def plot_routine(self):
        """
        Plots device geometry, the device edges, the injection coord and the
        random walk final coordinate, if any. Only called when test_suite is
        True.
        """
        # Plots the injection coordinate
        plt.plot(
            self.injection_coord[0] * Simulator.cm_to_nm,
            self.injection_coord[1] * Simulator.cm_to_nm,
            marker="o",
            markersize=3,
            color="red",
        )

        # Plots the random walk final coordinate, if random walk was called
        if self.randwalk_timesteps:
            plt.plot(
                self.randwalk_finalcoord[0] * Simulator.cm_to_nm,
                self.randwalk_finalcoord[1] * Simulator.cm_to_nm,
                marker="o",
                markersize=3,
                color="blue",
            )

        plt.xlim(
            self.x_device_left * Simulator.cm_to_nm,
            self.x_device_right * Simulator.cm_to_nm,
        )
        plt.ylim(
            self.y_core_bottom * Simulator.cm_to_nm,
            self.y_core_top * Simulator.cm_to_nm,
        )

        # --- Plot device edges ---
        device_x_edges = [
            self.x_core_left * Simulator.cm_to_nm,
            self.x_core_right * Simulator.cm_to_nm,
        ]
        for i in device_x_edges:
            plt.axvline(
                i,
                ymin=(self.wg_rib_y_coord - self.y_core_bottom)
                / (self.y_core_top - self.y_core_bottom),
                ymax=1,
                color="k",
            )
        plt.axhline(
            self.wg_rib_y_coord * Simulator.cm_to_nm,
            xmin=0.0,
            xmax=abs(
                (self.x_device_left - self.x_core_left)
                / (self.x_device_left - self.x_device_right)
            ),
            color="k",
        )
        plt.axhline(
            self.wg_rib_y_coord * Simulator.cm_to_nm,
            xmin=abs(
                (self.x_device_left - self.x_core_right)
                / (self.x_device_left - self.x_device_right)
            ),
            xmax=1,
            color="k",
        )

        plt.yticks(
            [
                self.y_core_bottom * Simulator.cm_to_nm,
                0,
                self.y_core_top * Simulator.cm_to_nm,
            ]
        )
        plt.show()

    def reset_simulation(self):
        """
        Resets simulation attributes to prepare for another run.
        """
        self.charge_carriers = {}
        self.dead_charges = set()

        self.d_list = []
        self.deadspace = None
        self.deadspace_start_coord = None
        self.deadspace_end_coord = None
        self.randwalk_timesteps = 0
        self.randwalk_finalcoord = np.zeros(2, dtype=np.float64)
        self.exit_list = np.zeros(9, dtype=np.int32)
        self.diffusion_time = 0

        self.injection_coord_raw = None
        self.injection_coord = None
        self.all_electrons = None
        self.all_holes = None
        self.total_timesteps = None
        self.charges_at_every_step = {}

        # --- Charge ID counter ---
        self._ids = count(0)

    def generate_injection_point(self, check_sim_reset=True):
        """
        Generates injection point of photogenerated charge. Adds electron-hole
        pair to list of charges for random walk.

        Parameters
        ----------
        check_sim_reset : bool
            If True, checks if simulation has been reset and raises error if
            not. Default is True. Should only set to False when testing or
            debugging.

        Returns
        -------
        None
        """
        if check_sim_reset:
            # Check again that the simulator has been reset.
            if len(self.charge_carriers) != 0:
                raise RuntimeError(
                    "Simulation has not been reset. Please call "
                    "reset_simulation() first."
                )

        # If in debugging mode, manually fix injection point if specified
        if self.test_suite:
            try:
                self.injection_coord_raw = self.test_injection_coord
            except AttributeError:
                self.injection_coord_raw = self.get_injection_point(self.pgen)
        else:
            self.injection_coord_raw = self.get_injection_point(self.pgen)

        injection_coord_lookup_idx = self.lookup(
            self.injection_coord_raw, self.lookup_jit_params
        )

        # [x,y] of injection point in [cm,cm]
        self.injection_coord = self.xy_all[injection_coord_lookup_idx]

        # Adds electron-hole pair to charge list
        self.add_charge_carrier(
            next(self._ids),
            "electron",
            self.injection_coord,
            0,
            self.random.uniform(0, 1),
        )
        self.add_charge_carrier(
            next(self._ids),
            "hole",
            self.injection_coord,
            0,
            self.random.uniform(0, 1),
        )

        # Defining these additional parameters that are only used for charges
        # in the random walk routine
        for _, charge in self.charge_carriers.items():
            charge["t_step"] = 0
            charge["injected"] = False

    def rand_walk(self, id_num):
        """
        Updates position of a given charge carrier for one timestep. Charge
        moves due to both brownian motion and local electric field.

        Parameters
        ----------
        id_num : int
            ID number of charge carrier to update.

        Returns
        -------
        timesteps : int
            Number of timesteps the charge took to cover the total
            displacement. This is generally 1, but can be higher if the
            charge carrier is in a region with a small diffusion constant.
        position : np.ndarray of shape (2,)
            Final position of charge carrier after one timestep.
        """
        pos = self.charge_carriers[id_num]["pos"]
        sign = self.charge_carriers[id_num]["sign"]
        name = self.charge_carriers[id_num]["name"]

        D = self.diffusion(pos, sign)[1]
        idx = self.lookup(pos, self.lookup_jit_params)
        efield_xy = self.efield_xy_all[idx]

        # Time (s) to travel randwalk_stepsize with local diffusion coefficient
        current_time_step = (self.randwalk_stepsize**2) / (2 * D)

        # Matching randwalk timestep to main simulation timestep
        if current_time_step < self.timestep:
            num_timesteps = 1
        else:
            num_timesteps = np.ceil(self.timestep / current_time_step)

        # Drift velocity magnitude, cm/s
        drift_v_mag = (
            self.driftv_e[idx] if name == "electron" else self.driftv_h[idx]
        )
        # Drift velocity vector, cm/s
        drift_v_mag_xy = (
            drift_v_mag * np.fabs(efield_xy) / norm(efield_xy)
        )
        # Displacement due to drift, cm
        drift_xy = self.calc_drift_xy(
            sign, current_time_step, drift_v_mag_xy, efield_xy
        )

        # Brownian motion angle is randomly determined
        angle = self.random.uniform(0, 2 * np.pi)
        # Displacement due to brownian motion, cm
        brownian_xy = self.randwalk_stepsize * np.array(
            [np.cos(angle), np.sin(angle)]
        )

        # Total random walk displacement, cm
        xy_new = pos + drift_xy + brownian_xy

        return num_timesteps, xy_new

    def RPL(self, id_num):
        """
        Random Path Length. Simulates one timestep for a charge in the
        depletion region and updates the charge's properties where relevant.

        Parameters
        ----------
        id_num : int
            ID number of charge carrier to simulate.

        Returns
        -------
        impact : bool
            True if charge successfully impact ionises, else False.
        outofbounds: bool
            True if charge exits device, else False
        cross_ion_threshold : bool
            True if charge's energy exceeds ionization threshold, else False
        exit_code : int
            0 : Charge is still within bounds of device
            1-8: Charge has escaped the device from the respective edges. See
            Simulator.escape_region docstring for details.
        norm_efield_xy : float
            Normalized electric field vector at charge's position.
        """
        impact, outofbounds, cross_ion_threshold = False, False, False
        pos = self.charge_carriers[id_num]["pos"]
        name = self.charge_carriers[id_num]["name"]

        idx = self.lookup(pos, self.lookup_jit_params)
        efield_xy = self.efield_xy_all[idx]  # E-field in V/cm

        # Displacement due to drift
        local_ion_coeff = (
            self.ion_e[idx] if name == "electron" else self.ion_h[idx]
        )
        # Drift velocity magnitude, cm/s
        drift_v_mag = (
            self.driftv_e[idx] if name == "electron" else self.driftv_h[idx]
        )
        # Drift velocity vector, cm/s
        drift_v_mag_xy, norm_efield_xy = self.calc_drift_v_mag_xy(
            drift_v_mag, efield_xy
        )

        # Update position of charge carrier
        xy_new = self.calc_xy_new(
            pos,
            self.timestep,
            self.charge_carriers[id_num]["sign"],
            drift_v_mag_xy,
            efield_xy,
        )
        self.charge_carriers[id_num]["pos"] = xy_new

        # Track distance travelled by injected charge to calculate deadspace
        if self.charge_carriers[id_num]["start_t"] == 0:
            self.charge_carriers[id_num]["travelled_distance"] += (
                norm(drift_v_mag_xy) * self.timestep
            )

        # Check if charge has escaped the device
        exit_code = self.escape_region(xy_new, self.escape_params)
        if exit_code != 0:
            outofbounds = True

        # Update charge attributes
        # Energy in J
        self.charge_carriers[id_num]["energy"] += self.charge_energy(
            efield_xy, drift_v_mag_xy, self.timestep
        )
        # Current in A, calculated via generalized Ramo's Theorem
        self.charge_carriers[id_num]["current"] = self.charge_current(
            drift_v_mag, efield_xy, self.weights_xy_all[idx]
        )
        # Note: Drift v is a scalar, so we take
        # velocity = drift v * unit vector of actual E-field to factor in
        # direction. Electrons have a -1 factor from the negative
        # charge (e is +ve) and another -1 factor from moving against
        # the E-field. Thus, charge.current has an overall + sign.

        # Check if ionization threshold has been reached
        if name == "electron":
            ion_threshold = Simulator.e_ionization_threshold
        else:
            ion_threshold = Simulator.h_ionization_threshold
        if self.charge_carriers[id_num]["energy"] > ion_threshold:
            if self.charge_carriers[id_num]["crossed_thresh"] is False:
                # If it is crossing threshold for the first time
                cross_ion_threshold = True
                self.charge_carriers[id_num]["crossed_thresh"] = True
            else:
                self.charge_carriers[id_num]["cum_exponent"] +=\
                    self.calc_cum_exponent(
                        local_ion_coeff,
                        drift_v_mag_xy,
                        self.timestep,
                    )
                self.charge_carriers[id_num]["cum_prob"] +=\
                    self.calc_cum_prob(
                        local_ion_coeff,
                        self.charge_carriers[id_num]["cum_exponent"],
                        drift_v_mag_xy,
                        self.timestep,
                    )  # Eqn 7 of 2018 paper
                if (
                    self.charge_carriers[id_num]["cum_prob"]
                    > self.charge_carriers[id_num]["random"]
                ):
                    impact = True

        return (
            impact,
            outofbounds,
            cross_ion_threshold,
            exit_code,
            norm_efield_xy,
        )

    def run_simulation(self, save_charges_at_every_step=False):
        """
        Main simulation loop. Does the following:
        1) Random walk for intially injected electron-hole pair.
        2) Once e-field threshold is reached, begin RPL sequence.

        Parameters
        ----------
        save_charges_at_every_step : bool
            If True, saves the charge's properties at every timestep. This
            is useful for debugging, but can significantly slow down the
            simulation.
        """
        start_time = time.time()
        t = 0  # Not time, number of timesteps
        max_timesteps = self.maxtime / self.timestep
        avalanche = False
        RPL = False

        if save_charges_at_every_step:
            self.all_electrons = {}
            self.all_holes = {}
            for id_num, charge in self.charge_carriers.items():
                if charge["name"] == "electron":
                    self.all_electrons[t] = [[
                        id_num,
                        t,
                        charge["pos"][0],
                        charge["pos"][1],
                        charge["current"]]
                    ]
                elif charge["name"] == "hole":
                    self.all_holes[t] = [[
                        id_num,
                        t,
                        charge["pos"][0],
                        charge["pos"][1],
                        charge["current"]]
                    ]

        # This while loop is the random walk process
        while not RPL:
            if len(self.charge_carriers) == len(self.dead_charges):
                break
            for id_num, charge in self.charge_carriers.items():
                if id_num not in self.dead_charges:
                    tsteps_taken, xy_new = self.rand_walk(id_num)
                    exit_code = self.escape_region(xy_new, self.escape_params)

                    if exit_code != 0:
                        self.exit_list[exit_code - 1] += 1
                        charge["dead"] = True
                        self.dead_charges.add(id_num)
                        continue

                    charge["pos"] = xy_new
                    charge["t_step"] += tsteps_taken

                    tstep_now = charge["t_step"]

                    if save_charges_at_every_step:
                        if charge["name"] == "electron":
                            self.all_electrons[tstep_now] = [[
                                id_num,
                                t,
                                charge["pos"][0],
                                charge["pos"][1],
                                charge["current"]]
                            ]

                        elif charge["name"] == "hole":
                            self.all_holes[tstep_now] = [[
                                id_num,
                                t,
                                charge["pos"][0],
                                charge["pos"][1],
                                charge["current"]]
                            ]

                    if self.threshold_check(xy_new):
                        RPL = True
                        self.randwalk_finalcoord[:] = (
                            charge["pos"]
                        )
                        t = charge["t_step"]
                        self.randwalk_timesteps = t
                        break

                    if charge["t_step"] >= max_timesteps:
                        break

        if RPL:
            pbar = tqdm(
                total=self.avalanche_threshold * 1e6,
                desc=f"Avalanche Current ({chr(181)}A)",
                disable=self.disable_tqdm,
            )

            while t < max_timesteps:
                current = 0
                alive_charges = set(
                    range(len(self.charge_carriers))
                ).difference(self.dead_charges)

                for id_num in alive_charges:
                    (
                        impact,
                        outofbounds,
                        cross_ion_threshold,
                        exit_code,
                        norm_efield_xy,
                    ) = self.RPL(id_num)

                    if outofbounds:  # Charge is out of device, it is dead
                        self.exit_list[exit_code - 1] += 1
                        self.charge_carriers[id_num]["dead"] = True
                        self.dead_charges.add(id_num)
                        continue

                    if norm_efield_xy < self.dep_edge_efield_mag:
                        # If outside depletion region, consider charge dead.
                        # Saves compute time rather than waiting for charge to
                        # slowly drift to device edge and exit device.
                        self.exit_list[8] += 1
                        self.charge_carriers[id_num]["dead"] = True
                        self.dead_charges.add(id_num)
                        continue

                    if cross_ion_threshold:
                        self.charge_carriers[id_num]["threshold_pos"] = (
                            self.charge_carriers[id_num]["pos"]
                        )
                        self.charge_carriers[id_num]["threshold_t"] = t
                        if (
                            self.deadspace is None and
                            self.charge_carriers[id_num]["start_t"] == 0
                        ):
                            self.deadspace = (
                                self.charge_carriers[id_num][
                                    "travelled_distance"
                                ]
                            )
                            self.deadspace_start_coord = (
                                self.charge_carriers[id_num]["start_pos"]
                            )
                            self.deadspace_end_coord = (
                                self.charge_carriers[id_num]["pos"]
                            )
                            self.diffusion_time = t

                    if impact:
                        self.charge_carriers[id_num]["impact_pos"] = (
                            self.charge_carriers[id_num]["pos"]
                        )
                        self.charge_carriers[id_num]["impact_t"] = t
                        # Create new electron-hole pair
                        if self.charge_carriers[id_num]["name"] == "electron":
                            (
                                new_electron_energy,
                                new_hole_energy,
                            ) = self.electron_impact(
                                self.charge_carriers[id_num]["energy"],
                                Simulator.e_ionization_threshold,
                            )
                            self.charge_carriers[id_num]["energy"] = (
                                new_electron_energy
                            )

                        else:  # If charge is a hole
                            (
                                new_electron_energy,
                                new_hole_energy,
                            ) = self.hole_impact(
                                self.charge_carriers[id_num]["energy"],
                                Simulator.h_ionization_threshold,
                            )
                            self.charge_carriers[id_num]["energy"] = (
                                new_hole_energy
                            )

                        # Add the new charge carriers into the list of charges
                        self.add_charge_carrier(
                            next(self._ids),
                            "hole",
                            self.charge_carriers[id_num]["pos"],
                            t,
                            self.random.uniform(0, 1),
                            energy=new_hole_energy,
                        )
                        self.add_charge_carrier(
                            next(self._ids),
                            "electron",
                            self.charge_carriers[id_num]["pos"],
                            t,
                            self.random.uniform(0, 1),
                            energy=new_electron_energy,
                        )

                        # Reset these to 0
                        self.charge_carriers[id_num]["cum_prob"] = 0
                        self.charge_carriers[id_num]["cum_exponent"] = 0

                    # Add this charge's contribution to the total current
                    current += self.charge_carriers[id_num]["current"]

                if save_charges_at_every_step:
                    electrons_at_this_iter = []
                    holes_at_this_iter = []

                    for id_num, charge in self.charge_carriers.items():
                        if id_num not in self.dead_charges:
                            if charge["name"] == "electron":
                                electrons_at_this_iter.append([
                                    id_num,
                                    t,
                                    charge["pos"][0],
                                    charge["pos"][1],
                                    charge["current"]
                                ])
                            elif charge["name"] == "hole":
                                holes_at_this_iter.append([
                                    id_num,
                                    t,
                                    charge["pos"][0],
                                    charge["pos"][1],
                                    charge["current"]
                                ])

                    self.all_electrons[t] = electrons_at_this_iter
                    self.all_holes[t] = holes_at_this_iter

                if current >= self.avalanche_threshold:
                    avalanche = True
                    break

                # Prevents the progress bar from overflowing
                pbar.update(current * 1e6 - pbar.n)

                # If all charges are dead
                if len(self.charge_carriers) == len(self.dead_charges):
                    break

                t += 1  # Move on to the next timestep

            pbar.close()
            self.total_timesteps = t

        # --- Final outputs & cleanup ---
        elapsed_time = time.time() - start_time

        result = [
            avalanche,
            RPL,
            self.diffusion_time / 100,
            (t - self.diffusion_time) / 100,
            len(self.charge_carriers) - len(self.dead_charges),
            len(self.dead_charges),
            elapsed_time,
        ]

        if self.deadspace is not None:  # Print deadspace stats, if any
            deadspace_result = [
                self.deadspace * Simulator.cm_to_nm,
                self.deadspace_start_coord[0] * Simulator.cm_to_nm,
                self.deadspace_start_coord[1] * Simulator.cm_to_nm,
                self.deadspace_end_coord[0] * Simulator.cm_to_nm,
                self.deadspace_end_coord[1] * Simulator.cm_to_nm,
            ]
        else:
            deadspace_result = [None] * 5

        # --- Debugging Plots ---
        if self.test_suite:
            self.plot_routine()

        if save_charges_at_every_step:
            self.charges_at_every_step = {
                "electrons": self.all_electrons,
                "holes": self.all_holes,
            }

        return (
            result,
            self.exit_list,
            deadspace_result,
            self.injection_coord*Simulator.cm_to_nm,
        )

    @property
    def final_alive_charges(self):
        """
        Returns a set of the IDs of charges that are alive at the end of the
        simulation. If simulator is run multiple times, only the results of
        the last simulation are returned.
        """

        return set(range(len(self.charge_carriers))).difference(
            self.dead_charges
        )

    @property
    def final_dead_charges(self):
        """
        Returns a set of the IDs of charges that are dead at the end of the
        simulation. If simulator is run multiple times, only the results of
        the last simulation are returned.
        """

        return self.dead_charges

    @property
    def electrons_per_tstep(self):
        """
        Returns a dictionary of electrons that are alive at every time step of
        the simulation. The keys are the timesteps, and the values are a list
        of a snapshot of the charge attributes at that timestep. Requires that
        the simulation is run with the `save_charges_at_every_step` argument
        set to True in the run_sequence method.
        """

        return self.charges_at_every_step.get("electrons")

    @property
    def holes_per_tstep(self):
        """
        Returns a dictionary of holes that are alive at every time step of the
        simulation. The keys are the timesteps, and the values are a list of a
        snapshot of the charge attributes at that timestep. Requires that the
        simulation is run with the `save_charges_at_every_step` argument set to
        True in the run_sequence method.
        """

        return self.charges_at_every_step.get("holes")

    def run_sequence(
        self,
        num_runs,
        save_charges_at_every_step=False
    ):
        """
        Convenience function to run the simulation (possibly) multiple times
        and return the results.
        1) Reset simulation
        2) Generate injection point
        3) Run simulation

        Parameters
        ----------
        num_runs : int
            Number of times to run the simulation.
        save_charges_at_every_step : bool
            Whether to save the state of the charges at every timestep.
            Accessible via the `electrons_per_tstep` and `holes_per_tstep`
            property. Useful for for debugging. Default is False. Incurs some
            performance penalty. If this is used, num_runs must be 1 since only
            the last simulation's results are saved. Raises RuntimeError if
            num_runs > 1 and save_charges_at_every_step is True.

        Returns
        -------
        results : pd.DataFrame
            DataFrame containing the results of the simulation.
        exit_results : pd.DataFrame
            DataFrame containing the exit points of the charges for failed
            random walks.
        deadspace_results : pd.DataFrame
            DataFrame containing the deadspace stats for each run.
        """

        if save_charges_at_every_step and num_runs > 1:
            raise RuntimeError(
                "Cannot save charges at every step if num_runs > 1"
            )
        if not isinstance(num_runs, int):
            raise TypeError("num_runs must be an integer")
        if isinstance(num_runs, bool):
            raise TypeError("num_runs must be an integer")
        if num_runs < 1:
            raise ValueError("num_runs must be an integer >= 1")
        if not isinstance(save_charges_at_every_step, bool):
            raise TypeError("save_charges_at_every_step must be a boolean")

        result_chunk_df = pd.DataFrame(
            columns=[
                "Avalanche",
                "Rand Walk",
                "Diffusion Time (ps)",
                "Avalanche Time (ps)",
                "Alive Charges",
                "Dead Charges",
                "Compute Time (s)",
            ]
        )
        exit_chunk_df = pd.DataFrame(
            columns=[f"region_{r+1}" for r in range(len(self.exit_list))]
        )
        deadspace_chunk_df = pd.DataFrame(
            columns=[
                "Deadspace (nm)",
                "Deadspace start x (nm)",
                "Deadspace start y (nm)",
                "Deadspace end x (nm)",
                "Deadspace end y (nm)",
            ]
        )
        pgen_start_coord_chunk_df = pd.DataFrame(
            columns=[
                "Start_x (nm)",
                "Start_y (nm)",
            ]
        )

        for i in range(num_runs):
            # Resets simulation variables
            self.reset_simulation()
            # Starts the next simulation, ends at random walk
            self.generate_injection_point()
            # Start the RPL sequence
            (
                result_chunk_df.loc[i],
                exit_chunk_df.loc[i],
                deadspace_chunk_df.loc[i],
                pgen_start_coord_chunk_df.loc[i],
            ) = self.run_simulation(save_charges_at_every_step)

        return (
            result_chunk_df,
            exit_chunk_df,
            deadspace_chunk_df,
            pgen_start_coord_chunk_df,
        )


@njit(fastmath=True)
def norm(x_y):
    """
    Fast function to calculate the norm of a 2D vector.

    Parameters
    ----------
    x_y : ndarray of shape (2,)
        Vector to calculate the norm of.

    Returns
    -------
    norm : float
        Norm of the vector.
    """
    i = x_y[0]
    j = x_y[1]

    return (i*i + j*j) ** 0.5


@njit(fastmath=True)
def dot(x, y):
    """
    Fast function to calculate the dot product of a 2D vector.

    Parameters
    ----------
    x : ndarray of shape (2,)
        First input vector.
    y : ndarray of shape (2,)
        Second input vector.

    Returns
    -------
    dot : float
        Dot product of the vectors.
    """
    return x[0]*y[0] + x[1]*y[1]
