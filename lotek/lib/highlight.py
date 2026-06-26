"""Syntax highlighting via Pygments."""

import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

_FENCE = re.compile(r"^```(\w*)\n([\s\S]*?)^```[ \t]*$", re.MULTILINE)
_formatter = HtmlFormatter(style="default")


def process_code_blocks(text):
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
