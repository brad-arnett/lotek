"""index page generator"""

from lotek.lib.site_config import config
from lotek.lib.site_time import now_string
from lotek.lib.html_stubs import html_stub_index
from lotek.lib.render import render, render_wrap


def generate_index_landing(posts, out):
    """Generate the index landing page."""
    items = ""
    for post in posts:
        items += html_stub_index(post)
    content = render("index.html", {"ITEMS": items, "DESC": config.site.description})
    (out / "index.html").write_text(
        render_wrap(content, config.site.title, url=config.site.url)
    )

    last_file = out / "_last"
    last_file.write_text(now_string())
