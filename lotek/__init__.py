"""lotek.run - A static site builder."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("lotek")
except PackageNotFoundError:
    __version__ = "unknown"

from lotek import cli
from lotek.lib.build import build


def main():
    cli.main()
