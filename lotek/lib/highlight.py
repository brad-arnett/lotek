"""Syntax highlighting via Pygments."""

import re
import shutil
from datetime import date
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from lotek.lib.logger import log
_FENCE = re.compile(r"^```(\w*)\n([\s\S]*?)^```[ \t]*$", re.MULTILINE)

highlight_formatter = None

def init_formatter(dirs, config):
    global highlight_formatter
    style = config.features.code_theme
    last_code_file = dirs.LOTEK / "last_code_theme"
    last_file = ""
    
    if highlight_formatter is not None:
        log.debug("highlight formatter already set")
        return
    
    if last_code_file.exists():
        last_file = last_code_file.read_text()
        if last_file == style:
            log.debug("pygments theme unchanged")
            return
    
    # theme has changed, update the last code theme
    last_code_file.write_text(style)
    # preserve any existing pygments.css
    backup_filename = (
        dirs.STATIC / f"pygments-backup-{date.today().strftime('%Y%m%d-%H%M%S')}.css"
    )
    if (dirs.STATIC / "pygments.css").exists():
        shutil.move(dirs.STATIC / "pygments.css", backup_filename)
        log.info("backed up existing pygments.css to %s", backup_filename)
    # write out the new theme's css
    highlight_formatter = HtmlFormatter(style=style)
    (dirs.STATIC / "pygments.css").write_text(
        highlight_formatter.get_style_defs("div.highlight")
    )

def process_code_blocks(dirs, config, text):
    global highlight_formatter
    if not highlight_formatter:
        init_formatter(dirs, config)
    def replace(m):
        lang = m.group(1).strip().lower() or "text"
        code = m.group(2)
        if code.endswith("\n"):
            code = code[:-1]
        try:
            lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound:
            lexer = get_lexer_by_name("text")
        return "\n\n" + highlight(code, lexer, highlight_formatter) + "\n\n"

    return _FENCE.sub(replace, text)
