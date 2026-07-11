#!/usr/bin/env python3
"""lotek.run -- static site builder

Requires: pandoc in PATH or markdown module
"""

from lotek.lib.site_time import now_string
from lotek.lib.pages import generate_pages, generate_pages_parallel
from lotek.lib.posts import generate_posts, generate_posts_parallel, load_posts
from lotek.lib.util import measure
from lotek.lib.index import generate_index_landing
from lotek.lib.static import wipe_and_copy_to_output_dir
from lotek.lib.logger import log
from lotek.plugins.rss import generate_rss
from lotek.plugins.robots import generate_robots


def build(dirs, parallel=True):
    """main entry point"""

    out = dirs.OUTPUT
    log.info("building lotek at %s", out)
    out.mkdir(exist_ok=True)
    dirs.OUTPUT_POSTS.mkdir(exist_ok=True)
    dirs.OUTPUT_STATIC.mkdir(exist_ok=True)
    posts = load_posts(dirs)

    # Use parallel version if enabled
    if parallel:
        measure(generate_posts_parallel, dirs, posts, out, stage_name="posts")
    else:
        measure(generate_posts, dirs, posts, out, stage_name="posts")

    if parallel:
        measure(generate_pages_parallel, dirs, out, stage_name="pages")
    else:
        measure(generate_pages, dirs, out, stage_name="pages")

    from lotek.lib.context import config
    if config.features.robotstxt:
        log.info("generating robots.txt...")
        measure(generate_robots, posts, out, stage_name="robots.txt")
    if config.features.rss:
        log.info("generating RSS feed...")
        measure(generate_rss, dirs, posts, out, stage_name="RSS feed")
    measure(generate_index_landing, dirs, posts, out, stage_name="index")
    measure(wipe_and_copy_to_output_dir, dirs, out, stage_name="static")

    log.info("built %s posts -> output/", len(posts))
    last_file = out / "_last"
    last_file.write_text(now_string())
