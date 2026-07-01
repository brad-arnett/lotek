"""builds content/pages/*.md to output/*.html"""

from lotek.lib.render import render, render_wrap, md_to_html
from lotek.lib.frontmatter import parse_frontmatter
from lotek.lib.logger import log

def generate_pages(dirs, out):
    from lotek.lib.context import config
    pages_dir = dirs.CONTENT_PAGES
    if not pages_dir.exists():
        return
    for path in sorted(pages_dir.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text())
        if meta.get("publish", "").lower() == "false":
            log.info("skipping page %s as it is not published", path.stem)
            continue
        log.info("info: generating page %s", path.stem)
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
