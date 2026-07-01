"""Test the Lotek logger."""

import sys
import io
import logging
import pytest
from unittest.mock import patch, MagicMock

from lotek.lib.logger import LotekLogger
from lotek.lib.colors import green, yellow, red, dim


class TestLotekLoggerInit:
    """Test logger initialization."""

    def test_logger_creation(self):
        """Test that logger can be created with a name."""
        logger = LotekLogger("test_logger")
        assert logger.name == "test_logger"

    def test_logger_name_default(self):
        """Test that logger uses the provided name."""
        logger = LotekLogger("custom_name")
        assert logger.name == "custom_name"

    def test_logger_has_required_methods(self):
        """Test that logger has all required logging methods."""
        logger = LotekLogger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "critical")
        assert hasattr(logger, "get_level")
        assert hasattr(logger, "set_level")
        assert hasattr(logger, "remove_handler")
        assert hasattr(logger, "add_stdout_handler")


class TestLotekLoggerColors:
    """Test logger colorization."""

    def test_colorize_info(self):
        """Test INFO message gets green color."""
        logger = LotekLogger("test")
        result = logger._colorize("INFO", "test message")
        assert isinstance(result, str)

    def test_colorize_warning(self):
        """Test WARNING message gets yellow color."""
        logger = LotekLogger("test")
        result = logger._colorize("WARNING", "test message")
        assert isinstance(result, str)

    def test_colorize_error(self):
        """Test ERROR message gets red color."""
        logger = LotekLogger("test")
        result = logger._colorize("ERROR", "test message")
        assert isinstance(result, str)

    def test_colorize_debug(self):
        """Test DEBUG message gets dim color."""
        logger = LotekLogger("test")
        result = logger._colorize("DEBUG", "test message")
        assert isinstance(result, str)

    def test_colorize_critical(self):
        """Test CRITICAL message gets red color."""
        logger = LotekLogger("test")
        result = logger._colorize("CRITICAL", "test message")
        assert isinstance(result, str)

    def test_colorize_unknown_level(self):
        """Test unknown level returns message unchanged."""
        logger = LotekLogger("test")
        result = logger._colorize("UNKNOWN", "test message")
        assert result == "test message"

    def test_colorize_applies_green_to_info(self):
        """Test INFO gets green color applied."""
        logger = LotekLogger("test")
        result = logger._colorize("INFO", "hello")
        assert result == green("hello")

    def test_colorize_applies_yellow_to_warning(self):
        """Test WARNING gets yellow color applied."""
        logger = LotekLogger("test")
        result = logger._colorize("WARNING", "hello")
        assert result == yellow("hello")

    def test_colorize_applies_red_to_error(self):
        """Test ERROR gets red color applied."""
        logger = LotekLogger("test")
        result = logger._colorize("ERROR", "hello")
        assert result == red("hello")

    def test_colorize_applies_dim_to_debug(self):
        """Test DEBUG gets dim color applied."""
        logger = LotekLogger("test")
        result = logger._colorize("DEBUG", "hello")
        assert result == dim("hello")


class TestLotekLoggerTTY:
    """Test logger TTY detection."""

    def test_should_use_colors_true(self):
        """Test that _should_use_colors returns True when stdout is a TTY."""
        logger = LotekLogger("test")
        with patch.object(sys.stdout, "isatty", return_value=True):
            assert logger._should_use_colors() is True

    def test_should_use_colors_false(self):
        """Test that _should_use_colors returns False when stdout is not a TTY."""
        logger = LotekLogger("test")
        with patch.object(sys.stdout, "isatty", return_value=False):
            assert logger._should_use_colors() is False

    def test_handler_not_added_when_not_tty(self):
        """Test that handler is not added when stdout is not a TTY."""
        logger = LotekLogger("test")
        with patch.object(sys.stdout, "isatty", return_value=False):
            assert logger._stdout_handler not in logger.handlers
            assert len(logger.handlers) == 0

    def test_level_not_changed_when_not_tty(self):
        """Test that level is NOT changed when stdout is not a TTY."""
        logger = LotekLogger("test")
        with patch.object(sys.stdout, "isatty", return_value=False):
            assert logger.level == logging.NOTSET

    def test_handler_added_when_tty(self):
        """Test that handler is added when stdout is a TTY."""
        # Need to patch isatty BEFORE creating the logger
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            assert logger._stdout_handler in logger.handlers
            assert len(logger.handlers) == 1

    def test_level_set_to_info_when_tty(self):
        """Test that level is set to INFO when stdout is a TTY."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            assert logger.level == logging.INFO


class TestLotekLoggerOutputCapture:
    """Test that logging output is captured correctly."""

    @pytest.fixture
    def tty_logger(self):
        """Create a logger with TTY output."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            yield logger

    def test_info_output_format(self, tty_logger):
        """Test that INFO output is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.info("test message")
        result = output.getvalue()
        assert "INFO:" in result
        assert "test message" in result

    def test_warning_output_format(self, tty_logger):
        """Test that WARNING output is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.warning("test message")
        result = output.getvalue()
        assert "WARNING:" in result
        assert "test message" in result

    def test_error_output_format(self, tty_logger):
        """Test that ERROR output is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.error("test message")
        result = output.getvalue()
        assert "ERROR:" in result
        assert "test message" in result

    def test_critical_output_format(self, tty_logger):
        """Test that CRITICAL output is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.critical("test message")
        result = output.getvalue()
        assert "CRITICAL:" in result
        assert "test message" in result


