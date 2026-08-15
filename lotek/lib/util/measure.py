import time
from lotek.lib.logger import log


def measure(func, *args, stage_name=None):
    """Measure execution time of a function call and prints result to log.debug.
    
    returns (any/None): result of func(*args)"""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    log.debug("%s done in %.2fs", stage_name, elapsed)
    return result
