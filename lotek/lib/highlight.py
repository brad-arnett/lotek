"""Syntax highlighting via Pygments."""

import re
import shutil
from datetime import date
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

_FENCE = re.compile(r"^```(\w*)\n([\s\S]*?)^```[ \t]*$", re.MULTILINE)
_formatter = None


def _init_formatter(dirs, config):
    global _formatter
    style = config.features.code_theme
    _formatter = HtmlFormatter(classes=True, style=style)
    last_code_file = dirs.LOTEK / ".last_code_file"
    if last_code_file.exists():
        last_file = last_code_file.read_text()
        if last_file == style:
            # assume unchanged and return
            return
    # theme has changed, update the last code theme
    (dirs.LOTEK / ".last_code_theme").write_text(style)
    # preserve any existing pygments.css
    shutil.move(dirs.STATIC / "pygments.css", dirs.STATIC / f"pygments-backup-{date.today().strftime('%Y%m%d-%H%M%S')}.css")
    # write out the new theme's css
    (dirs.STATIC / "pygments.css").write_text(_formatter.get_style_defs('div.highlight'))

def process_code_blocks(dirs, text):
    from lotek.lib.context import config
    print( f"dbg: formatting with {config.features.code_theme}")
    if not _formatter:
        from lotek.lib.context import config
        _init_formatter(dirs, config)
    def replace(m):
        lang = m.group(1).strip().lower() or "text"
        code = m.group(2)
        if code.endswith("\n"):
            code = code[:-1]
        try:
            lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound:
            lexer = get_lexer_by_name("text")
        return "\n\n" + highlight(code, lexer, _formatter) + "\n\n"

    return _FENCE.sub(replace, text)
