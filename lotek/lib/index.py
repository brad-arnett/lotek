"""index page generator"""

from lotek.lib.site_time import now_string
from lotek.lib.html_stubs import html_stub_index
from lotek.lib.render import render, render_wrap


def generate_index_landing(dirs, posts, out):
    """Generate the index landing page."""
    from lotek.lib.context import config
    items = ""
    for post in posts:
        items += html_stub_index(post)
    content = render(dirs, "index.html", {"ITEMS": items, "DESC": config.site.description})
    (out / "index.html").write_text(
        render_wrap(dirs, content, config.site.title, url=config.site.url)
    )

    last_file = out / "_last"
    last_file.write_text(now_string())
