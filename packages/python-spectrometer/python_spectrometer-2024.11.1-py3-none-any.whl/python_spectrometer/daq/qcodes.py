from __future__ import annotations

import dataclasses
import sys
from types import ModuleType
from typing import Any, Dict, Iterator, Type
from unittest.mock import Mock

from qutil.domains import ContinuousInterval
from qutil.functools import cached_property

from .base import DAQ
from .settings import DAQSettings

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated
try:
    from typing import TypeVar
except ImportError:
    from typing_extensions import TypeVar
try:
    from numpy.typing import NDArray
except ImportError:
    from numpy import ndarray as NDArray
try:
    import qcodes
except ImportError as e:
    raise RuntimeError('These DAQs require qcodes.') from e
else:
    try:
        from qcodes.instrument_drivers.Keysight import Keysight344xxA as _Keysight344xxA_qcodes
    except ImportError:
        # Maybe qcodes < 0.46 and name not available in top-level Keysight module
        from qcodes.instrument_drivers.Keysight.private.Keysight_344xxA_submodules import (
            _Keysight_344xxA as _Keysight344xxA_qcodes
        )
try:
    from qcodes_contrib_drivers.drivers.NationalInstruments import DAQ as ni_daq_qcodes
except ImportError:
    ni_daq_qcodes = Mock(Mock)
try:
    import nidaqmx
except ImportError:
    nidaqmx = Mock()

#: Keysight 344xxA instrument subclass
Keysight344xxAT = TypeVar('Keysight344xxAT', bound=_Keysight344xxA_qcodes)


@dataclasses.dataclass
class Keysight344xxA(DAQ):
    """Generates setup and acquisition functions for a Keysight 344xxA DMM.

    See :class:`~python_spectrometer.core.Spectrometer` for more
    details on usage and
    :class:`~python_spectrometer.daq.settings.DAQSettings` for
    more information on setup parameters.

    Returns
    -------
    setup, acquire : Callable

    """
    dmm: Keysight344xxAT = dataclasses.field()
    """The
    :class:`~qcodes:qcodes.instrument_drivers.Keysight.Keysight34465A` 
    :class:`~qcodes:qcodes.instrument.Instrument` representing the DMM.
    """

    @cached_property
    def DAQSettings(self) -> Type[DAQSettings]:
        class Keysight344xxASettings(DAQSettings):
            DEFAULT_FS = 1 / 3e-4

            @property
            def ALLOWED_FS(this) -> ContinuousInterval[float]:
                # timer_minimum is dynamic (depends on dmm.aperture_time() and others)
                dt_min = self.dmm.aperture_time.vals.min_value
                dt_max = self.dmm.aperture_time.vals.max_value
                return (ContinuousInterval(upper=1 / self.dmm.sample.timer_minimum(),
                                           precision=this.PRECISION)
                        & ContinuousInterval(lower=1 / dt_max, upper=1 / dt_min,
                                             precision=this.PRECISION))

        return Keysight344xxASettings

    def setup(self, **settings) -> Dict[str, Any]:
        """Sets up a Keysight DMM to acquire a timetrace for given parameters."""
        # Set the integration time (automatically selects aperture mode)
        self.dmm.aperture_time(1 / settings.get('fs', self.DAQSettings.DEFAULT_FS))

        # Since self.DAQSettings' bounds for fs dynamically depend on the aperture time, only
        # define actual settings after we set that. For some reason, timetrace_dt does not have the
        # same lower bound as aperture_time.
        # Make sure we use the setter for fs so that bounds are taken into account
        settings = self.DAQSettings(settings)
        settings.fs = 1 / self.dmm.aperture_time()

        self.dmm.timetrace_dt(1 / settings.fs)
        self.dmm.timetrace_npts(settings.n_pts)

        assert settings._isclose(1 / self.dmm.timetrace_dt(), settings['fs'])
        assert settings._isclose(self.dmm.timetrace_npts(), settings['n_pts'])

        return settings.to_consistent_dict()

    def acquire(self, *, n_avg: int, **_) -> Iterator[NDArray]:
        """Executes a measurement and yields the resulting timetrace."""
        for _ in range(n_avg):
            yield self.dmm.timetrace.get()
        return self.dmm.get_idn()


