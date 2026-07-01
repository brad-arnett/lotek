"""Logger class for Lotek"""
import logging
import sys
from logging import StreamHandler, Formatter

from lotek.lib.colors import green, yellow, red, dim

class LotekLogger(logging.Logger):
    """Custom logger that supports colored output to stdout"""

    def __init__(self, name, level=logging.INFO):
        super().__init__(name)

        # Create stdout handler
        self._stdout_handler = StreamHandler(stream=sys.stdout)
        self._stdout_handler.setFormatter(Formatter(
            '%(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        ))
        self.set_level(level)

    def _should_use_colors(self):
        """Check if we should use colors (only when stdout is a TTY)"""
        return sys.stdout.isatty()

    def info(self, message, *args, **kwargs):
        """Log at INFO level"""
        formatted_msg = message % args if args else message
        self._log(logging.INFO, formatted_msg, ())
    
    def warning(self, message, *args, **kwargs):
        """Log at WARNING level"""
        formatted_msg = message % args if args else message
        self._log(logging.WARNING, formatted_msg, ())
    
    def error(self, message, *args, **kwargs):
        """Log at ERROR level"""
        formatted_msg = message % args if args else message
        self._log(logging.ERROR, formatted_msg, ())
    
    def debug(self, message, *args, **kwargs):
        """Log at DEBUG level (disabled by default)"""
        formatted_msg = message % args if args else message
        self._log(logging.DEBUG, formatted_msg, ())
    
    def critical(self, message, *args, **kwargs):
        """Log at CRITICAL level"""
        formatted_msg = message % args if args else message
        self._log(logging.CRITICAL, formatted_msg, ())
    
    def get_level(self):
        """Return current log level (useful for enabling debug)"""
        return self.level
    
    def set_level(self, level):
        """Set the log level (e.g., logging.DEBUG to enable debug)"""
        self.setLevel(level)
    
    def remove_handler(self):
        """Remove the stdout handler (useful for adding file handlers)"""
        if self._stdout_handler in self.handlers:
            self.removeHandler(self._stdout_handler)
    
    def add_stdout_handler(self):
        """Add stdout handler back if removed"""
        self.addHandler(self._stdout_handler)

# set up singleton logger
log = LotekLogger("main")
