"""build.py cmd"""
import lotek.lib.build as build_module
from lotek.lib.logger import log
from lotek.lib.util.measure import measure

def cmd_build(dirs, config):
    """build.py cmd_build"""
    try:
        return measure(build_module.build, dirs, config, stage_name="build")
    except Exception as e:
        log.error("Build failed: %s", e)
        import traceback
        traceback.print_exc()
        return 1
