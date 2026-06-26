"""lotek.run - A static site builder."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("lotek-run")
except PackageNotFoundError:
    __version__ = "unknown"

import lotek.cli as cli

def main():
    cli.main()
