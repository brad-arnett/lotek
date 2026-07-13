#!/usr/bin/env python3
"""lotek - operational command for lotek.run."""

import argparse
import logging
from pathlib import Path
import lotek

from zoneinfo import ZoneInfo

from lotek.lib.dirs import Dirs
from lotek.lib.site_config import load_config
from lotek.lib.init import init
from lotek.lib.site_config import load_config
from lotek.cmd.add import cmd_add
from lotek.cmd.build import cmd_build
from lotek.cmd.clean import cmd_clean
from lotek.cmd.list import cmd_list
from lotek.cmd.publish import cmd_publish, cmd_unpublish
from lotek.cmd.serve import cmd_serve


USAGE = f"""
lotek - a tiny static site generator
ver: {getattr(lotek, "__version__", "unknown")}

Build:
  lotek build [--debug]   Build the site (with --debug show timing)
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

    p = subs.add_parser("build")
    p.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output including timing information",
    )

    p.add_argument(
        "--force",
        action="store_true",
        help="build every post and page even if they haven't changed"
    )

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
    args = setup_cmd_parser()
    if args.command == "init" and args.path:
        wd = Path(args.path)
        # init creates its own config, skip loading
        _main(args, wd, None)
        return
    wd = Path.cwd()
    from lotek.lib.logger import log
    config = load_config(wd / "site-config.toml")
    try:
        if args.force:
            print("force flag is set, building all posts")
            config.lotek.warp = True
    except Exception as e:
        print(e)
    _main(args, wd, config)

def _main(args, wd, config):
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
            if args.force:
                print("setting force")
                config.lotek.warp = False
            if args.debug:
                from lotek.lib.logger import log
                print("setting debug")
                log.set_level(logging.DEBUG)
            return cmd_build(dirs, config)
        if args.command == "clean":
            return cmd_clean(dirs, config)
        if args.command == "serve":
            return cmd_serve(dirs, config, args.port)
        if args.command == "list":
            return cmd_list(dirs, config)
        if args.command == "add":
            return cmd_add(dirs, config, args.title)
        if args.command == "publish":
            return cmd_publish(dirs, config, args.slug)
        if args.command == "unpublish":
            return cmd_unpublish(dirs, config, args.slug)
    except KeyboardInterrupt:
        log.error("\nInterrupted by user")
        return 1
    except Exception as e:
        from traceback import format_exc
        log.error("Error: %s", e)
        log.error(format_exc())
        return 1


if __name__ == "__main__":
    main()
