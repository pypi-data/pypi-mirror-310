import os
import gc
import logging
import psutil

# Default formats and level names
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)-38s: %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S'
)
LEVELS = ['CRITICAL', 'WARNING', 'INFO', 'DEBUG']
LOGGER = logging.getLogger('raynest.utils')


class _Handler(logging.Handler):

    def __init__(self, verbose=0, **kwargs):
        super().__init__(**kwargs)
        self.set_verbosity(verbose)
        self.setFormatter(FORMATTER)

    def get_verbosity(self):
        return self._verbose

    def set_verbosity(self, verbose):
        LOGGER.warning('Setting verbosity to {}'.format(verbose))
        self._verbose = verbose
        self.setLevel(LEVELS[verbose])


class StreamHandler(_Handler, logging.StreamHandler):
    def __init__(self, verbose=0, **kwargs):
        super().__init__(verbose=verbose, **kwargs)


class FileHandler(_Handler, logging.FileHandler):
    def __init__(self, filename, verbose=0, **kwargs):
        super().__init__(filename=filename, verbose=verbose, **kwargs)


class LogFile:
    """
    Context manager for file logging. It logs everything from `logger`
    in some file at a given `filename`.

    Parameters
    ----------
    filename : str
        Filename under which to save the log.

    verbose : int, optional
        Logging level verbosity 0='CRITICAL' 1='WARNING' 2='INFO' 3='DEBUG'.

    loggername : str, optional
        Name of the logger to send to file at `path`. Default is `'raynest'` so
        all raynest logs are recorded. E.g. specify `'raynest.raynest'` to only
        record logs from the `raynest.py` module.

    Attributes
    ----------
    handler : logging.FileHandler
        File handler object.

    Examples
    --------
    ```python
    from raynest.utils import LogFile

    with LogFile('example.log') as flog:
        # Do some stuff here and it will be logged to 'example.log'
        ...

    # Do some stuff here and it won't be logged to 'example.log'

    with flog:
        # Do some stuff here and it will be logged to 'example.log'
        ...
    ```

    """

    def __init__(self, filename, verbose=0, loggername='raynest'):
        self._filename = filename
        self._verbose = verbose
        self._logger = logging.getLogger(loggername)
        self.handler = None

    def open(self):
        self.handler = FileHandler(self._filename, verbose=self._verbose)
        self._logger.addHandler(self.handler)

    def close(self):
        self._logger.removeHandler(self.handler)
        self.handler.close()
        self.handler = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

def auto_garbage_collect(pct=80.0):
    """
    auto_garbage_collection - Call the garbage collection if memory used is greater than 80% of total available memory.
                              This is called to deal with an issue in Ray not freeing up used memory.

        pct - Default value of 80%.  Amount of memory in use that triggers the garbage collection call.
    """
    if psutil.virtual_memory().percent >= pct:
        gc.collect()
    return
