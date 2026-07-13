import subprocess
import shutil
import sys
from lotek.lib.logger import log
from lotek.lib.highlight import process_code_blocks


def _has_pandoc():
    return shutil.which("pandoc") is not None


def md_to_html(dirs, text, config):
    text = process_code_blocks(dirs, config, text)
    if _has_pandoc():
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "html", "--no-highlight"],
            input=text.encode(),
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            log.error("pandoc: %s", result.stderr.decode())
            sys.exit(1)
        return result.stdout.decode()
    else:
        import markdown as md

        return md.markdown(text, extensions=["extra", "smarty"])


def render(dirs, template_name, replacements):
    text = (dirs.TEMPLATES / template_name).read_text()
    for key, value in replacements.items():
        if value:
            text = text.replace(f"[[{key}]]", value)
    for key in replacements:
        if f"[[{key}]]" in text:
            text = text.replace(f"[[{key}]]", "")
    return text


def _nav_html(config):

    return "\n      ".join(
        f'<a href="{link.href}">{link.label}</a>' for link in config.nav
    )


def render_wrap(dirs, config, content, title, desc=None, url=None, page_type="website"):
    """convenience wrapper for rendering a page with the base template"""

    url = url or config.site.url
    return render(
        dirs,
        "base.html",
        {
            "TITLE": title,
            "CONTENT": content,
            "SITE_TITLE": config.site.title,
            "SITE_DESC": config.site.description,
            "META_DESC": desc or config.site.description,
            "META_URL": url or config.site.url,
            "META_TYPE": page_type,
            "NAV": _nav_html(config),
        },
    )
