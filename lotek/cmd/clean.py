
import shutil
from lotek.lib.colors import green

def cmd_clean(dirs):

    output = dirs.OUTPUT
    if output.exists():
        shutil.rmtree(output)
        print(green("Removed output/"))
    return 0
