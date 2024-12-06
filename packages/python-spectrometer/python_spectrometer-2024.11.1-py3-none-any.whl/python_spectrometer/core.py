import copy
import inspect
import os
import shelve
import warnings
from datetime import datetime
from pathlib import Path
from pprint import pprint
from queue import Queue
from threading import Thread
from typing import (Any, Callable, Dict, Generator, Iterator, List,
                    Literal, Mapping, Optional, Sequence, Tuple, Union, cast)
from unittest import mock

import dill
import numpy as np
from matplotlib import colors
from qutil import io
from qutil.functools import cached_property, chain, partial
from qutil.itertools import count
from qutil.signal_processing.real_space import Id, welch
from qutil.typecheck import check_literals
from qutil.ui import progressbar

from ._plot_manager import PlotManager
from .daq import settings as daq_settings
from .daq.base import DAQ

_keyT = Union[int, str, Tuple[int, str]]
_pathT = Union[str, os.PathLike]
_styleT = Union[str, os.PathLike, dict]
_styleT = Union[None, _styleT, List[_styleT]]


def _forward_property(cls: type, member: str, attr: str):
    def getter(self):
        return getattr(getattr(self, member), attr)

    def setter(self, val):
        return setattr(getattr(self, member), attr, val)

    return property(getter, setter, doc=getattr(cls, attr).__doc__)


