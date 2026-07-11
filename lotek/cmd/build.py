from lotek.lib.logger import log
import lotek.build as build_module

def cmd_build(dirs):
    try:
        build_module.build(dirs)
        return 0
    except Exception as e:
        log.error("Build failed: %s", e)
        import traceback
        traceback.print_exc()
        return 1
