"""Logger class for Lotek"""
import logging
import sys
from logging import StreamHandler, Formatter

from lotek.lib.colors import green, yellow, red, dim

class LotekLogger(logging.Logger):
    """Custom logger that supports colored output to stdout"""

    def __init__(self, name):
        super().__init__(name)

        # Create stdout handler
        self._stdout_handler = StreamHandler(stream=sys.stdout)
        self._stdout_handler.setFormatter(Formatter(
            '%(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        ))

        # Only add stdout handler if stdout is a TTY (has colors)
        if self._should_use_colors():
            self.addHandler(self._stdout_handler)
            self.setLevel(logging.INFO)

        # Set default color for each level
        self._colors = {
            'INFO': green,
            'WARNING': yellow,
            'ERROR': red,
            'DEBUG': dim,
            'CRITICAL': red,
        }

    def _should_use_colors(self):
        """Check if we should use colors (only when stdout is a TTY)"""
        return sys.stdout.isatty()
    
    def _colorize(self, level, message):
        """Apply color to message based on level"""
        if level in self._colors:
            return self._colors[level](message)
        return message
    
    def info(self, message, *args, **kwargs):
        """Log at INFO level"""
        formatted_msg = message % args if args else message
        message = self._colorize('INFO', formatted_msg)

        self._log(logging.INFO, message, ())
    
    def warning(self, message, *args, **kwargs):
        """Log at WARNING level"""
        formatted_msg = message % args if args else message
        message = self._colorize('WARNING', formatted_msg)
        self._log(logging.WARNING, message, ())
    
    def error(self, message, *args, **kwargs):
        """Log at ERROR level"""
        formatted_msg = message % args if args else message
        message = self._colorize('ERROR', formatted_msg)
        self._log(logging.ERROR, message, ())
    
    def debug(self, message, *args, **kwargs):
        """Log at DEBUG level (disabled by default)"""
        formatted_msg = message % args if args else message
        message = self._colorize('DEBUG', formatted_msg)
        self._log(logging.DEBUG, message, ())
    
    def critical(self, message, *args, **kwargs):
        """Log at CRITICAL level"""
        formatted_msg = message % args if args else message
        message = self._colorize('CRITICAL', formatted_msg)
        self._log(logging.CRITICAL, message, ())
    
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
