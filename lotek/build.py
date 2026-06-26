#!/usr/bin/env python3
"""lotek.run -- static site builder

Requires: pandoc in PATH or markdown module
"""

from lotek.lib.site_config import config
from lotek.lib.site_time import now_string
from lotek.lib.pages import generate_pages
from lotek.lib.posts import generate_posts, load_posts
from lotek.lib.index import generate_index_landing
from lotek.lib.dirs import dirs
from lotek.lib.static import wipe_and_copy_to_output_dir
from lotek.plugins.rss import generate_rss
from lotek.plugins.robots import generate_robots


def build():
    """main entry point"""

    out = dirs.OUTPUT
    print(f"building lotek at {out}")
    out.mkdir(exist_ok=True)
    dirs.OUTPUT_POSTS.mkdir(exist_ok=True)
    dirs.OUTPUT_STATIC.mkdir(exist_ok=True)
    posts = load_posts(dirs.CONTENT_POSTS)

    generate_posts(posts, out)
    generate_pages(out)
    if config.features.robotstxt:
        print("generating robots.txt...")
        generate_robots(posts, out)
    if config.features.rss:
        print("generating RSS feed...")
        generate_rss(posts, out)
    generate_index_landing(posts, out)
    wipe_and_copy_to_output_dir(out)

    print(f"built {len(posts)} posts -> output/")
    last_file = out / "_last"
    last_file.write_text(now_string())
