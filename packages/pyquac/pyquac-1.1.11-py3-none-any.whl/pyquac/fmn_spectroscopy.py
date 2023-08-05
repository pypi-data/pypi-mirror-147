# built-in libraries
from time import perf_counter
from typing import Iterable, Union
import time
# installable libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import numba as nb

# working with 2nd qubit
from scipy.optimize import curve_fit

# devices
import zhinst
import zhinst.ziPython
from drivers.M9290A import *
from drivers.N5183B import *
from drivers.znb_besedin import *
from resonator_tools import circlefit
from resonator_tools.circuit import notch_port

# family class
from pyquac.fmn_datatools import TwoToneSpectroscopy, timer


def _fit_cos(t, A1, A0, omega, teta):
    return A1 * np.cos(2 * np.pi * omega * t + teta) + A0


class Tts(TwoToneSpectroscopy):
    """
    Two Tone Spectroscopy for 1 qubit measurements
    """

    def __init__(self,
                 *, x_min, x_max, y_min, y_max,
                 fr_min: float, fr_max: float,
                 nx_points=None, x_step=None,
                 y_step=None, ny_points=None,
                 hdawg_port: str = '127.0.0.1', hdawg_port1: int = 8004, hdawg_mode: int = 6,
                 hdawg_device: str = 'dev8210', hdawg_channel: int = 5,
                 LO_port: str = 'TCPIP0::192.168.180.143::hislip0::INSTR',
                 LO_res_port: str = 'TCPIP0::192.168.180.110::inst0::INSTR',
                 LO_set_power: int = 5,
                 LO_res_set_bandwidth: int = 20, LO_res_set_power: int = -10, LO_res_set_nop=101,
                 base_bandwidth=40, LO_res_set_averages=1, LO_res_meas_averages=1
                 ):
        """
        Class provides methods for working with live data for Two Tone Spectroscopy
        :param x_min: x minimum value (int | float)
        :param x_max: x maximum value (int | float)
        :param y_min: y minimum value (int | float)
        :param y_max: y maximum value (int | float)
        :param nx_points: x count value (int)
        :param x_step: x step value (float)
        :param ny_points: y count value (int)
        :param y_step: y step value (float)
        :param fr_min: min frequency for find resonator
        :param fr_max: max frequency for find resonator
        :param hdawg_port: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param hdawg_port1: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param hdawg_mode: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param LO_port: qubit LO = N5183B('N5183B', LO_port)
        :param LO_res_port: resonator LO_res = Znb(LO_res_port)
        :param hdawg_device: 'dev8210' by default
        :param hdawg_channel: hdawg.setInt('/' + hdawg_device + '/sigouts/' + str(hdawg_channel) + '/on', 1)
        :param LO_set_power: base LO power (default 5)
        :param LO_res_set_bandwidth: bandwidth during resonator tuning
        :param LO_res_set_power: base resonator LO power (default -10)
        :param LO_res_set_nop: number of points during resonator scanning (default 101)
        :param base_bandwidth: (int) bandwidth during mesurments
        :param LO_res_set_averages: set averages for resonator LO parameter
        :param LO_res_meas_averages: measure averages for resonator LO parameter
        """

        super().__init__(x_min=x_min, x_max=x_max, nx_points=nx_points, y_min=y_min, y_max=y_max, ny_points=ny_points,
                         x_step=x_step, y_step=y_step)

        self.fr_min = fr_min
        self.fr_max = fr_max
        self.hdawg_channel = hdawg_channel
        self.hdawg_device = hdawg_device

        # HDAWG init
        self.hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        self.hdawg_setDouble = '/' + self.hdawg_device + '/sigouts/' + str(self.hdawg_channel) + '/offset'
        # open HDAWG ZI
        hdawgModule = self.hdawg.awgModule()

        # freq generator init
        self.LO = N5183B('N5183B', LO_port)  # qubit
        self.LO_res = Znb(LO_res_port)  # resonator

        # set base parameters
        self.LO_set_power = LO_set_power
        self.LO_res_set_nop = LO_res_set_nop
        self.LO_res_set_bandwidth = LO_res_set_bandwidth
        self.LO_res_set_power = LO_res_set_power
        self.base_bandwidth = base_bandwidth
        self.LO_res_set_averages = LO_res_set_averages
        self.LO_res.set_averages(LO_res_set_averages)
        self.LO_res_meas_averages = LO_res_meas_averages

        pass

    @property
    def __find_resonator(self):

        self.LO.set_status(0)

        # prior bandwidth
        bandwidth = self.LO_res.get_bandwidth()
        xlim = self.LO_res.get_freq_limits()

        self.LO_res.set_bandwidth(self.LO_res_set_bandwidth)
        self.LO_res.set_nop(self.LO_res_set_nop)
        self.LO_res.set_freq_limits(self.fr_min, self.fr_max)
        self.LO_res.set_averages(self.LO_res_set_averages)

        # measure S21
        freqs = self.LO_res.get_freqpoints()
        notch = notch_port(freqs, self.LO_res.measure()['S-parameter'])
        notch.autofit(electric_delay=60e-9)
        result = round(notch.fitresults['fr'])

        # Resetting to the next round of measurements
        self.LO_res.set_bandwidth(bandwidth)
        self.LO_res.set_freq_limits(*xlim)
        self.LO_res.set_nop(1)
        self.LO.set_status(1)

        return result

    def run_measurements(self, *, x_key: Union[float, int, Iterable] = None, y_key: Union[float, int, Iterable] = None,
                         x_min=None, x_max=None, y_min=None, y_max=None,
                         sleep=0.007, timeout=None):

        # Turn on HDAWG
        self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.hdawg_channel) + '/on', 1)

        self.iter_setup(x_key=x_key, y_key=y_key,
                        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)

        # Set power
        self.LO.set_power(self.LO_set_power)
        self.LO_res.set_power(self.LO_res_set_power)
        # base bandwidth
        self.LO_res.set_bandwidth(self.base_bandwidth)
        try:
            for i in range(len(self.load)):
                if (i == 0) or (self.load[i] != self.load[i - 1]):
                    self.LO_res.set_center(float(self.__find_resonator))

                    if timeout is not None:
                        timer.sleep(timeout)
                    else:
                        pass
                # measurement averages
                self.LO_res.set_averages(self.LO_res_meas_averages)

                self.hdawg.setDouble(self.hdawg_setDouble, self.load[i])  # Current write
                self.LO.set_frequency(self.frequency[i])  # Frequency write

                result = self.LO_res.measure()['S-parameter']

                self.write(x=self.load[i],
                           y=self.frequency[i],
                           heat=20 * np.log10(abs(result)[0])
                           )
                timer.sleep(sleep)

        except KeyboardInterrupt:
            pass

        # Turn off LO
        self.LO.set_status(0)

        # Turn off HDAWG
        self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.hdawg_channel) + '/on', 0)


