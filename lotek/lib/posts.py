"""post handling library"""

from datetime import datetime
from zoneinfo import ZoneInfo
from lotek.lib.render import md_to_html, render, render_wrap
from lotek.lib.frontmatter import parse_frontmatter


def generate_posts(dirs, posts, out):
    from lotek.lib.context import config
    posts_dir = out / "posts"
    posts_dir.mkdir(exist_ok=True)
    for post in posts:
        html = md_to_html(dirs, post["body"])
        content = render(dirs,
            "post.html",
            {
                "TITLE": post["title"],
                "DATE": post["date"],
                "CONTENT": html,
            },
        )
        post_url = f"{config.site.url}/posts/{post['slug']}.html"
        page = render_wrap(dirs,
            content,
            f"{post['title']} -- {config.site.title}",
            desc=post["desc"],
            url=post_url,
            page_type="article",
        )
        (posts_dir / f"{post['slug']}.html").write_text(page)


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
                print(f"info: skipping post {path.stem} as it is not published")
                continue
            # skip if undated or future
            if post_date is None or post_date > today:
                print(
                    f"info: skipping post {path.stem} as it is not published or future"
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
