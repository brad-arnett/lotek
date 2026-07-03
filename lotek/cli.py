#!/usr/bin/env python3
"""lotek - operational command for lotek.run."""
import sys
import argparse
from pathlib import Path
import lotek

from lotek.lib.dirs import Dirs
from lotek.lib.site_config import load_config
from lotek.lib.init import init
from lotek.lib.context import update_config
from lotek.lib.logger import log
from lotek.cmd.add import cmd_add
from lotek.cmd.build import cmd_build
from lotek.cmd.clean import cmd_clean
from lotek.cmd.list import cmd_list
from lotek.cmd.publish import cmd_publish, cmd_unpublish
from lotek.cmd.serve import cmd_serve

USAGE = f"""
lotek - Tiny Blog Management Tool
ver: {getattr(lotek, "__version__", "unknown")}

Build:
  lotek build             Build the site
  lotek clean             Remove build output
  lotek serve [--port N]  Serve output locally (default: 8000)

Content:
  lotek init              Make a new site from scratch
  lotek list              List all posts
  lotek add <title>       Create new post
  lotek publish <slug>    Mark a post as published
  lotek unpublish <slug>  Mark a post as unpublished
"""

def setup_cmd_parser():
    parser = argparse.ArgumentParser(prog="lotek")
    subs = parser.add_subparsers(dest="command")

    i = subs.add_parser("init")
    i.add_argument("path", type=str, default=".", nargs="?")

    subs.add_parser("build")

    subs.add_parser("clean")

    p = subs.add_parser("serve")
    p.add_argument("--port", "-p", type=int, default=8000)

    p = subs.add_parser("deploy")
    p.add_argument("--skip-build", action="store_true")


    subs.add_parser("list")

    p = subs.add_parser("add")
    p.add_argument("title", nargs="?")

    p = subs.add_parser("publish")
    p.add_argument("slug")

    p = subs.add_parser("unpublish")
    p.add_argument("slug")

    args = parser.parse_args()
    return args

def main():
    # load config
    args = setup_cmd_parser()
    if args.command == "init" and args.path:
        wd = Path(args.path)
        # init creates its own config, skip loading
        _main(args, wd)
        return
    wd = Path.cwd()
    update_config(load_config(wd / "site-config.toml"))
    _main(args, wd)

def _main(args, wd):
    if not args.command:
        print(USAGE)
        return 0
    # dirs derives from the current working directory (except init)
    dirs = Dirs(wd)
    try:
        if args.command == "init":
            # init is a special case and instantiates path based on an argument
            return init(Path.absolute(Path(args.path)))
        if args.command == "build":
            return cmd_build(dirs)
        if args.command == "clean":
            return cmd_clean(dirs)
        if args.command == "serve":
            return cmd_serve(dirs, args.port)
        if args.command == "list":
            return cmd_list(dirs)
        if args.command == "add":
            return cmd_add(dirs, args.title)
        if args.command == "publish":
            return cmd_publish(dirs, args.slug)
        if args.command == "unpublish":
            return cmd_unpublish(dirs, args.slug)
    except KeyboardInterrupt:
        log.error("\nInterrupted by user")
        return 1
    except Exception as e:
        log.error("Error: %s", e)
        return 1

if __name__ == "__main__":
    main()