class Sts(TwoToneSpectroscopy):
    """
    Single Tone Spectroscopy for 1 qubit measurements
    """

    def __init__(self,
                 *, x_min, x_max, y_min, y_max,
                 nx_points=None, x_step=None, y_step=None, ny_points=None,
                 hdawg_port: str = '127.0.0.1', hdawg_port1: int = 8004, hdawg_mode: int = 6,
                 hdawg_channel: int = 5, hdawg_device: str = 'dev8210',
                 LO_res_port: str = 'TCPIP0::192.168.180.110::inst0::INSTR',
                 LO_res_set_bandwidth: int = 20, LO_res_set_power: int = -10,
                 LO_res_set_averages=1
                 ):
        """
        :param x_min: x minimum value (int | float)
        :param x_max: x maximum value (int | float)
        :param y_min: y minimum value (int | float)
        :param y_max: y maximum value (int | float)
        :param x_step: x step value (float)
        :param nx_points: x count value (int)
        :param y_step: y step value (float)
        :param ny_points: y count value (int)
        :param hdawg_port: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param hdawg_port1: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param hdawg_mode: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param LO_res_port: resonator LO_res = Znb(LO_res_port)
        :param hdawg_channel: hdawg.setInt('/' + hdawg_device + '/sigouts/' + str(hdawg_channel) + '/on', 1)
        :param hdawg_device: 'dev8210' by default
        :param LO_res_set_bandwidth: base bandwidth (default 20)
        :param LO_res_set_power: base LO_res power (default -10)
        :param LO_res_set_averages: set averages for resonator LO parameter
        """

        super().__init__(x_min=x_min, x_max=x_max, nx_points=nx_points, y_min=y_min, y_max=y_max, ny_points=ny_points,
                         x_step=x_step, y_step=y_step)

        self.ny_points = ny_points if self.y_step is None else len(self.y_list)

        # HDAWG init
        self.hdawg_device = hdawg_device
        self.hdawg_channel = hdawg_channel

        # HDAWG init
        self.hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        hdawgModule = self.hdawg.awgModule()

        # LO connect
        self.LO_res = Znb(LO_res_port)  # resonator

        # set base parameters of LO res
        self.LO_res_set_bandwidth = LO_res_set_bandwidth
        self.LO_res_set_power = LO_res_set_power

        self.LO_res_set_averages = LO_res_set_averages
        self.LO_res.set_averages(LO_res_set_averages)

        pass

    def run_measurements(self, *, sleep=0.0007):

        self.iter_setup(x_key=None, y_key=None,
                        x_min=None, x_max=None, y_min=None, y_max=None)

        # enable channel
        self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.hdawg_channel) + '/on', 1)

        # Set power
        self.LO_res.set_power(self.LO_res_set_power)

        # Set LO parameters
        self.LO_res.set_bandwidth(self.LO_res_set_bandwidth)
        self.LO_res.set_nop(self.ny_points)
        self.LO_res.set_freq_limits(self.y_min, self.y_max)

        freq_len = len(self.y_list)
        try:
            for i in range(len(self.load)):
                if (i == 0) or (self.load[i] != self.load[i - 1]):
                    self.hdawg.setDouble('/' + hdawg_device + '/sigouts/' + str(self.hdawg_channel)
                                         + '/offset', self.load[i])  # current write

                    self.LO_res.set_averages(self.LO_res_set_averages)
                    result = self.LO_res.measure()['S-parameter']

                    for j in range(freq_len):
                        self.write(x=self.load[i],
                                   y=self.y_list[j],
                                   heat=20 * np.log10(abs(result[j]))
                                   )

                timer.sleep(sleep)

        except KeyboardInterrupt:
            if (self.x_raw[-1] == self.x_list[-1]) and (self.y_raw[-1] == self.y_list[-1]):
                pass
            else:
                # drop the last column if interrupt for stable data saving
                self.drop(x=self.x_raw[-1])
            pass

        # channel switch off
        self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.hdawg_channel) + '/on', 0)


