"""static page generator — builds content/pages/*.md to output/*.html"""

from lotek.lib.render import render, render_wrap, md_to_html
from lotek.lib.frontmatter import parse_frontmatter


def generate_pages(dirs, out):
    from lotek.lib.context import config
    pages_dir = dirs.CONTENT_PAGES
    if not pages_dir.exists():
        return
    for path in sorted(pages_dir.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text())
        if meta.get("publish", "").lower() == "false":
            print(f"info: skipping page {path.stem} as it is not published")
            continue
        print(f"info: generating page {path.stem}")
        slug = path.stem
        title = meta.get("title", slug)
        html = md_to_html(dirs, body)
        content = render(dirs,
            "post.html",
            {
                "TITLE": title,
                "DATE": meta.get("date", ""),
                "CONTENT": html,
            },
        )
        (out / f"{slug}.html").write_text(
            render_wrap(dirs,
                content,
                f"{title} -- {config.site.title}",
                url=f"{config.site.url}/{slug}.html",
            )
        )
