from datetime import datetime
from lotek.lib.colors import red, green
from lotek.lib.dirs import dirs

def cmd_add(title):
    if not title:
        print(red("Title required"))
        return 1
    posts_dir = dirs.CONTENT_POSTS
    posts_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-")
    fname = f"{today}-{slug}.md"
    fp = posts_dir / fname
    if fp.exists():
        print(red(f"Already exists: {fname}"))
        return 1
    template_path = dirs.TEMPLATES / "post.md"
    if not template_path.exists():
        print(red("Templates not found — run 'lotek init' first"))
        return 1
    template = template_path.read_text()
    fp.write_text(template.replace("{title}", title).replace("{date}", today))
    print(green(f"Created: content/posts/{fname}"))
    return 0