class Sts2Q(TwoToneSpectroscopy):
    """
    Single Tone Spectroscopy for 2 qubit measurements
    """

    def __init__(self,
                 *,
                 flux_qubit: str, readout_qubit: str,
                 x_min=None, x_max=None, y_min=None, y_max=None,
                 nx_points=None, x_step=None, y_step=None, ny_points=None,
                 x_min_coupler=None, x_max_coupler=None, x_step_coupler=None, nx_points_coupler=None,
                 x_min_control=None, x_max_control=None, x_step_control=None, nx_points_control=None,
                 target_ch: int = None,
                 control_ch: int = None,
                 coupler_ch: int = None,
                 hdawg_port: str = '127.0.0.1', hdawg_port1: int = 8004, hdawg_mode: int = 6,
                 hdawg_device: str = 'dev8210',
                 LO_res_port: str = 'TCPIP0::192.168.180.110::inst0::INSTR',
                 LO_res_set_bandwidth: int = 20, LO_res_set_power: int = -10,
                 LO_res_set_averages=1
                 ):
        """

        :param flux_qubit: str|list of strings. names of qubits that we drive
        :param readout_qubit: str. name of readout qubit
        :param x_min: min x value of target qubit or base x_min while checking
        :param x_max: max x value of target qubit or base x_max while checking
        :param y_min: min y value of readout qubit
        :param y_max: max y value of readout qubit
        :param nx_points: nx_points value of target qubit or base nx_points while checking
        :param x_step: x_step value of target qubit or base x_step while checking
        :param y_step: y_step value of readout qubit
        :param ny_points: ny_points value of readout qubit
        :param x_min_coupler: min x value of coupler qubit
        :param x_max_coupler: max x value of coupler qubit
        :param x_step_coupler: x_step value of coupler qubit
        :param nx_points_coupler: nx_points value of coupler qubit
        :param x_min_control: min x value of control qubit
        :param x_max_control: max x value of control qubit
        :param x_step_control: x_step value of control qubit
        :param nx_points_control: nx_points value of control qubit
        :param target_ch: target channel
        :param control_ch: control channel
        :param coupler_ch: coupler channel
        :param hdawg_port: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param hdawg_port1: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param hdawg_mode: hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        :param LO_res_port: resonator LO_res = Znb(LO_res_port)
        :param hdawg_channel: hdawg.setInt('/' + hdawg_device + '/sigouts/' + str(hdawg_channel) + '/on', 1)
        :param hdawg_device: 'dev8210' by default
        :param LO_res_set_bandwidth: base bandwidth (default 20)
        :param LO_res_set_power: base LO_res power (default -10)
        :param LO_res_set_averages: set averages for resonator LO parameter
        """

        if (target_ch is not None) and (control_ch is None) and (coupler_ch is None):
            super().__init__(x_min=x_min, x_max=x_max, nx_points=nx_points, y_min=y_min, y_max=y_max,
                             ny_points=ny_points, x_step=x_step, y_step=y_step)
            self.ny_points = ny_points if self.y_step is None else len(self.y_list)
            # channel define
            self.target_ch = target_ch

        elif (coupler_ch is not None) and (control_ch is None) and (target_ch is None):
            super().__init__(x_min=x_min_coupler, x_max=x_max_coupler, nx_points=nx_points_coupler, y_min=y_min,
                             y_max=y_max,
                             ny_points=ny_points, x_step=x_step_coupler, y_step=y_step)
            self.ny_points = ny_points if self.y_step is None else len(self.y_list)
            # channel define
            self.coupler_ch = coupler_ch

        elif (control_ch is not None) and (coupler_ch is None) and (target_ch is None):
            super().__init__(x_min=x_min_control, x_max=x_max_control, nx_points=nx_points_control, y_min=y_min,
                             y_max=y_max, ny_points=ny_points, x_step=x_step_control,
                             y_step=y_step)
            self.ny_points = ny_points if self.y_step is None else len(self.y_list)
            # channel define
            self.control_ch = control_ch

        else:

            if target_ch is not None:
                self.target_ch = target_ch
            if coupler_ch is not None:
                self.coupler_ch = coupler_ch
            if control_ch is not None:
                self.control_ch = control_ch

            super().__init__(x_min=x_min, x_max=x_max, nx_points=nx_points, y_min=y_min,
                             y_max=y_max, ny_points=ny_points, x_step=x_step, y_step=y_step)

            self.ny_points = ny_points if self.y_step is None else len(self.y_list)

        # HDAWG init
        self.hdawg_device = hdawg_device
        self.hdawg = zhinst.ziPython.ziDAQServer(hdawg_port, hdawg_port1, hdawg_mode)
        hdawgModule = self.hdawg.awgModule()

        # LO connect
        self.LO_res = Znb(LO_res_port)  # resonator

        # set base parameters of LO res
        self.LO_res_set_bandwidth = LO_res_set_bandwidth
        self.LO_res_set_power = LO_res_set_power

        self.LO_res_set_averages = LO_res_set_averages
        self.LO_res.set_averages(LO_res_set_averages)

        self.flux_qubit = flux_qubit
        self.readout_qubit = readout_qubit

        self.finished = False
        self.active = False
        self.start_for_fit_LP = (6, 0.02, 0.1, 0)
        self.start_for_fit_HP = (10, 0.2, 0.5, 0)

        self.fit = None
        self.x_offset = None
        pass

    def run_measurements(self, *, sleep=0.0007):

        self.iter_setup(x_key=None, y_key=None,
                        x_min=None, x_max=None, y_min=None, y_max=None)

        self.active = True

        # channel switch on
        if self.target_ch is not None:
            self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.target_ch) + '/on', 1)

        if self.coupler_ch is not None:
            self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.coupler_ch) + '/on', 1)

        if self.control_ch is not None:
            self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.control_ch) + '/on', 1)

        # Set power
        self.LO_res.set_power(self.LO_res_set_power)

        # Set LO parameters
        self.LO_res.set_bandwidth(self.LO_res_set_bandwidth)
        self.LO_res.set_nop(self.ny_points)
        self.LO_res.set_freq_limits(self.y_min, self.y_max)

        freq_len = len(self.y_list)
        try:
            for i in range(len(self.load)):
                if (i == 0) or (self.load[i] != self.load[i - 1]):

                    if self.target_ch is not None:
                        self.hdawg.setDouble('/' + self.hdawg_device + '/sigouts/'
                                             + str(self.target_ch) + '/offset', self.load[i])

                    if self.coupler_ch is not None:
                        self.hdawg.setDouble('/' + self.hdawg_device + '/sigouts/'
                                             + str(self.coupler_ch) + '/offset', self.load[i])

                    if self.control_ch is not None:
                        self.hdawg.setDouble('/' + self.hdawg_device + '/sigouts/'
                                             + str(self.control_ch) + '/offset', self.load[i])

                    self.LO_res.set_averages(self.LO_res_set_averages)
                    result = self.LO_res.measure()['S-parameter']

                    for j in range(freq_len):
                        self.write(x=self.load[i],
                                   y=self.y_list[j],
                                   heat=20 * np.log10(abs(result[j]))
                                   )
                timer.sleep(sleep)

        except KeyboardInterrupt:
            if (self.x_raw[-1] == self.x_list[-1]) and (self.y_raw[-1] == self.y_list[-1]):
                pass
            else:
                # drop the last column if interrupt for stable data saving
                self.drop(x=self.x_raw[-1])
            self.active = False
            pass

        if (self.x_raw[-1] == self.x_list[-1]) and (self.y_raw[-1] == self.y_list[-1]):
            self.finished = True
        else:
            pass

        # channel switch off
        if self.target_ch is not None:
            self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.target_ch) + '/on', 0)

        if self.coupler_ch is not None:
            self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.coupler_ch) + '/on', 0)

        if self.control_ch is not None:
            self.hdawg.setInt('/' + self.hdawg_device + '/sigouts/' + str(self.control_ch) + '/on', 0)

        self.active = False

    def fit_and_offset(self, start, fitted_freqs=None):

        if fitted_freqs is not None:
            fitted_params, cov = curve_fit(_fit_cos, self.x_list, fitted_freqs, start)
        else:
            fitted_freqs = self.fit_curve()['y']
            fitted_params, cov = curve_fit(_fit_cos, self.x_list, fitted_freqs, start)

        A1, A0, omega, teta = fitted_params

        fit = A1 * np.cos(2 * np.pi * omega * self.x_list + teta) + A0
        fit_dict = dict(x=self.x_list, y=fit)
        x_offset = self.x_list[np.argmax(fit)]

        self.fit = fit
        self.x_offset = x_offset

        return fit_dict, x_offset


