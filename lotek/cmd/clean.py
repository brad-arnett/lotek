
import shutil
from lotek.lib.colors import green
from lotek.lib.dirs import dirs

def cmd_clean():

    output = dirs.OUTPUT
    if output.exists():
        shutil.rmtree(output)
        print(green("Removed output/"))
    return 0
