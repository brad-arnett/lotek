"""generate the about page"""

from lotek.lib.render import render, render_wrap, md_to_html
from lotek.lib.frontmatter import parse_frontmatter


def generate_about(dirs, out):
    from lotek.lib.context import config
    cfg = config
    about = dirs.CONTENT_PAGES / "about.md"
    if about.exists():
        meta, body = parse_frontmatter(about.read_text())
        html = md_to_html(dirs, body)
        content = render(dirs,
            "post.html",
            {
                "TITLE": meta.get("title", "About"),
                "DATE": "",
                "CONTENT": html,
            },
        )
        (out / "about.html").write_text(
            render_wrap(dirs,
                content,
                f"About - {cfg.site.title}",
                url=f"{cfg.site.url}/about.html",
            )
        )