class Spectrometer:
    r"""A spectrometer to acquire and display power spectral densities.

    Spectra are acquired using :meth:`take` and identified by an
    index-comment two-tuple. The data is measured and processed by
    either a user-supplied function or
    :func:`~qutil:qutil.signal_processing.real_space.welch`.

    Parameters
    ----------
    daq : DAQ
        A :class:`.daq.core.DAQ` object handling data acquisition. This
        class abstracts away specifics of how to interact with the
        hardware to implement an interface that is independent of the
        lower-level driver. See the :class:`.DAQ` docstring for more
        information.

        If not given, the instance is read-only and can only be used
        for processing and plotting old data.
    psd_estimator : Callable or kwarg dict
        If callable, a function with signature::

            f(data, **settings) -> (ndarray, ndarray, ndarray)

        that takes the data acquired by the DAQ and the settings
        dictionary and estimates the PSD, returning a tuple of
        (PSD, frequencies, iFFTd data). If dict, a keyword-argument
        dictionary to be passed to
        :func:`~qutil:qutil.signal_processing.real_space.welch` as a PSD
        estimator.

        .. note::

            If a dict, the keyword 'density' will be excluded when
            called since it is always assumed that the ``psd_estimator``
            will return a power spectral density.

    procfn : Callable or sequence of Callable
        A (sequence of) callable with signature::

            f(timetrace, **settings) -> ndarray

        that performs processing steps on the raw timeseries data.
        The function is called with the settings as returned by
        :meth:`.DAQ.setup`. If a sequence, the functions are applied
        from left-to-right, e.g., if ``procfn = [a, b, c]``, then
        it is applied as ``c(b(a(xf, f, **s), f, **s), f, **s)``.
    plot_raw : bool, default False
        Plot the raw spectral data on a secondary y-axis using a
        smaller alpha (more transparent line). Can also be toggled
        dynamically by setting :attr:`plot_raw`.
    plot_timetrace : bool, default False
        Plot the most recent raw timeseries data on a new subplot.
        Can also be toggled dynamically by setting
        :attr:`plot_timetrace`.
    plot_cumulative : bool, default False
        Plot the cumulative data given by

        .. math::
            \int_{f_\mathrm{min}}^f\mathrm{d}f^\prime S(f^\prime)

        on a new subplot. :math:`S(f)` is whatever is plotted in the
        main plot and therefore depends on :attr:`plot_density` and
        :attr:`plot_amplitude`. Can also be toggled dynamically by
        setting :attr:`plot_cumulative`.
    plot_negative_frequencies : bool, default True
        Plot negative frequencies for two-sided spectra (in case the
        time-series data is complex). For ``matplotlib >= 3.6`` an
        ``asinh``, otherwise a linear scale is used. Can also be
        toggled dynamically by setting
        :attr:`plot_negative_frequencies`.
    plot_absolute_frequencies : bool, default True
        For lock-in measurements: plot the physical frequencies at the
        input of the device, not the downconverted ones. This means the
        displayed frequencies are shifted by the demodulation
        frequency, which must be present in the settings under the
        keyword 'freq'. Can also be toggled dynamically by setting
        :attr:`plot_absolute_frequencies`.
    plot_amplitude : bool, default True
        Plot the amplitude spectral density / spectrum (the square root)
        instead of the power. Also applies to the cumulative plot
        (:attr:`plot_cumulative`), in which case that plot
        corresponds to the cumulative mean square instead of the
        root-mean-square (RMS) if plotting the density. Can also be
        toggled dynamically by setting :attr:`plot_amplitude`.

        .. note::
            :attr:`psd_estimator` should always return a power spectral
            density, the conversions concerning this parameter are done
            only when plotting.

    plot_density : bool, default True
        Plot the * spectral density rather than the * spectrum. If
        False and plot_amplitude is True, i.e. if the amplitude spectrum
        is plotted, the height of a peak will give an estimate of the
        RMS amplitude. Can also be toggled dynamically by setting
        :attr:`plot_density`.

        .. note::
            :attr:`psd_estimator` should always return a power spectral
            density, the conversions concerning this parameter are done
            only when plotting.

    plot_cumulative_normalized : bool, default False
        Normalize the cumulative data so that it corresponds to the CDF.
        Can also be toggled dynamically by setting
        :attr:`plot_cumulative_normalized`.
    plot_style : str, Path, dict, list thereof, or None, default 'fast'
        Use a matplotlib style sheet for plotting. All styles available
        are given by :attr:`matplotlib.style.available`. Set to None to
        disable styling and use default parameters. Note that line
        styles in ``prop_cycle`` override style settings.
    plot_update_mode : {'fast', 'always', 'never'}
        Determines how often the event queue of the plot is flushed.

         - 'fast' : queue is only flushed after all plot calls are
           done. Lines might not show upon every average update. By
           experience, whether lines are updated inside a loop depends
           on the DAQ backend. (default)
         - 'always' : forces a flush before and after plot calls are
           done, but slows down the entire plotting by a factor of
           order unity.
         - 'never' : Queue is never flushed explicitly.

        When `threaded_acquisition` is True, this should not need to be
        changed and defaults to never. If not, defaults to 'fast'.
    plot_dB_scale : bool, default False
        Plot data in dB relative to a reference spectrum instead of
        in absolute units. The reference spectrum defaults to the first
        acquired, but can be set using :meth:`set_reference_spectrum`.
    threaded_acquisition : bool, default True
        Acquire data in a separate thread. This keeps the plot window
        responsive while acquisition is running.
    prop_cycle : cycler.Cycler
        A property cycler for styling the plotted lines.
    savepath : str or Path
        Directory where the data is saved. All relative paths, for
        example those given to :meth:`serialize_to_disk`, will be
        referenced to this.
    compress : bool
        Compress the data when saving to disk (using
        :func:`numpy:numpy.savez_compressed`).
    raw_unit : str
        The unit of the raw, unprocessed data returned by
        meth:`DAQ.acquire`.
    processed_unit : str
        The unit of the processed data. Can also be set dynamically by
        setting :attr:`processed_unit` in case it changed when using
        :meth:`reprocess_data`.
    figure_kw, gridspec_kw, subplot_kw, legend_kw : Mappings
        Keyword arguments forwarded to the corresopnding matplotlib
        constructors.

    Examples
    --------
    Perform spectral estimation on simulated data using :mod:`qopt:qopt`
    as backend:

    >>> from pathlib import Path
    >>> from tempfile import mkdtemp
    >>> from python_spectrometer.daq import QoptColoredNoise
    >>> def spectrum(f, A=1e-4, exp=1.5, **_):
    ...     return A/f**exp
    >>> daq = QoptColoredNoise(spectrum)
    >>> spect = Spectrometer(daq, savepath=mkdtemp())
    >>> spect.take('a comment', f_max=2000, A=2e-4)
    >>> spect.print_keys()
    (0, 'a comment')
    >>> spect.take('more comments', df=0.1, f_max=2000)
    >>> spect.print_keys()
    (0, 'a comment')
    (1, 'more comments')

    Hide and show functionality:

    >>> spect.hide(0)
    >>> spect.show('a comment')  # same as spect.show(0)
    >>> spect.drop(1)  # drops the spectrum from cache but leaves the data

    Save/recall functionality:

    >>> spect.serialize_to_disk('foo')
    >>> spect_loaded = Spectrometer.recall_from_disk(
    ...     spect.savepath / 'foo', daq
    ... )
    >>> spect_loaded.print_keys()
    (0, 'a comment')
    >>> spect.print_settings('a comment')
    Settings for key (0, 'a comment'):
    {'A': 0.0002,
     'df': 1.0,
     'f_max': 2000.0,
     'f_min': 1.0,
     'fs': 4000.0,
     'n_avg': 1,
     'n_pts': 12000,
     'n_seg': 5,
     'noverlap': 2000,
     'nperseg': 4000}

    """
    _OLD_PARAMETER_NAMES = {
        'plot_cumulative_power': 'plot_cumulative',
        'plot_cumulative_spectrum': 'plot_cumulative',
        'cumulative_normalized': 'plot_cumulative_normalized',
        'amplitude_spectral_density': 'plot_amplitude'
    }

    @check_literals
    def __init__(self, daq: Optional[DAQ] = None, *,
                 psd_estimator: Optional[Union[Callable, Dict[str, Any]]] = None,
                 procfn: Optional[Union[Callable, Sequence[Callable]]] = None,
                 plot_raw: bool = False, plot_timetrace: bool = False,
                 plot_cumulative: bool = False, plot_negative_frequencies: bool = True,
                 plot_absolute_frequencies: bool = True, plot_amplitude: bool = True,
                 plot_density: bool = True, plot_cumulative_normalized: bool = False,
                 plot_style: _styleT = 'fast',
                 plot_update_mode: Optional[Literal['fast', 'always', 'never']] = None,
                 plot_dB_scale: bool = False, threaded_acquisition: bool = True,
                 purge_raw_data: bool = False, prop_cycle=None, savepath: _pathT = None,
                 relative_paths: bool = True, compress: bool = True, raw_unit: str = 'V',
                 processed_unit: str = 'V', figure_kw: Optional[Mapping] = None,
                 subplot_kw: Optional[Mapping] = None, gridspec_kw: Optional[Mapping] = None,
                 legend_kw: Optional[Mapping] = None):

        self._data: Dict[Tuple[int, str], Dict] = {}
        self._savepath: Optional[Path] = None

        self.daq = daq
        self.procfn = chain(*procfn) if np.iterable(procfn) else chain(procfn or Id)
        self.relative_paths = relative_paths
        if savepath is None:
            savepath = Path.home() / 'python_spectrometer' / datetime.now().strftime('%Y-%m-%d')
        self.savepath = savepath
        self.compress = compress
        self.threaded_acquisition = threaded_acquisition
        if plot_update_mode is None:
            plot_update_mode = 'never' if self.threaded_acquisition else 'fast'
        if purge_raw_data:
            warnings.warn('Enabling purge raw data might break some plotting features!',
                          UserWarning, stacklevel=2)
        self.purge_raw_data = purge_raw_data

        if psd_estimator is None:
            psd_estimator = {}
        if callable(psd_estimator):
            self.psd_estimator = psd_estimator
        elif isinstance(psd_estimator, Mapping):
            self.psd_estimator = partial(welch, **psd_estimator)
        else:
            raise TypeError('psd_estimator should be callable or kwarg dict for welch().')
        uses_windowed_estimator = 'window' in inspect.signature(self.psd_estimator).parameters

        self._plot_manager = PlotManager(self._data, plot_raw, plot_timetrace,
                                         plot_cumulative, plot_negative_frequencies,
                                         plot_absolute_frequencies, plot_amplitude,
                                         plot_density, plot_cumulative_normalized,
                                         plot_style, plot_update_mode, plot_dB_scale,
                                         prop_cycle, raw_unit, processed_unit,
                                         uses_windowed_estimator, figure_kw, subplot_kw,
                                         gridspec_kw, legend_kw)

    # Expose plot properties from plot manager
    _to_expose = ('fig', 'ax', 'ax_raw', 'leg', 'plot_raw', 'plot_timetrace', 'plot_cumulative',
                  'plot_negative_frequencies', 'plot_absolute_frequencies', 'plot_amplitude',
                  'plot_density', 'plot_cumulative_normalized', 'plot_style', 'plot_update_mode',
                  'plot_dB_scale', 'reference_spectrum', 'processed_unit')
    locals().update({attr: _forward_property(PlotManager, '_plot_manager', attr)
                     for attr in _to_expose})

    def __repr__(self) -> str:
        if self.keys():
            return super().__repr__() + ' with keys\n' + self._repr_keys()
        else:
            return super().__repr__()

    def __getitem__(self, key: _keyT) -> Dict[str, Any]:
        return self._data[self._parse_keys(key)[0]]

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterator (yields values instead of keys like a dict)."""
        yield from self.values()

    def __len__(self) -> int:
        return self._data.__len__()

    @property
    def _index(self) -> int:
        """Next available index."""
        known_ix = sorted((ix for ix, *_ in self._data))
        free_ix = (np.diff(known_ix) != 1).nonzero()[0]
        if 0 not in known_ix:
            return 0
        elif free_ix.size:
            return free_ix[0] + 1
        else:
            return len(self._data)

    @cached_property
    def _runfile(self) -> Path:
        return self._get_new_file('files', suffix='txt')

    @cached_property
    def _objfile(self) -> Path:
        return self._get_new_file('object', suffix='')

    @property
    def files(self) -> Generator[str, None, None]:
        """List of all data files."""
        return (str(data['filepath']) for data in self.values())

    @property
    def savepath(self) -> Path:
        """The base path where files are stored on disk."""
        return self._savepath

    @savepath.setter
    def savepath(self, path):
        self._savepath = io.to_global_path(path)

    def _resolve_path(self, file: _pathT) -> Path:
        """Resolve file to a fully qualified path."""
        if not (file := Path(file)).is_absolute():
            file = self.savepath / file
        return io.to_global_path(file)

    def _get_new_file(self, append: str = 'data', comment: str = '', suffix: str = 'npz') -> Path:
        """Obtain a new file."""
        self.savepath.mkdir(parents=True, exist_ok=True)
        comment = _make_filesystem_compatible(comment)
        file = "spectrometer{}_{}{}{}".format('_' + append if append else '',
                                              datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                                              '_' + comment if comment else '',
                                              '.' + suffix if suffix else '')
        if self.relative_paths:
            return Path(file)
        return self.savepath / file

    def _unravel_coi(self, *comment_or_index: _keyT) -> Tuple[_keyT, ...]:
        if len(comment_or_index) == 1:
            if comment_or_index[0] == 'all':
                comment_or_index = tuple(self.keys())
            elif isinstance(comment_or_index[0], slice):
                idx = [ix for ix, _ in self.keys()]
                slc = cast(slice, comment_or_index[0])
                comment_or_index = tuple(ix for ix in range(max(idx) + 1)[slc] if ix in idx)
        return comment_or_index

    def _parse_keys(self, *comment_or_index: _keyT) -> List[Tuple[int, str]]:
        """Get spectrum data for key."""
        parsed = []
        for coi in comment_or_index:
            if coi in self.keys():
                # key a tuple of (int, str)
                parsed.append(coi)
            else:
                # Check if key is either int or str, otherwise raise
                indices, comments = zip(*tuple(self._data))
                try:
                    if isinstance(coi, str):
                        ix = [i for i, elem in enumerate(comments) if elem == coi]
                        if len(ix) == 0:
                            raise ValueError
                        elif len(ix) == 1:
                            ix = ix[0]
                        else:
                            raise KeyError(f"Comment '{coi}' occurs multiple times. Please "
                                           + "specify the index.") from None
                    elif isinstance(coi, int):
                        # Allow for negative indices. Can raise ValueError
                        ix = indices.index(coi if coi >= 0 else len(indices) + coi)
                    else:
                        raise ValueError
                except ValueError:
                    raise KeyError(f'Key {coi} not registered') from None
                parsed.append((indices[ix], comments[ix]))
        return parsed

    def _repr_keys(self, *keys) -> str:
        if not keys:
            keys = self.keys()
        return '\n'.join((str(key) for key in sorted(self.keys()) if key in keys))

    @mock.patch.multiple('numpy.compat.py3k.pickle',
                         Unpickler=dill.Unpickler, Pickler=dill.Pickler)
    def _savefn(self, file: _pathT, **kwargs):
        file = io.check_path_length(self._resolve_path(file))
        if self.compress:
            np.savez_compressed(str(file), **_to_native_types(kwargs))
        else:
            np.savez(str(file), **_to_native_types(kwargs))

    @classmethod
    def _make_kwargs_compatible(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        compatible_kwargs = dict()
        signature = inspect.signature(cls)

        # Replace old param names by new ones ...
        for old, new in cls._OLD_PARAMETER_NAMES.items():
            if old in kwargs:
                if new not in kwargs:
                    kwargs[new] = kwargs.pop(old)
                else:
                    # Don't overwrite in case of clash
                    kwargs.pop(old)

        # And drop all other unknown ones.
        for param, val in kwargs.items():
            if param not in signature.parameters:
                warnings.warn(f'Parameter {param} not supported anymore, dropping', RuntimeWarning)
            else:
                compatible_kwargs[param] = val

        return compatible_kwargs

    def _process_data(self, timetrace_raw, **settings) -> Dict[str, Any]:
        S_raw, f_raw, _ = welch(timetrace_raw, **settings)
        S_processed, f_processed, timetrace_processed = self.psd_estimator(
            self.procfn(np.array(timetrace_raw), **settings),
            **settings
        )
        # if read-only, self.daq is None
        DAQSettings = getattr(self.daq or daq_settings, 'DAQSettings')
        data = dict(timetrace_raw=timetrace_raw,
                    timetrace_processed=timetrace_processed,
                    f_raw=f_raw,
                    f_processed=f_processed,
                    S_raw=S_raw,
                    S_processed=S_processed,
                    settings=DAQSettings(settings))
        return data

    def _handle_fetched(self, fetched_data, key: _keyT, **settings):
        processed_data = self._process_data(fetched_data, **settings)

        # TODO: This could fail if the iterator was empty and processed_data was never assigned
        self._data[key].update(_merge_data_dicts(self._data[key], processed_data))
        self.set_reference_spectrum(self.reference_spectrum)
        self.show(key)

    def _take_threaded(self, iterator: Iterator, progress: bool, key: _keyT, n_avg: int,
                         **settings):
        """Acquire data in a separate thread."""

        def task():
            for _ in progressbar(count(), disable=not progress, total=n_avg,
                                 desc=f'Acquiring {n_avg} spectra with key {key}'):
                try:
                    item = next(iterator)
                except Exception as error:
                    queue.put(error)
                    break
                else:
                    queue.put(item)

        queue = Queue()
        thread = Thread(target=task)
        thread.start()

        sentinel = object()
        fetched_data = sentinel

        while thread.is_alive():
            while queue.empty():
                self.fig.canvas.start_event_loop(20e-3)

            result = queue.get()
            if isinstance(result, StopIteration):
                return result.value
            elif isinstance(result, Exception):
                # Make sure we are left in a reproducible state
                self.drop(key)

                msg = 'Something went wrong during data acquisition'
                if fetched_data is not sentinel:
                    msg = msg + (f'. {self.daq.acquire} last returned the following data:\n '
                                 f'{fetched_data}')

                raise RuntimeError(msg) from result
            else:
                fetched_data = result
                self._handle_fetched(fetched_data, key, n_avg=n_avg, **settings)

    def _take_sequential(self, iterator: Iterator, progress: bool, key: _keyT, n_avg: int,
                         **settings):
        """Acquire data in the main thread."""

        sentinel = object()
        fetched_data = sentinel

        for i in progressbar(count(), disable=not progress, total=n_avg,
                             desc=f'Acquiring {n_avg} spectra with key {key}'):
            try:
                fetched_data = next(iterator)
            except StopIteration as stop:
                return stop.value
            except Exception as error:
                # Make sure we are left in a reproducible state
                self.drop(key)

                msg = 'Something went wrong during data acquisition'
                if fetched_data is not sentinel:
                    msg = msg + (f'. {self.daq.acquire} last returned the following data:\n '
                                 f'{fetched_data}')

                raise RuntimeError(msg) from error
            else:
                self._handle_fetched(fetched_data, key, n_avg=n_avg, **settings)

    def take(self, comment: str = '', progress: bool = True, **settings):
        """Acquire a spectrum with given settings and comment.

        There are default parameter names that manage data acqusition
        settings by way of a dictionary subclass,
        :class:`.daq.settings.DAQSettings`. These are checked for
        consistency at runtime, since it is for example not possible to
        specify :attr:`~.daq.settings.DAQSettings.f_min` to be smaller
        than the frequency resolution
        :attr:`~.daq.settings.DAQSettings.df`. See the
        :class:`~.daq.settings.DAQSettings` docstring for examples; the
        special settings are reproduced below.

        Parameters
        ----------
        comment : str
            An explanatory comment that helps identify the spectrum.
        progress : bool
            Show a progressbar for the outer repetitions of data acqusition.
            Default True.
        **settings
            Keyword argument settings for the data acquisition and
            possibly data processing using :attr:`procfn` or
            :attr:`fourier_procfn`.
        """
        if not isinstance(self.daq, DAQ):
            raise ReadonlyError('Cannot take new data since no DAQ backend given')

        if (key := (self._index, comment)) in self._data:
            raise KeyError(f'Key {key} already exists. Choose a different comment.')

        # Drop density from settings so that self.psd_estimator will always return a PSD
        if 'density' in settings:
            settings.pop('density')

        settings = self.daq.DAQSettings(self.daq.setup(**settings))
        filepath = self._get_new_file(comment=comment)
        self._data[key] = {'settings': settings, 'comment': comment, 'filepath': filepath,
                           'timestamp': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}
        self._plot_manager.add_new_line_entry(key)

        iterator = self.daq.acquire(**settings)

        if self.threaded_acquisition:
            measurement_metadata = self._take_threaded(iterator, progress, key, **settings)
        else:
            measurement_metadata = self._take_sequential(iterator, progress, key, **settings)

        self._data[key].update(measurement_metadata=measurement_metadata)
        if self.purge_raw_data:
            del self._data[key]['timetrace_raw']
            del self._data[key]['timetrace_processed']
            del self._data[key]['f_raw']
            del self._data[key]['S_raw']
            self._data[key]['S_processed'] = np.mean(self._data[key]['S_processed'], axis=0)[None]

        self._savefn(filepath, **self._data[key])

    take.__doc__ = (take.__doc__.replace(8*' ', '')
                    + '\n\nDAQ Parameters'
                    + '\n==============\n'
                    + '\n'.join((f'{key} : {val}' for key, val in daq_settings._doc_.items())))

    def drop(self, *comment_or_index: _keyT, update_figure: bool = True):
        """Delete a spectrum from cache and plot.

        Parameters
        ----------
        *comment_or_index : int | str | (int, str)
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys.
        update_figure : bool, default True
            Update the figure. Only used internally.

        See Also
        --------
        :meth:`hide`
        :meth:`show`

        Examples
        --------
        The following are equivalent for a :class:`Spectrometer` with
        keys ``[(0, 'a'), (1, 'b')]``::

            spect.drop(0)
            spect.drop('a')
            spect.drop(-2)
            spect.drop((0, 'a'))

        Multiple spectra can be dropped at the same time::

            spect.drop(0, (1, 'b'))

        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                self._plot_manager.destroy_lines(keys=[key])
                self._plot_manager.drop_lines(key)
                del self._data[key]
                if key == self.reference_spectrum:
                    if self:
                        self._plot_manager._reference_spectrum = list(self.keys())[0]
                    else:
                        self._plot_manager._reference_spectrum = None
        finally:
            if update_figure:
                with self._plot_manager.plot_context:
                    self._plot_manager.update_figure()

    def delete(self, *comment_or_index: _keyT):
        """Delete the data of a spectrum saved on disk and drop it
        from cache.

        .. warning::
            This deletes data from disk!

        Parameters
        ----------
        *comment_or_index : int | str | (int, str)
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys.

        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                file = self[key]['filepath']
                if not file.is_absolute():
                    file = self.savepath / file
                if io.query_yes_no(f'Really delete file {file}?', default='no'):
                    self.drop(key, update_figure=False)
                    os.remove(file)
        finally:
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()

    def hide(self, *comment_or_index: _keyT):
        """Hide a spectrum in the plot.

        Parameters
        ----------
        *comment_or_index : int | str | (int, str) | slice | 'all'
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys. Can also be 'all', which hides
            all registered spectra.

        See Also
        --------
        :meth:`drop`
        :meth:`show`

        Examples
        --------
        The following are equivalent for a :class:`Spectrometer` with
        keys ``[(0, 'a'), (1, 'b')]``::

            spect.hide(0)
            spect.hide('a')
            spect.hide(-2)
            spect.hide((0, 'a'))

        Multiple spectra can be hidden at the same time::

            spect.hide(0, (1, 'b'))

        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                self._plot_manager.destroy_lines(keys=[key])
                self._plot_manager.update_line_attrs(self._plot_manager.plots_to_draw,
                                                     self._plot_manager.lines_to_draw,
                                                     [key], stale=False, hidden=True)
        finally:
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()

    def show(self, *comment_or_index: _keyT, color: Optional[Union[str, List[str]]] = None):
        """Show a spectrum in the plot.

        Parameters
        ----------
        *comment_or_index : int | str | (int, str) | slice | 'all'
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys. Can also be 'all', which shows
            all registered spectra.
        color: str or list[str]
            A valid matplotlib color to override the default color for
            this key.

        See Also
        --------
        :meth:`drop`
        :meth:`hide`

        Examples
        --------
        The following are equivalent for a :class:`Spectrometer` with
        keys ``[(0, 'a'), (1, 'b')]``::

            spect.show(0)
            spect.show('a')
            spect.show(-2)
            spect.show((0, 'a'))

        Multiple spectra can be shown at the same time::

            spect.show(0, (1, 'b'))

        You can override the default color for the spectrum::

            spect.show(0, color='pink')
            spect.show(0, 1, color=['k', 'r'])

        """
        # Need to unravel 'all' or slice for colors below
        comment_or_index = self._unravel_coi(*comment_or_index)

        if color is not None:
            if colors.is_color_like(color):
                color = [color]
            assert len(color) == len(comment_or_index), 'Need as many colors as there are keys'
        else:
            color = [None]*len(comment_or_index)

        try:
            for key, col in zip(self._parse_keys(*comment_or_index), color):
                # Color kwarg needs to be set for all plot and line types
                # (also the ones not currently shown)
                self._plot_manager.update_line_attrs(keys=[key], color=col)
                self._plot_manager.update_line_attrs(self._plot_manager.plots_to_draw,
                                                     self._plot_manager.lines_to_draw,
                                                     [key], stale=True, hidden=False)
        finally:
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()

    def reprocess_data(self,
                       *comment_or_index: _keyT,
                       save: Literal[False, True, 'overwrite'] = False,
                       processed_unit: Optional[str] = None,
                       **new_settings):
        """Repeat data processing using updated settings.

        .. warning::
            This can change data saved on disk!

        Parameters
        ----------
        *comment_or_index : int | str | (int, str) | slice | 'all'
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys. Can also be 'all', which processes
            all registered spectra.
        save : bool or 'overwrite', default False
            Save the processed data to a new or overwrite the old file.
        processed_unit : str, optional
            A string for the new unit if it changes.
        **new_settings
            Updated keyword argument settings for data processing using
            :attr:`procfn` or :attr:`fourier_procfn`. Previous settings
            are used for those not provided here.
        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                data = self._data[key]
                data.update(self._process_data(self._data[key]['timetrace_raw'],
                                               **{**data['settings'], **new_settings}))

                if save:
                    if save == 'overwrite':
                        data['filepath'] = io.query_overwrite(data['filepath'])
                    else:
                        data['filepath'] = self._get_new_file(comment=data['comment'])
                    self._savefn(data['filepath'], **data)

                self._data[key] = data
                self._plot_manager.update_line_attrs(self._plot_manager.plots_to_draw,
                                                     self._plot_manager.lines_to_draw,
                                                     keys=[key], stale=True)
        finally:
            if processed_unit is not None:
                self._plot_manager.processed_unit = str(processed_unit)
                self._plot_manager.setup_figure()
            else:
                with self._plot_manager.plot_context:
                    self._plot_manager.update_figure()

    def set_reference_spectrum(self, comment_or_index: Optional[_keyT] = None):
        """Set the spectrum to be taken as a reference for the dB scale.

        Applies only if :attr:`plot_dB_scale` is True."""
        # Cannot implement this as a setter for the reference_spectrum propert
        # since we need the _parse_keys method of Spectrometer.
        if comment_or_index is None:
            # Default for no data
            if self._data:
                comment_or_index = 0
            else:
                return
        key = self._parse_keys(comment_or_index)[0]
        if key != self.reference_spectrum:
            self._plot_manager._reference_spectrum = key
            if self.plot_dB_scale:
                self._plot_manager.update_line_attrs(['main', 'cumulative'],
                                                     self._plot_manager.lines_to_draw,
                                                     stale=True)
                self._plot_manager.setup_figure()

    @staticmethod
    def update_metadata(file: _pathT, *,
                        delete_old_file: bool = False,
                        new_comment: Optional[str] = None,
                        new_settings: Optional[Mapping[str, Any]] = None,
                        new_savepath: Union[Literal[False], _pathT] = False,
                        relative_paths: bool = True,
                        compress: bool = True):
        """Update the metadata of a previously acquired spectrum and
        write it to disk.

        .. warning::
            This can change data saved on disk!

        Parameters
        ----------
        file: PathLike
            The data file to modify.
        delete_old_file : bool
            Rename the file on disk according to the updated comment.
            If false, a new file is written and the old retained.
            Default: False.

            .. note::
                The new file will have the same timestamp but possibly
                a different comment and therefore filename. Thus, any
                old serialization files will have dead filename links
                generated by :meth:`save_run` and you should
                re-serialize the object.

        new_comment : str
            A new comment replacing the old one.
        new_settings : Mapping[str, Any]
            New (metadata) settings to add to/replace existing ones.

            .. warning::
                This might overwrite settings used for spectral
                estimation. In some cases, it might be better to delete
                the previous spectrum from disk and acquire a new one.

        new_savepath : False | PathLike, default: False
            Use this object's savepath or a specified one instead of
            the one stored in the file. Helpful for handling data
            that has been moved to a different system in case absolute
            paths were used.
        relative_paths: bool
            Use relative or absolute file paths.
        compress : bool
            Compress the data.
        """
        data = _load_spectrum(oldfile := io.to_global_path(file).with_suffix('.npz'))
        backup = {'comment': copy.deepcopy(data['comment']),
                  'settings': copy.deepcopy(data['settings'])}

        if new_savepath is False:
            savepath = oldfile.parent
        else:
            savepath = Path(cast(_pathT, new_savepath))
        if new_comment is not None:
            data['comment'] = new_comment
        if new_settings is not None:
            data['settings'].update(new_settings)
        newfile = (
            # trunk and timestamp parts of the filename
            oldfile.stem[:37]
            # new comment tail
            + (('_' + _make_filesystem_compatible(data['comment'])) if data['comment'] else '')
        )
        data['filepath'] = newfile if relative_paths else savepath / newfile

        newfile = io.query_overwrite(io.check_path_length(savepath / newfile))
        if compress:
            np.savez_compressed(savepath / newfile, **_to_native_types(data))
        else:
            np.savez(savepath / newfile, **_to_native_types(data))

        if newfile == oldfile:
            # Already 'deleted' (overwrote) the old file
            return
        if delete_old_file and io.query_yes_no(f"Really delete file {file}?", default='no'):
            os.remove(file)

    def save_run(self, file: Optional[_pathT] = None, verbose: bool = False) -> Path:
        """Saves the names of all data files to a text file."""
        if file := self._resolve_path(file):
            file = file.with_stem(file.stem + '_files').with_suffix('.txt')
        else:
            file = self._runfile

        file = io.check_path_length(file)
        file.write_text('\n'.join(self.files))

        if verbose:
            print(f'Wrote filenames to {file}.')

        if self.relative_paths:
            return file.relative_to(self.savepath)
        return file

    @mock.patch.multiple('shelve', Unpickler=dill.Unpickler, Pickler=dill.Pickler)
    def serialize_to_disk(self, file: Optional[_pathT] = None, protocol: int = -1,
                          verbose: bool = False):
        """Serialize the Spectrometer object to disk.

        Parameters
        ----------
        file : str | Path
            Where to save the data. Defaults to the same directory where
            also the spectral data is saved.
        protocol : int
            The pickle protocol to use.
        verbose : bool
            Print some progress updates.

        See Also
        --------
        :meth:`recall_from_disk`
        """
        if file is None:
            file = self._objfile
        file = io.check_path_length(
            io.query_overwrite(_resolve_shelve_file(self._resolve_path(file)))
        ).with_suffix('')

        spectrometer_attrs = ['psd_estimator', 'procfn', 'savepath', 'relative_paths',
                              'plot_raw', 'plot_timetrace', 'plot_cumulative',
                              'plot_negative_frequencies', 'plot_absolute_frequencies',
                              'plot_amplitude', 'plot_density', 'plot_cumulative_normalized',
                              'plot_style', 'plot_update_mode', 'plot_dB_scale', 'compress']
        plot_manager_attrs = ['reference_spectrum', 'prop_cycle', 'raw_unit', 'processed_unit']
        with shelve.open(str(file), protocol=protocol) as db:
            # Constructor args
            for attr in spectrometer_attrs:
                try:
                    db[attr] = getattr(self, attr)
                except AttributeError:
                    pass
            for attr in plot_manager_attrs:
                try:
                    db[attr] = getattr(self._plot_manager, attr)
                except AttributeError:
                    pass
            # Write a text file with the locations of all data files
            db['runfile'] = self.save_run(file, verbose=verbose)
        if verbose:
            print(f'Wrote object data to {file}')

    @classmethod
    @mock.patch.multiple('shelve', Unpickler=dill.Unpickler, Pickler=dill.Pickler)
    def recall_from_disk(cls, file: _pathT, daq: Optional[DAQ] = None, *,
                         reprocess_data: bool = False, **new_settings):
        """Restore a Spectrometer object from disk.

        Parameters
        ----------
        file : str | Path
            The saved file.
        daq : DAQ
            The :class:`.DAQ` instance that sets up and executes data
            acquisition (see also the class constructor).

            If not given, the instance is read-only and can only be used
            for processing and plotting old data.
        reprocess_data : bool
            Redo the processing steps using this object's :attr:`procfn`
            and :attr:`psd_estimator`. Default: False.

        See Also
        --------
        :meth:`serialize_to_disk`
        """

        if not (file := _resolve_shelve_file(io.to_global_path(file))).exists():
            raise FileNotFoundError(f'File {file} does not exist!')
        with shelve.open(str(file.with_suffix(''))) as db:
            if not db:
                raise FileNotFoundError(f'File {file} is empty!')
            try:
                kwargs = dict(**db)
            except TypeError:
                # Weirdly, if a serialized function object does not exist in the
                # namespace, a TypeError is raised instead of complaining about
                # said object. Therefore, go through the db one-by-one to trigger
                # the error on the object actually causing problems
                kwargs = dict()
                for key, val in db.items():
                    kwargs[key] = val

            if not (runfile := kwargs.pop('runfile')).is_absolute():
                runfile = kwargs['savepath'] / runfile
            spectrum_files = np.array(io.to_global_path(runfile).read_text().split('\n'))

        # Need to treat reference_spectrum separately since it is not a
        # Spectrometer but a _PlotManager attribute.
        reference_spectrum = kwargs.pop('reference_spectrum', None)

        spectrometer = cls(daq=daq, **cls._make_kwargs_compatible(kwargs))

        # Then restore the data
        keys = []
        for i, file in enumerate(progressbar(spectrum_files, desc='Loading files')):
            try:
                if spectrometer.relative_paths:
                    file = spectrometer.savepath / file
                keys.append(spectrometer.add_spectrum_from_file(file, show=False,
                                                                reprocess_data=reprocess_data,
                                                                **new_settings))
            except FileNotFoundError:
                print(f'Could not retrieve file {file}. Skipping.')

        spectrometer.set_reference_spectrum(reference_spectrum)
        # Show all at once to save drawing time
        spectrometer.show(*keys)
        return spectrometer

    def add_spectrum_from_file(self, file: _pathT, show: bool = True, color: Optional[str] = None,
                               reprocess_data: bool = False, **new_settings) -> Tuple[int, str]:
        """Load data from disk and display it in the current figure.

        Parameters
        ----------
        file : str | os.PathLike
            The file to be loaded.
        show : bool
            Show the added spectrum in the plot.
        color : str
            A custom color to be used for the spectrum.
        reprocess_data : bool
            Redo the processing steps using this object's :attr:`procfn`
            and :attr:`psd_estimator`. Default: False.
        **new_settings
            New settings to use for reprocessing the data.

        Returns
        -------
        key : Tuple[int, str]
            The key assigned to the new spectrum data.

        """
        data = _load_spectrum(self._resolve_path(file).with_suffix('.npz'))

        if reprocess_data:
            data.update(self._process_data(data['timetrace_raw'],
                                           **{**data['settings'], **new_settings}))

        key = (self._index, data['comment'])
        self._data[key] = data
        self._plot_manager.add_new_line_entry(key)
        if show:
            self.show(key, color=color)
        else:
            # Sets flags correctly
            self.hide(key)
        return key

    def print_settings(self, comment_or_index: _keyT):
        """Convenience method to pretty-print the settings for a
        previously acquired spectrum."""
        key = self._parse_keys(comment_or_index)[0]
        print(f'Settings for key {key}:')
        pprint(self[key]['settings'], width=120)

    def print_keys(self, *comment_or_index: _keyT):
        """Prints the registered (index, comment) tuples."""
        print(self._repr_keys(*self._parse_keys(*comment_or_index)))

    def keys(self) -> List[Tuple[int, str]]:
        """Registered keys (sorted)."""
        return sorted(self._data.keys())

    def values(self) -> List[Dict[str, Any]]:
        """Registered data (sorted by keys)."""
        return [value for _, value in sorted(self._data.items())]

    def items(self) -> List[Tuple[Tuple[int, str], Dict[str, Any]]]:
        """Registered (key, data) tuples (sorted by keys)."""
        return [(key, value) for key, value in sorted(self._data.items())]


def _load_spectrum(file: _pathT) -> Dict[str, Any]:
    """Loads data from a spectrometer run."""
    class monkey_patched_io:
        # Wrap around data saved during JanewayPath folly
        class JanewayWindowsPath(os.PathLike):
            def __init__(self, *args):
                self.path = Path(*args)

            def __fspath__(self):
                return str(self.path)

        def __enter__(self):
            setattr(io, 'JanewayWindowsPath', self.JanewayWindowsPath)

        def __exit__(self, exc_type, exc_val, exc_tb):
            delattr(io, 'JanewayWindowsPath')

    with np.load(file, allow_pickle=True) as fp, monkey_patched_io():
        data = {}
        for key, val in fp.items():
            try:
                # Squeeze singleton arrays into native Python data type
                data[key] = val.item()
            except ValueError:
                data[key] = val
            except Exception as err:
                raise RuntimeError(f'Encountered unhandled object in file {file}') from err

    return _from_native_types(data)


def _make_filesystem_compatible(comment: str) -> str:
    for old, new in zip((' ', '/', '.', ':', '\\', '|', '*', '?', '<', '>'),
                        ('_', '_', '-', '-', '_', '_', '_', '_', '_', '_')):
        comment = comment.replace(old, new)
    return comment


def _merge_data_dicts(data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    for key, val in new_data.items():
        if key == 'settings' or key.startswith('f'):
            # Only store single copy of frequency arrays / settings
            data[key] = val
        else:
            if key not in data:
                data[key] = []
            # Append new data arrays to list of existing
            data[key].append(val)
    return data


def _resolve_shelve_file(path: Path) -> Path:
    # shelve writes a single file without suffix or three files with suffixes
    # .dat, .dir, .bak depending on the dbm implementation available.
    if (p := path.with_suffix('')).is_file():
        return p
    if (p := path.with_suffix('.dat')).is_file():
        return p
    return path


def _to_native_types(data: Dict[str, Any]) -> Dict[str, Any]:
    """Converts custom types to native Python or NumPy types."""
    data_as_native_types = dict()
    for key, val in data.items():
        if isinstance(val, Path):
            # Cannot instantiate WindowsPaths on Posix and vice versa
            data_as_native_types[key] = str(val)
        elif isinstance(val, daq_settings.DAQSettings):
            # DAQSettings might not be available on system loading the
            # data, so unravel to consistent Python dict.
            data_as_native_types[key] = val.to_consistent_dict()
        else:
            data_as_native_types[key] = val
    return data_as_native_types


def _from_native_types(data: Dict[str, Any]) -> Dict[str, Any]:
    """Inverts :func:`_to_native_types`."""
    for key, val in data.items():
        if key == 'filepath':
            data[key] = Path(data[key])
        elif key == 'settings':
            data[key] = daq_settings.DAQSettings(data[key])
        else:
            data[key] = val
    return data


class ReadonlyError(Exception):
    """Indicates a :class:`Spectrometer` object is read-only."""
    pass
