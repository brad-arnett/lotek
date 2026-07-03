import subprocess
import sys
from lotek.lib.logger import log

def cmd_serve(dirs, port=8000):
    output = dirs.OUTPUT
    if not output.exists():
        log.error("no output/ directory exists to serve.  Did you run `lotek build`?")
        return 1
    log.info("serving at http://localhost:%s.  Press ctrl-c to stop this server.", port)
    try:
        subprocess.run(
            [sys.executable, "-m", "http.server", str(port), "-d", str(output)],
            check=False
        )
    except KeyboardInterrupt:
        pass
    return 0
