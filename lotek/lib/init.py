"""Site initialization command for lotek.run."""

import shutil
from datetime import date
from pathlib import Path
from lotek.lib.site_config import DEFAULT_CONFIG_TEMPLATE_PATH
from lotek.lib.dirs import Dirs
from lotek.lib.logger import log

# Get the package root directory
_pkg_path = Path(__file__).parent.parent


def init(site_path: Path, layout: str="") -> None:
    """Initialize a new lotek site in the given directory.

    Creates the directory structure, copies templates, and generates site-config.toml.

    Args:
        site_path: Path to the site directory to initialize. Uses cwd if not provided.
    """
    log.info("working path is: %s", site_path)

    dirs: Dirs = Dirs(site_path)
    # Create directory structure
    site_path.mkdir(parents=True, exist_ok=True)
    dirs.LOTEK.mkdir(exist_ok=True)
    dirs.CONTENT.mkdir(exist_ok=True)
    dirs.CONTENT_POSTS.mkdir(parents=True, exist_ok=True)
    dirs.CONTENT_PAGES.mkdir(exist_ok=True)
    dirs.STATIC.mkdir(exist_ok=True)
    dirs.IMAGES.mkdir(parents=True, exist_ok=True)
    dirs.TEMPLATES.mkdir(exist_ok=True)
    # Copy templates
    log.info("Copying templates...")
    for template in dirs.PKG_TEMPLATES.glob("*"):
        dst = dirs.TEMPLATES / template.name
        shutil.copy2(template, dst)

    # Copy static files
    log.info("Populating static directory..")
    static_src = dirs.PKG_STATIC
    for item in static_src.iterdir():
        if item.is_dir():
            shutil.copytree(item, dirs.STATIC / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dirs.STATIC)

    # Create site-config.toml from defaults
    config_path = site_path / "site-config.toml"
    if not config_path.exists():
        log.info("Creating %s from template...", config_path)
        config_path.write_text(DEFAULT_CONFIG_TEMPLATE_PATH.read_text())
        log.info("✓ Site configuration created")

    # Create an about page
    about_path = dirs.CONTENT_PAGES / "about.md"
    if not about_path.exists():
        log.info("Creating %s from template...", about_path)
        example_about = """---
title: About
date: 2026-06-15
---

lotek is a small static blog generator.  It uses very little technology to do this.

The name comes from the Lo-Tek in William Gibson's Johnny Mnemonic -- an underground community that lives in the margins of the city, outside the corporate system. Not against technology. Against the assumption that more technology is always better, that the newest version is always correct, that you should replace what works because something newer exists.

---

**rss**: /feed.xml

---

Built with pandoc and a Python script. No npm. No framework. No build chain.
"""
        about_path.write_text(example_about)
        log.info("✓ About page created")

    # Create an example post
    today = date.today().strftime("%Y-%m-%d")
    example_post = dirs.CONTENT_POSTS / f"{today}-welcome.md"
    if not example_post.exists():
        example_content = f"""---
title: Welcome to Lotek
date: {today}
desc: Your first post
---

Congratulations! You've created a new lotek site.

This is your first post. Edit or delete this file to get started.

## Quick Start

1. Add more posts in `content/posts/`
2. Add static pages in `content/pages/`
3. Customize `site-config.toml` to change site settings
4. Run `lotek build` to generate the site
5. Serve it with `lotek serve`
"""
        example_post.write_text(example_content)
        log.info("✓ Example post created")

    log.info("\nSite initialized at: %s", dirs.CWD)
    log.info("Next steps:")
    log.info("  - Edit content in content/posts/ and content/pages/")
    log.info("  - Customize settings in site-config.toml")
    log.info("  - Run 'lotek build' to generate the site")
