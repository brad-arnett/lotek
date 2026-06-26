"""generate the about page"""

from lotek.lib.site_config import config
from lotek.lib.dirs import dirs
from lotek.lib.render import render, render_wrap, md_to_html
from lotek.lib.frontmatter import parse_frontmatter


def generate_about(out):
    about = dirs.CONTENT_PAGES / "about.md"
    if about.exists():
        meta, body = parse_frontmatter(about.read_text())
        html = md_to_html(body)
        content = render(
            "post.html",
            {
                "TITLE": meta.get("title", "About"),
                "DATE": "",
                "CONTENT": html,
            },
        )
        (out / "about.html").write_text(
            render_wrap(
                content,
                f"About - {config.site.title}",
                url=f"{config.site.url}/about.html",
            )
        )
