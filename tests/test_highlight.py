"""Test syntax highlighting via Pygments."""

import unittest
from pathlib import Path
import tempfile
import shutil
from lotek.lib.highlight import process_code_blocks
from lotek.lib.init import init
from lotek.lib.site_config import load_config


def get_temp_dir():
    return Path(tempfile.mkdtemp())

dirs = unittest.mock.MagicMock()
config = unittest.mock.MagicMock()

class TestProcessCodeBlocks(unittest.TestCase):

    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.test_output = None
        self.config = None

    def test_fenced_block_replaced(self):
        result = process_code_blocks(dirs, self.config, "```python\ndef foo(): pass\n```")
        self.assertIn("<pre>", result)
        self.assertNotIn("```", result)

    def test_code_content_present(self):
        result = process_code_blocks(dirs, self.config, "```python\ndef foo(): pass\n```")
        self.assertIn("foo", result)

    def test_no_code_blocks(self):
        text = "Just plain text with no code."
        self.assertEqual(process_code_blocks(dirs, self.config, text), text)

    def test_multiple_blocks(self):
        text = "```python\nx = 1\n```\n\nSome text.\n\n```bash\necho hello\n```"
        result = process_code_blocks(dirs, self.config, text)
        self.assertEqual(result.count("<pre>"), 2)

    def test_unknown_language_handled(self):
        result = process_code_blocks(dirs, self.config, "```unknownlang\nsome code\n```")
        self.assertIn("<pre>", result)
        self.assertIn("some code", result)

    def test_no_language_handled(self):
        result = process_code_blocks(dirs, self.config, "```\nsome code\n```")
        self.assertIn("<pre>", result)
        self.assertIn("some code", result)

    def test_html_entities_escaped(self):
        result = process_code_blocks(dirs, self.config, "```python\nprint('<script>&')\n```")
        self.assertIn("&lt;script&gt;", result)
        self.assertIn("&amp;", result)

    def test_python_keywords_highlighted(self):
        result = process_code_blocks(dirs, self.config, "```python\ndef foo():\n    return None\n```")
        self.assertIn("<span", result)

    def test_produces_highlight_wrapper(self):
        result = process_code_blocks(dirs, self.config, "```python\nx = 1\n```")
        self.assertIn('class="highlight"', result)


if __name__ == "__main__":
    unittest.main()
