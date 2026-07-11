"""post handling library"""

from datetime import datetime
from zoneinfo import ZoneInfo
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from lotek.lib.render import md_to_html, render, render_wrap
from lotek.lib.frontmatter import parse_frontmatter
from lotek.lib.logger import log

# Default batch size for parallel processing
DEFAULT_BATCH_SIZE = 10


def _render_single_post(args):
    """Render a single post. Wrapper for ThreadPoolExecutor."""
    dirs, post, posts_dir, config = args
    start = time.perf_counter()
    html = md_to_html(dirs, post["body"])
    content = render(
        dirs,
        "post.html",
        {
            "TITLE": post["title"],
            "DATE": post["date"],
            "CONTENT": html,
        },
    )
    post_url = f"{config.site.url}/posts/{post['slug']}.html"
    page = render_wrap(
        dirs,
        content,
        f"{post['title']} -- {config.site.title}",
        desc=post["desc"],
        url=post_url,
        page_type="article",
    )
    (posts_dir / f"{post['slug']}.html").write_text(page)
    elapsed = time.perf_counter() - start
    log.debug("%.2fs - %s", elapsed, post["title"])


def _get_config():
    """Get global config from lotek.lib.context.config."""
    import lotek.lib.context

    return lotek.lib.context.config


def _render_batch(args, batch, posts_dir):
    """Render a batch of posts concurrently."""
    dirs, config = args
    config = _get_config()
    batch_posts = list(batch)
    with ThreadPoolExecutor(max_workers=len(batch_posts)) as executor:
        futures = [
            executor.submit(
                _render_single_post,
                (dirs, post, posts_dir, config),
            )
            for post in batch_posts
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                post = next(
                    (
                        p
                        for p in batch_posts
                        if p["slug"] == future.get_args()[1]["slug"]
                    ),
                    None,
                )
                log.warning(
                    "Failed to render %s: %s", post["title"] if post else "unknown", e
                )


def generate_posts_parallel(dirs, posts, out):
    """Render posts in parallel using concurrent execution."""
    from lotek.lib.context import config

    posts_dir = out / "posts"
    posts_dir.mkdir(exist_ok=True)

    if not posts:
        return

    # Split posts into batches
    batch_size = DEFAULT_BATCH_SIZE
    batches = []
    for i in range(0, len(posts), batch_size):
        batches.append(posts[i : i + batch_size])

    args = (dirs, config)

    with ThreadPoolExecutor(max_workers=len(batches)) as executor:
        futures = [
            executor.submit(_render_batch, args, batch, posts_dir) for batch in batches
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                log.error("Failed to render batch: %s", e)


def generate_posts(dirs, posts, out):
    """Render posts sequentially (legacy behavior)."""
    from lotek.lib.context import config

    posts_dir = out / "posts"
    posts_dir.mkdir(exist_ok=True)
    for i, post in enumerate(posts):
        start = time.perf_counter()
        html = md_to_html(dirs, post["body"])
        content = render(
            dirs,
            "post.html",
            {
                "TITLE": post["title"],
                "DATE": post["date"],
                "CONTENT": html,
            },
        )
        post_url = f"{config.site.url}/posts/{post['slug']}.html"
        page = render_wrap(
            dirs,
            content,
            f"{post['title']} -- {config.site.title}",
            desc=post["desc"],
            url=post_url,
            page_type="article",
        )
        (posts_dir / f"{post['slug']}.html").write_text(page)
        log.debug("%.2fs - %s", time.perf_counter() - start, post["title"])


def load_posts(dirs, posts_dir=None):
    from lotek.lib.context import config

    if posts_dir is None:
        posts_dir = dirs.CONTENT_POSTS
    posts = []
    if not posts_dir.exists():
        return posts
    if config.features.skip_future:
        today = datetime.now(ZoneInfo(config.rss.timezone)).date()
        for path in sorted(posts_dir.glob("*.md"), reverse=True):
            text = path.read_text()
            meta, body = parse_frontmatter(text)
            post_date_str = meta.get("date", "")
            post_date = None
            try:
                post_date = datetime.strptime(post_date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
            # skip if publish is explicitly false
            if meta.get("publish", "").lower() == "false":
                log.info("skipping post %s as it is not published", path.stem)
                continue
            # skip if undated or future
            if post_date is None or post_date > today:
                log.info(
                    "info: skipping post %s as it is not published or future", path.stem
                )
                continue
            posts.append(
                {
                    "path": path,
                    "slug": path.stem,
                    "title": meta.get("title", path.stem),
                    "date": post_date_str,
                    "desc": meta.get("desc", ""),
                    "body": body,
                }
            )
        return posts

    # When skip_future is disabled, include all posts (no date filtering)
    for path in sorted(posts_dir.glob("*.md"), reverse=True):
        text = path.read_text()
        meta, body = parse_frontmatter(text)
        # skip if publish is explicitly false (or not set in stub)
        if meta.get("publish", "").lower() == "false":
            continue
        posts.append(
            {
                "path": path,
                "slug": path.stem,
                "title": meta.get("title", path.stem),
                "date": meta.get("date", ""),
                "desc": meta.get("desc", ""),
                "body": body,
            }
        )
    return posts
