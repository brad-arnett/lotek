from datetime import datetime

from lotek.lib.frontmatter import parse_frontmatter
from lotek.lib.logger import log


def _table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, c in enumerate(row):
            widths[i] = max(widths[i], len(str(c)))
    hdr = "│ " + " │ ".join(h.center(w) for h, w in zip(headers, widths)) + " │"
    print(hdr)
    print("-" * len(hdr))
    for row in rows:
        print("│ " + " │ ".join(str(c).ljust(w) for c, w in zip(row, widths)) + " │")


def cmd_list(dirs, config):
    posts_dir = dirs.CONTENT_POSTS
    if not posts_dir.exists():
        log.info("No posts directory found")
        return 0
    today = datetime.now().date()
    posts = []
    for f in posts_dir.glob("*.md"):
        meta, _ = parse_frontmatter(f.read_text())
        if meta.get("title"):
            posts.append((f, meta))
    if not posts:
        log.info("No posts found")
        return 0

    def sort_key(item):
        try:
            return datetime.strptime(item[1].get("date", ""), "%Y-%m-%d").date()
        except ValueError:
            return today

    posts.sort(key=sort_key, reverse=True)
    rows = []
    for f, meta in posts:
        date_str = meta.get("date", "")
        if meta.get("publish", "").lower() == "false":
            state = "hidden"
        elif config.features.skip_future:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                state = f"in {(d - today).days}d" if d > today else "live"
            except ValueError:
                state = "live"
        else:
            state = "live"
        rows.append([date_str, meta.get("title", ""), f.stem, state])
    _table(["date", "title", "slug", "status"], rows)
    return 0
