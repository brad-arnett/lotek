"""warp.py

Hash based accelerator for lotek.

This library is designed to enable lotek to selectively build only
values that have changed since the last time 'lotek build' was run.

It does this by keeping a hash value of each markdown file and then
comparing this hash value to the hash value of the file at build-time.
"""

import hashlib
from pathlib import Path
from lotek.lib.dirs import Dirs
from lotek.lib.logger import log

class Warp:
    def __init__(self, dirs: Dirs):
        self.dirs = dirs
        self.dirs.LOTEK_WARP_PAGES.mkdir(parents=True, exist_ok=True)
        self.dirs.LOTEK_WARP_POSTS.mkdir(parents=True, exist_ok=True)

    def can_warp(self, path: Path, path_type: str):
        """compares a file against its hash to determine if we can warp (skip)
        past it, or if it is dirty and should rebuild

        Args:
            - path: the path to the file
            - path_type: the type of file (post or page)

        return False if the file has changed, True otherwise.
        """
        if path.exists() and path.is_file():
            if path_type == "posts":
                warp_dir = self.dirs.LOTEK_WARP_POSTS
            elif path_type == "pages":
                warp_dir = self.dirs.LOTEK_WARP_PAGES
            else:
                raise ValueError(f"Invalid path type: {path_type}")
            stem = path.stem
            if not (warp_dir / stem).exists():
                # no hash, should build file
                fhash = hashlib.sha256(path.read_bytes()).hexdigest()
                (warp_dir / stem).write_text(fhash)
                log.debug("warp %s? %s", stem, False)
                return False
            else:
                # hash exists, read hash and compare
                old_hash = (warp_dir / stem).read_text()
                new_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                if old_hash == new_hash:
                    log.debug("warp %s? %s", stem, True)
                    return True
                else:
                    (warp_dir / stem).write_text(new_hash)
                    log.debug("warp %s? %s", stem, False)
                    return False
        raise FileNotFoundError(f"No file found at {path}")

def warp_content(dirs, posts, content_type: str):
    """also works for pages
    
    Args:
        - dirs: a Dirs object
        - posts: list of posts/pages
        - content_type: "posts" or "pages"
    """
    buildable_posts = []
    _warp = Warp(dirs)
    for p in posts:
        p_path = None
        if isinstance(p, Path):
            p_path = p
        else: # is a dict-type object
            p_path = p["path"]
        if not _warp.can_warp(p_path, content_type):
            # can't warp, need to build
            buildable_posts.append(p)
    return buildable_posts
