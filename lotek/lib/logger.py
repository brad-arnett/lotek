"""logger for lotek"""

import logging
import sys
from logging import INFO, WARNING, ERROR, DEBUG, CRITICAL


class LotekLogger(logging.Logger):
    """Custom logger that outputs to stderr with formatted level prefix."""

    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.INFO)

        # Create stderr handler (logs should go to stderr)
        self._stderr_handler = logging.StreamHandler(stream=sys.stderr)
        self._stderr_handler.setFormatter(
            logging.Formatter("%(levelname)s: %(message)s")
        )
        self.addHandler(self._stderr_handler)

    def info(self, message, *args, **kwargs):
        """Log at INFO level"""
        self._log(INFO, message, args if args else (), **kwargs)

    def warning(self, message, *args, **kwargs):
        """Log at WARNING level"""
        self._log(WARNING, message, args if args else (), **kwargs)

    def error(self, message, *args, **kwargs):
        """Log at ERROR level"""
        self._log(ERROR, message, args if args else (), **kwargs)

    def debug(self, message, *args, **kwargs):
        """Log at DEBUG level (disabled by default)"""
        self._log(DEBUG, message, args if args else (), **kwargs)

    def critical(self, message, *args, **kwargs):
        """Log at CRITICAL level"""
        self._log(CRITICAL, message, args if args else (), **kwargs)

    def exc(self, e):
        """Log an exception"""
        from traceback import format_exc
        self.debug(format_exc())

    def get_level(self):
        """Return current log level (useful for enabling debug)"""
        return self.level

    def set_level(self, level):
        """Set the log level (e.g., logging.DEBUG to enable debug)"""
        self.setLevel(level)

    def remove_handler(self):
        """Remove the stdout handler (useful for adding file handlers)"""
        if self._stderr_handler in self.handlers:
            self.removeHandler(self._stderr_handler)

    def add_stdout_handler(self):
        """Add stdout handler back if removed"""
        self.addHandler(self._stderr_handler)


# set up singleton logger
log = LotekLogger("lotek")
