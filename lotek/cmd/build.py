import sys
from lotek.lib.colors import red
import lotek.build as build_module

def cmd_build():

    try:
        build_module.build()
        return 0
    except Exception as e:
        print(red(f"Build failed: {e}"), file=sys.stderr)
        return 1
