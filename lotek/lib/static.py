"""static directory generator"""

import shutil
from lotek.lib.dirs import dirs

def wipe_and_copy_to_output_dir(out):
    """clears out the output/static directory and copies the static/ back into it"""
    static_dst = out / "static"
    if static_dst.exists():
        shutil.rmtree(static_dst)
    shutil.copytree(dirs.STATIC, static_dst)
