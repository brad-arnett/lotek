"""lotek.run - A static site builder."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("lotek")
except PackageNotFoundError:
    __version__ = "unknown"

# must import after __version__ definition or version will always be unknown
from lotek import cli # pylint: disable=wrong-import-position
