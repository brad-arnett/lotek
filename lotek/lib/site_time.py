"""helper functions for time"""

from datetime import datetime


def now_string(delim="\n"):
    """formatted with the tzone of pac, newline delimited"""
    from lotek.lib.context import pac, config
    return datetime.now(pac).strftime(config.date_format.format) + delim
