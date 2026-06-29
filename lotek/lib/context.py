"""general purpose context object"""

from zoneinfo import ZoneInfo

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
