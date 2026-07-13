"""helper functions for time"""

from datetime import datetime
from zoneinfo import ZoneInfo

def now_string(config, delim="\n"):
    """formatted with the tzone of pac, newline delimited"""
    pac = ZoneInfo(config.rss.timezone)
    return datetime.now(pac).strftime(config.date_format.format) + delim