class TestLotekLoggerDebug:
    """Test DEBUG level logging."""

    def test_debug_level_default(self):
        """Test that DEBUG level is disabled by default."""
        logger = LotekLogger("test")
        # Default level should be NOTSET or INFO, not DEBUG
        assert logger.level != logging.DEBUG

    def test_debug_with_level_set(self):
        """Test that debug works when level is set to DEBUG."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            logger.setLevel(logging.DEBUG)
            
            output = io.StringIO()
            logger._stdout_handler.stream = output
            logger.debug("debug message")
            assert "DEBUG:" in output.getvalue()

    def test_debug_output_format(self):
        """Test that DEBUG output is formatted correctly."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            logger.setLevel(logging.DEBUG)
            
            output = io.StringIO()
            logger._stdout_handler.stream = output
            logger.debug("debug message")
            result = output.getvalue()
            assert "DEBUG:" in result
            assert "debug message" in result


class TestLotekLoggerLevelControl:
    """Test logger level control methods."""

    def test_get_level_returns_current_level(self):
        """Test that get_level() returns the current log level."""
        logger = LotekLogger("test")
        level = logger.get_level()
        assert isinstance(level, int)

    def test_set_level_changes_level(self):
        """Test that set_level() changes the log level."""
        logger = LotekLogger("test")
        initial_level = logger.get_level()
        logger.set_level("DEBUG")
        new_level = logger.get_level()
        assert new_level != initial_level

    def test_debug_enabled_with_debug_level(self):
        """Test that debug messages are logged when level is DEBUG."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            logger.setLevel(logging.DEBUG)
            
            output = io.StringIO()
            logger._stdout_handler.stream = output
            logger.debug("debug message")
        assert "DEBUG:" in output.getvalue()


class TestLotekLoggerHandlers:
    """Test logger handler management."""

    @pytest.fixture
    def tty_logger(self):
        """Create a logger with TTY output."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            yield logger

    def test_remove_handler_removes_handler(self, tty_logger):
        """Test that remove_handler() removes the stdout handler."""
        tty_logger.remove_handler()
        assert tty_logger._stdout_handler not in tty_logger.handlers

    def test_remove_handler_noop_when_not_present(self):
        """Test that remove_handler() does nothing if handler is not present."""
        logger = LotekLogger("test")
        logger.remove_handler()  # Should not raise
        assert len(logger.handlers) == 0

    def test_add_stdout_handler_adds_handler(self):
        """Test that add_stdout_handler() adds the stdout handler."""
        logger = LotekLogger("test")
        with patch.object(sys.stdout, "isatty", return_value=False):
            logger.add_stdout_handler()
            assert logger._stdout_handler in logger.handlers

    def test_add_then_remove_handler(self, tty_logger):
        """Test that we can add and remove handlers."""
        tty_logger.remove_handler()
        assert tty_logger._stdout_handler not in tty_logger.handlers
        tty_logger.add_stdout_handler()
        assert tty_logger._stdout_handler in tty_logger.handlers
        tty_logger.remove_handler()
        assert tty_logger._stdout_handler not in tty_logger.handlers


class TestLotekLoggerMessageFormatting:
    """Test logger message formatting."""

    @pytest.fixture
    def tty_logger(self):
        """Create a logger with TTY output."""
        with patch.object(sys.stdout, "isatty", return_value=True):
            logger = LotekLogger("test")
            yield logger

    def test_info_formats_message(self, tty_logger):
        """Test that INFO message is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.info("Hello World")
        result = output.getvalue()
        assert "INFO:" in result
        assert "Hello World" in result

    def test_warning_formats_message(self, tty_logger):
        """Test that WARNING message is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.warning("Hello World")
        result = output.getvalue()
        assert "WARNING:" in result
        assert "Hello World" in result

    def test_error_formats_message(self, tty_logger):
        """Test that ERROR message is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.error("Hello World")
        result = output.getvalue()
        assert "ERROR:" in result
        assert "Hello World" in result

    def test_critical_formats_message(self, tty_logger):
        """Test that CRITICAL message is formatted correctly."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.critical("Hello World")
        result = output.getvalue()
        assert "CRITICAL:" in result
        assert "Hello World" in result

    def test_info_with_args(self, tty_logger):
        """Test that info() supports format arguments."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.info("User %s logged in", "john")
        result = output.getvalue()
        assert "User john logged in" in result

    def test_error_with_args(self, tty_logger):
        """Test that error() supports format arguments."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.error("Connection failed to %s", "server.example.com")
        result = output.getvalue()
        assert "Connection failed to server.example.com" in result

    def test_warning_with_args(self, tty_logger):
        """Test that warning() supports format arguments."""
        output = io.StringIO()
        tty_logger._stdout_handler.stream = output
        tty_logger.warning("Low disk space on %s", "/dev/sda1")
        result = output.getvalue()
        assert "Low disk space on /dev/sda1" in result
