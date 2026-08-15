import shutil
from lotek.lib.util.logger import log


def cmd_clean(dirs, _config):
    """Clean the output directory and warp cache"""
    output = dirs.OUTPUT
    if output.exists():
        shutil.rmtree(output)
        log.info("Removed output/")
    warp = dirs.LOTEK_WARP
    if warp.exists():
        shutil.rmtree(warp)
        log.info("Removed .lotek/warp/")
    return 0
