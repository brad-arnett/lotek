import sys

from lotek.lib.frontmatter import parse_frontmatter
from lotek.lib.logger import log


def _strip_datecode(stem):
    if (
        len(stem) > 11
        and stem.startswith("20")
        and stem[4] == stem[7] == "-"
        and stem[10] == "-"
    ):
        return stem[11:]
    return stem


def find_post(dirs, slug):
    posts_dir = dirs.CONTENT_POSTS
    if not posts_dir.exists():
        return None
    fp = posts_dir / f"{slug}.md"
    if fp.exists():
        return fp
    for f in posts_dir.glob("*.md"):
        if slug == _strip_datecode(f.stem):
            return f
    matches = [
        f for f in posts_dir.glob("*.md") if _strip_datecode(f.stem).startswith(slug)
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        log.warning("Ambiguous: %s matches for '%s'", len(matches), slug)
        for m in matches:
            log.warning("  %s", m.stem)
        sys.exit(2)
    return None


def _set_publish(dirs, slug, value):
    fp = find_post(dirs, slug)
    if not fp:
        log.error("Not found: %s", slug)
        return 1
    meta, body = parse_frontmatter(fp.read_text())
    if not meta.get("title"):
        log.error("No title in frontmatter")
        return 1
    meta["publish"] = value
    fp.write_text(
        "---\n" + "".join(f"{k}: {v}\n" for k, v in meta.items()) + "---\n\n" + body
    )
    log.info("%s: %s", str("Published" if value == "true" else "Unpublished"), slug)
    return 0


def cmd_publish(dirs, slug):
    """i don't know if we even need these, really."""
    return _set_publish(dirs, slug, "true")


def cmd_unpublish(dirs, slug):
    """i don't know if we even need these, really."""
    return _set_publish(dirs, slug, "false")
