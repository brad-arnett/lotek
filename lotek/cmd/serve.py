import subprocess
import sys
import threading
import time
from pathlib import Path
from lotek.lib.logger import log
from lotek.lib.dirs import Dirs
from lotek.lib.site_config import load_config


def get_watched_files():
    """Return dict of {filepath: mtime} for content/ and static/ files."""
    files = {}
    for p in Path("content").rglob("*"):
        if p.is_file():
            files[str(p)] = p.stat().st_mtime
    for p in Path("static").rglob("*"):
        if p.is_file():
            files[str(p)] = p.stat().st_mtime
    return files


def check_for_changes(current_files, last_files):
    """Return True if any watched file has changed."""
    if len(current_files) != len(last_files):
        return True
    for fpath, mtime in current_files.items():
        if abs(mtime - last_files.get(fpath, 0)) > 0.01:
            return True
    return False


def http_server(port, output_dir):
    """Run HTTP server."""
    subprocess.run(
        [sys.executable, "-m", "http.server", str(port), "-d", str(output_dir)],
        check=False,
    )


def rebuild():
    """Rebuild the site."""
    wd = Path.cwd()
    dirs = Dirs(wd)
    from lotek.build import build
    build(dirs)


def cmd_serve(dirs, _config, port=8000):
    output = dirs.OUTPUT
    if not output.exists():
        log.error("no output/ directory exists to serve.  Did you run `lotek build`?")
        return 1

    log.info("serving at http://localhost:%s.  Press ctrl-c to stop this server.", port)

    server_thread = threading.Thread(target=http_server, args=(port, output), daemon=False)
    server_thread.start()

    last_files = None
    try:
        while True:
            current_files = get_watched_files()
            if last_files is None or check_for_changes(current_files, last_files):
                rebuild()
            last_files = current_files
            time.sleep(1)
    except KeyboardInterrupt:
        server_thread.join()
    except Exception as e:
        log.error(f"Build failed: {e}")
        log.exc()
        server_thread.join()
        raise
    return 0
