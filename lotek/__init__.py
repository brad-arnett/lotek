"""lotek.run - A static site builder."""

from importlib.metadata import version, PackageNotFoundError
from lotek import cli

try:
    __version__ = version("lotek-run")
except PackageNotFoundError:
    __version__ = "unknown"


def main():
    cli.main()
