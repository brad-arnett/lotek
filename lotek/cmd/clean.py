import shutil
from lotek.lib.logger import log


def cmd_clean(dirs):
    """Clean the output directory"""
    output = dirs.OUTPUT
    if output.exists():
        shutil.rmtree(output)
        log.info("Removed output/")
    return 0
