"""lotek directory structure"""
from pathlib import Path

class Dirs:
    """lotek directory structure"""
    def __init__(self, path=Path.cwd()):
        # pylint: disable=invalid-name
        self.CWD = path
        self.LOTEK = self.CWD / ".lotek"

        self.CONTENT = self.CWD / "content"
        self.CONTENT_POSTS = self.CONTENT / "posts"
        self.CONTENT_PAGES = self.CONTENT / "pages"

        self.STATIC = self.CWD / "static"
        self.IMAGES = self.CWD / "static" / "img"
        self.TEMPLATES = self.CWD / "templates"

        self.OUTPUT = self.CWD / "output"
        self.OUTPUT_POSTS = self.CWD / "output" / "posts"
        self.OUTPUT_STATIC = self.CWD / "output" / "static"

        # expected to be buried somewhere in site-packages
        self.PKG = _pkg_path = Path(__file__).parent.parent
        self.PKG_TEMPLATES = self.PKG / "templates"
        self.PKG_STATIC = self.PKG / "static"
