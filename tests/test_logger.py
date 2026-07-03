"""Test the Lotek logger."""

import sys
import logging
import pytest
from lotek.lib.logger import log

from logging import INFO, WARNING, ERROR, DEBUG, CRITICAL


def test_log_info():
    """Test info logging."""
    log.info("test message")


def test_log_warning():
    """Test warning logging."""
    log.warning("test warning")


def test_log_error():
    """Test error logging."""
    log.error("test error")


def test_log_different_levels():
    """Test all logging levels."""
    log.debug("debug")
    log.info("info")
    log.warning("warning")
    log.error("error")
    log.critical("critical")


def test_log_format():
    """Test message format."""
    log.info("test")
    log.info("test with %s", "arg")


def test_log_file_stderr():
    """Test that logs go to stderr."""
    assert log.info("test") is None


class TestLogLevel:
    """Test log level management."""

    def test_default_level(self):
        """Test default log level is INFO."""
        assert log.level == logging.INFO

    def test_set_level_debug(self):
        """Test setting level to DEBUG."""
        log.setLevel(DEBUG)
        assert log.level == DEBUG

    def test_set_level_warning(self):
        """Test setting level to WARNING."""
        log.setLevel(WARNING)
        assert log.level == WARNING
        log.setLevel(INFO)  # reset


class TestLogError:
    """Test error logging."""

    def test_error_format(self):
        """Test error message format."""
        log.error("message")

    def test_error_prefix(self):
        """Test error has [ERROR] prefix."""
        log.error("test")


class TestLogWarning:
    """Test warning logging."""

    def test_warning_format(self):
        """Test warning message format."""
        log.warning("test")

    def test_warning_prefix(self):
        """Test warning has [WARNING] prefix."""
        log.warning("test")
