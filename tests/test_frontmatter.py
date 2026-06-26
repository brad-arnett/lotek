"""Test frontmatter parsing."""

import unittest
from lotek.lib.frontmatter import parse_frontmatter


class TestFrontmatter(unittest.TestCase):
    def test_parse_valid_frontmatter(self):
        text = "---\ntitle: Test\ndate: 2026-06-15\ntags: test,meta\n---\nbody"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta["title"], "Test")
        self.assertEqual(meta["date"], "2026-06-15")
        self.assertEqual(meta["tags"], "test,meta")
        self.assertEqual(body, "body")

    def test_parse_invalid_frontmatter(self):
        text = "---\ntitle: Test\nsome content without closing delimiter"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)

    def test_parse_no_frontmatter(self):
        text = "# Just plain markdown\n\nSome content."
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)

    def test_parse_empty_frontmatter(self):
        text = "---\n---"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, "---\n---")

    def test_parse_single_key(self):
        text = "---\nkey: value\n---\nbody"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta, {"key": "value"})
        self.assertEqual(body, "body")

    def test_parse_keys_without_colon(self):
        text = "---\nkey: value\nnokey\n---\nbody"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta["key"], "value")
        self.assertEqual(meta, {"key": "value"})

    def test_parse_whitespace_handling(self):
        text = "---\n  title  :  Test  \n  date  :  2026-06-15  \n---\nbody"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta["title"], "Test")
        self.assertEqual(meta["date"], "2026-06-15")


if __name__ == "__main__":
    unittest.main()
