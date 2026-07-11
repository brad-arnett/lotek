from datetime import datetime
from lotek.lib.logger import log


def cmd_add(dirs, title):
    if not title:
        log.error("Title required")
        return 1
    posts_dir = dirs.CONTENT_POSTS
    posts_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-")
    fname = f"{today}-{slug}.md"
    fp = posts_dir / fname
    if fp.exists():
        log.warning("Already exists: %s", fname)
        return 1
    template_path = dirs.TEMPLATES / "post.md"
    if not template_path.exists():
        log.error(
            "%s doesn't exist, did you forget to run `lotek init` first?", template_path
        )
        return 1
    template = template_path.read_text()
    fp.write_text(template.replace("{title}", title).replace("{date}", today))
    log.info("Created: content/posts/%s", fname)
    return 0
