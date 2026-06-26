import subprocess
import sys
from lotek.lib.colors import green, red
from lotek.lib.dirs import dirs

def cmd_serve(port=8000):
    output = dirs.OUTPUT
    if not output.exists():
        print(red("No output/ — run 'lotek build' first."))
        return 1
    print(green(f"Serving at http://localhost:{port}  (Ctrl-C to stop)"))
    try:
        subprocess.run(
            [sys.executable, "-m", "http.server", str(port), "-d", str(output)]
        )
    except KeyboardInterrupt:
        pass
    return 0
