#!/usr/bin/env python3
"""lotek.run -- static site builder

Requires: pandoc in PATH or markdown module
"""

from lotek.lib.site_time import now_string
from lotek.lib.highlight import init_formatter
from lotek.lib.pages import generate_pages, generate_pages_parallel
from lotek.lib.posts import generate_posts, generate_posts_parallel, load_posts
from lotek.lib.util import measure
from lotek.lib.index import generate_index_landing
from lotek.lib.static import wipe_and_copy_to_output_dir
from lotek.lib.logger import log
from lotek.lib.warp import warp_content
from lotek.plugins.rss import generate_rss
from lotek.plugins.robots import generate_robots

def _build(dirs, config, parallel=True):
    """main entry point"""
    out = dirs.OUTPUT
    log.info("building lotek at %s", out)
    out.mkdir(exist_ok=True)
    dirs.OUTPUT_POSTS.mkdir(exist_ok=True)
    dirs.OUTPUT_STATIC.mkdir(exist_ok=True)
    formatter = init_formatter(dirs, config)
    posts = load_posts(dirs, config)
    buildable = []
    # hash needs to happen after posts load so we don't accidentally hash an
    # embargoed post without building it, leaving it unbuildable in the future
    if config.lotek.warp:
        log.info("warp speed engaged, building dirty pages only")
        buildable = warp_content(dirs, posts, "posts")
    else:
        buildable = posts

    # Use parallel version if enabled
    if parallel:
        measure(generate_posts_parallel, dirs, config, buildable, out, stage_name="posts")
    else:
        measure(generate_posts, dirs, config, buildable, out, stage_name="posts")

    if parallel:
        measure(generate_pages_parallel, dirs, config, out, stage_name="pages")
    else:
        measure(generate_pages, dirs, config, out, stage_name="pages")

    if config.features.robotstxt:
        log.info("generating robots.txt...")
        measure(generate_robots, config, posts, out, stage_name="robots.txt")
    if config.features.rss:
        log.info("generating RSS feed...")
        measure(generate_rss, dirs, config, posts, out, stage_name="rss")
    measure(generate_index_landing, dirs, config, posts, out, stage_name="index")
    measure(wipe_and_copy_to_output_dir, dirs, out, stage_name="static")
    log.info("built %s posts", len(posts))

    last_file = out / "_last"
    last_file.write_text(now_string(config))

def build(dirs, config, parallel=True):
    measure(_build, dirs, config, parallel, stage_name="build")
