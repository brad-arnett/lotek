"""helper functions for time"""

from datetime import datetime
from lotek.lib.site_config import pac, config


def now_string(delim="\n"):
    """formatted with the tzone of pac, newline delimited"""
    return datetime.now(pac).strftime(config.date_format.format) + delim
