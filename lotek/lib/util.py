import time
from lotek.lib.logger import log


def measure(func, *args, stage_name=None):
    """Measure execution time of a function call"""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    log.debug("%.2fs - %s", elapsed, stage_name)
    return result