class Sts2QContainer:

    def __init__(self, *,
                 y_minQ1, y_maxQ1, y_minQ2, y_maxQ2,
                 q1_ch: int,
                 q2_ch: int,
                 coupler_ch: int,
                 x_min=None, x_max=None, nx_points=None, x_step=None,

                 x_minQ1=None, x_maxQ1=None, nx_pointsQ1=None, x_stepQ1=None,
                 ny_pointsQ1=None, y_stepQ1=None,

                 x_minC=None, x_maxC=None, nx_pointsC=None, x_stepC=None,

                 x_minQ2=None, x_maxQ2=None, nx_pointsQ2=None, x_stepQ2=None,
                 ny_pointsQ2=None, y_stepQ2=None,

                 hdawg_port: str = '127.0.0.1', hdawg_port1: int = 8004, hdawg_mode: int = 6,
                 hdawg_device: str = 'dev8210',
                 LO_res_port: str = 'TCPIP0::192.168.180.110::inst0::INSTR',
                 LO_res_set_bandwidth: int = 20, LO_res_set_power: int = -10,
                 LO_res_set_averages=1
                 ):

        if (x_min is not None) and (x_max is not None):

            x_minQ1 = x_min if x_minQ1 is None else x_minQ1
            x_minQ2 = x_min if x_minQ2 is None else x_minQ2
            x_minC = x_min if x_minC is None else x_minC

            x_maxQ1 = x_max if x_maxQ1 is None else x_maxQ1
            x_maxQ2 = x_max if x_maxQ2 is None else x_maxQ2
            x_maxC = x_max if x_maxC is None else x_maxC

            nx_pointsQ1 = nx_points if nx_pointsQ1 is None else nx_pointsQ1
            nx_pointsQ2 = nx_points if nx_pointsQ2 is None else nx_pointsQ2
            nx_pointsC = nx_points if nx_pointsC is None else nx_pointsC

            x_stepQ1 = x_step if x_stepQ1 is None else x_stepQ1
            x_stepQ2 = x_step if x_stepQ2 is None else x_stepQ2
            x_stepC = x_step if x_stepC is None else x_stepC

        else:
            pass

        "Flux on Q1 | Coupler | Q2; Readout - Q1"
        self.Q1 = Sts2Q(x_min=x_minQ1, x_max=x_maxQ1, y_min=y_minQ1, y_max=y_maxQ1,
                        nx_points=nx_pointsQ1, x_step=x_stepQ1, y_step=y_stepQ1, ny_points=ny_pointsQ1,
                        target_ch=q1_ch,
                        readout_qubit='Q1', flux_qubit='Q1',
                        hdawg_port=hdawg_port, hdawg_port1=hdawg_port1, hdawg_mode=hdawg_mode,
                        hdawg_device=hdawg_device,
                        LO_res_port=LO_res_port,
                        LO_res_set_bandwidth=LO_res_set_bandwidth, LO_res_set_power=LO_res_set_power,
                        LO_res_set_averages=LO_res_set_averages)

        self.Q1_Coupler = Sts2Q(x_min_coupler=x_minC, x_max_coupler=x_maxC, y_min=y_minQ1, y_max=y_maxQ1,
                                nx_points_coupler=nx_pointsC, x_step_coupler=x_stepC, y_step=y_stepQ1, ny_points=ny_pointsQ1,
                                coupler_ch=coupler_ch,
                                readout_qubit='Q1', flux_qubit='Coupler',
                                hdawg_port=hdawg_port, hdawg_port1=hdawg_port1, hdawg_mode=hdawg_mode,
                                hdawg_device=hdawg_device,
                                LO_res_port=LO_res_port,
                                LO_res_set_bandwidth=LO_res_set_bandwidth, LO_res_set_power=LO_res_set_power,
                                LO_res_set_averages=LO_res_set_averages)

        self.Q1_Q2 = Sts2Q(x_min_control=x_minQ2, x_max_control=x_maxQ2, y_min=y_minQ1, y_max=y_maxQ1,
                           nx_points_control=nx_pointsQ2, x_step_control=x_stepQ2, y_step=y_stepQ1, ny_points=ny_pointsQ1,
                           control_ch=q2_ch,
                           readout_qubit='Q1', flux_qubit='Q2',
                           hdawg_port=hdawg_port, hdawg_port1=hdawg_port1, hdawg_mode=hdawg_mode,
                           hdawg_device=hdawg_device,
                           LO_res_port=LO_res_port,
                           LO_res_set_bandwidth=LO_res_set_bandwidth, LO_res_set_power=LO_res_set_power,
                           LO_res_set_averages=LO_res_set_averages)

        "Flux on Q1 | Coupler | Q2; Readout - Q2"
        self.Q2 = Sts2Q(x_min=x_minQ2, x_max=x_maxQ2, y_min=y_minQ2, y_max=y_maxQ2,
                        nx_points=nx_pointsQ2, x_step=x_stepQ2, y_step=y_stepQ2, ny_points=ny_pointsQ2,
                        target_ch=q2_ch,
                        readout_qubit='Q2', flux_qubit='Q2',
                        hdawg_port=hdawg_port, hdawg_port1=hdawg_port1, hdawg_mode=hdawg_mode,
                        hdawg_device=hdawg_device,
                        LO_res_port=LO_res_port,
                        LO_res_set_bandwidth=LO_res_set_bandwidth, LO_res_set_power=LO_res_set_power,
                        LO_res_set_averages=LO_res_set_averages)

        self.Q2_Coupler = Sts2Q(x_min_coupler=x_minC, x_max_coupler=x_maxC, y_min=y_minQ2, y_max=y_maxQ2,
                                nx_points_coupler=nx_pointsC, x_step_coupler=x_stepC, y_step=y_stepQ2, ny_points=ny_pointsQ2,
                                coupler_ch=coupler_ch,
                                readout_qubit='Q2', flux_qubit='Coupler',
                                hdawg_port=hdawg_port, hdawg_port1=hdawg_port1, hdawg_mode=hdawg_mode,
                                hdawg_device=hdawg_device,
                                LO_res_port=LO_res_port,
                                LO_res_set_bandwidth=LO_res_set_bandwidth, LO_res_set_power=LO_res_set_power,
                                LO_res_set_averages=LO_res_set_averages)

        self.Q2_Q1 = Sts2Q(x_min_control=x_minQ1, x_max_control=x_maxQ1, y_min=y_minQ2, y_max=y_maxQ2,
                           nx_points_control=nx_pointsQ1, x_step_control=x_stepQ1, y_step=y_stepQ2, ny_points=ny_pointsQ2,
                           control_ch=q1_ch,
                           readout_qubit='Q2', flux_qubit='Q1',
                           hdawg_port=hdawg_port, hdawg_port1=hdawg_port1, hdawg_mode=hdawg_mode,
                           hdawg_device=hdawg_device,
                           LO_res_port=LO_res_port,
                           LO_res_set_bandwidth=LO_res_set_bandwidth, LO_res_set_power=LO_res_set_power,
                           LO_res_set_averages=LO_res_set_averages)

        pass

    @property
    def final_matrix(self):

        # First row
        Q1_offset_base = self.Q1.x_offset if self.Q1.finished else None
        a11 = 1 if self.Q1.finished else None

        Q2_offset = self.Q1_Q2.x_offset if self.Q1_Q2.finished else None
        a12 = Q1_offset_base / Q2_offset if self.Q1_Q2.finished and self.Q1.finished else None

        Q1_coupler_offset = self.Q1_Coupler.x_offset if self.Q1_Coupler.finished else None
        a13 = Q1_offset_base / Q1_coupler_offset if self.Q1_Coupler.finished and self.Q1.finished else None

        # Second row
        Q2_offset_base = self.Q2.x_offset if self.Q2.finished else None
        Q1_offset = self.Q2_Q1.x_offset if self.Q2_Q1.finished else None
        a21 = Q2_offset_base / Q1_offset if self.Q2_Q1.finished and self.Q2.finished else None

        a22 = 1 if self.Q2.finished else None

        Q2_coupler_offset = self.Q2_Coupler.x_offset if self.Q2_Coupler.finished else None
        a23 = Q2_offset_base / Q2_coupler_offset if self.Q2_Coupler.finished and self.Q2.finished else None

        # Third row
        a31 = 0
        a32 = 0
        a33 = 1

        matrix = np.array([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])
        return np.linalg.inv(matrix)


