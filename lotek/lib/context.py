"""general purpose context object"""

from zoneinfo import ZoneInfo
from lotek.lib.logger import log

config = None
pac = None


def update_pac(new_pac=None):
    global pac  # pylint: disable=global-statement
    if not new_pac:
        pac = ZoneInfo(config.rss.timezone)
    else:
        pac = new_pac

def update_config(new_config):
    global config  # pylint: disable=global-statement
    config = new_config
    update_pac(ZoneInfo(config.rss.timezone))
    # Apply log level from config if available
    log_level = getattr(getattr(config, 'lotek', {}), 'log_level', 'info')
    if log_level:
        import logging
        log.setLevel(getattr(logging, log_level.upper(), logging.INFO))
