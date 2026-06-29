"""Test syntax highlighting via Pygments."""

import unittest
from lotek.lib.highlight import process_code_blocks


dirs = unittest.mock.MagicMock()
class TestProcessCodeBlocks(unittest.TestCase):

    def test_fenced_block_replaced(self):
        result = process_code_blocks(dirs, "```python\ndef foo(): pass\n```")
        self.assertIn("<pre>", result)
        self.assertNotIn("```", result)

    def test_code_content_present(self):
        result = process_code_blocks(dirs, "```python\ndef foo(): pass\n```")
        self.assertIn("foo", result)

    def test_no_code_blocks(self):
        text = "Just plain text with no code."
        self.assertEqual(process_code_blocks(dirs, text), text)

    def test_multiple_blocks(self):
        text = "```python\nx = 1\n```\n\nSome text.\n\n```bash\necho hello\n```"
        result = process_code_blocks(dirs, text)
        self.assertEqual(result.count("<pre>"), 2)

    def test_unknown_language_handled(self):
        result = process_code_blocks(dirs, "```unknownlang\nsome code\n```")
        self.assertIn("<pre>", result)
        self.assertIn("some code", result)

    def test_no_language_handled(self):
        result = process_code_blocks(dirs, "```\nsome code\n```")
        self.assertIn("<pre>", result)
        self.assertIn("some code", result)

    def test_html_entities_escaped(self):
        result = process_code_blocks(dirs, "```python\nprint('<script>&')\n```")
        self.assertIn("&lt;script&gt;", result)
        self.assertIn("&amp;", result)

    def test_python_keywords_highlighted(self):
        result = process_code_blocks(dirs, "```python\ndef foo():\n    return None\n```")
        # Pygments wraps keywords in spans — presence of any span confirms highlighting ran
        self.assertIn("<span", result)

    def test_produces_highlight_wrapper(self):
        result = process_code_blocks(dirs, "```python\nx = 1\n```")
        self.assertIn('class="highlight"', result)


if __name__ == "__main__":
    unittest.main()
