import sys
from lotek.lib.colors import red
import lotek.build as build_module

def cmd_build(dirs):

    try:
        build_module.build(dirs)
        return 0
    except Exception as e:
        print(red(f"Build failed: {e}"), file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
