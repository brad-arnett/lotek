import os
import sys

BOLD, RESET = "\033[1m", "\033[0m"

def _color(t, c):
    if os.isatty(sys.stderr.fileno()):
        return c + t + RESET
    return t

def green(t):
    return _color(t, "\033[32m")

def red(t):
    return _color(t, "\033[31m")

def dim(t):
    return _color(t, "\033[2m")
