"""general purpose context object"""

from types import SimpleNamespace
from zoneinfo import ZoneInfo
from lotek.lib.logger import log

config = SimpleNamespace()
pac = None
highlight_formatter = None

def update_pac(new_pac=None):
    """Replaces the pac (ZoneInfo) object, making dynamic imports required."""
    global pac  # pylint: disable=global-statement
    if not new_pac:
        pac = ZoneInfo(config.rss.timezone)
    else:
        pac = new_pac


def update_config(new_config):
    """modifies config in place so dynamic import is unnecessary"""
    global config  # pylint: disable=global-statement
    config.__dict__.update(new_config.__dict__)
    update_pac(ZoneInfo(config.rss.timezone))
    # Apply log level from config if available
    log_level = getattr(getattr(config, "lotek", {}), "log_level", "info")
    if log_level:
        import logging

        log.setLevel(getattr(logging, log_level.upper(), logging.INFO))

def update_formatter(formatter):
    """Replaces the context object, dynamic import required"""
    global highlight_formatter
    highlight_formatter = formatter