@dataclasses.dataclass
class NationalInstrumentsUSB(DAQ):
    """Handles data acquisition using a NI USB-DAQ.

    Requires the :mod:`nidaqmx:nidaqmx` package.

    See :class:`~python_spectrometer.core.Spectrometer` for
    more details on usage and
    :class:`~python_spectrometer.daq.settings.DAQSettings`
    for more information on setup parameters.

    Examples
    --------
    Use a NI DAQ to convert an analog input to a digital signal::

        from qcodes_contrib_drivers.drivers.NationalInstruments import DAQ
        import nidaqmx
        ni_daq = DAQ.DAQAnalogInputs('ni_daq', 'Dev1',
                                     rate=1, channels={'mychan': 3},
                                     task=nidaqmx.Task(),
                                     samples_to_read=2)
        pyspec_daq = national_instruments_daq(ni_daq)

    """
    ni_daq: ni_daq_qcodes.DAQAnalogInputs = dataclasses.field()
    """The
    :class:`~qcodes_contrib_drivers:qcodes_contrib_drivers.drivers.NationalInstruments.DAQ.DAQAnalogInputs` 
    :class:`~qcodes:qcodes.instrument.Instrument` representing the
    device.
    """

    def __post_init__(self):
        if not isinstance(nidaqmx, ModuleType):
            raise ImportError(
                'This daq requires the nidaqmx package. You can install it by running '
                "'pip install nidaqmx' and downloading the NI-DAQmx software from "
                'https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.htm'
            )
        if not isinstance(ni_daq_qcodes, ModuleType):
            raise ImportError('This daq requires qcodes_contrib_drivers.')

    def setup(self, **settings) -> Dict[str, Any]:
        """Sets up a NI DAQ to acquire a timetrace for given parameters."""
        settings = super().setup(**settings)

        rate = settings['fs']
        samples_to_read = settings['n_pts']

        self.ni_daq.rate = rate
        self.ni_daq.samples_to_read = samples_to_read
        self.ni_daq.metadata.update({'rate': f'{rate} Hz'})
        self.ni_daq.task.timing.cfg_samp_clk_timing(
            rate,
            source=settings.get('clock_src') or '',
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=samples_to_read
        )
        self.ni_daq.task.ai_channels[0].ai_term_cfg = settings.get(
            'terminal_configuration', nidaqmx.constants.TerminalConfiguration.DIFF
        )

        old_param = self.ni_daq.parameters.pop('voltage')
        self.ni_daq.add_parameter(
            name='voltage',
            parameter_class=ni_daq_qcodes.DAQAnalogInputVoltages,
            task=self.ni_daq.task,
            samples_to_read=samples_to_read,
            shape=(old_param.shape[0], samples_to_read),
            timeout=settings.get('timeout', old_param.timeout),
            label='Voltage',
            unit='V'
        )
        return settings

    def acquire(self, *, n_avg: int, **_) -> Iterator[NDArray]:
        """Executes a measurement and yields the resulting timetrace."""
        for _ in range(n_avg):
            yield self.ni_daq.voltage.get().squeeze()
        return self.ni_daq.metadata


class NationalInstrumentsUSB6003(NationalInstrumentsUSB):

    @cached_property
    def DAQSettings(self) -> Type[DAQSettings]:
        class NationalInstrumentsDAQSettings(DAQSettings):
            ALLOWED_FS = ContinuousInterval(lower=18.626450e-3, upper=100e3,
                                            precision=DAQSettings.PRECISION)

        return NationalInstrumentsDAQSettings


@deprecated("Use Keysight344xxA instead")
class keysight_344xxA(Keysight344xxA):
    ...


@deprecated("Use NationalInstrumentsUSB instead")
class national_instruments_daq (NationalInstrumentsUSB):
    ...
