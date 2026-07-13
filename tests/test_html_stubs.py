"""Test HTML stubs generation."""

import unittest
from lotek.lib.html_stubs import html_stub_index, html_stub_feed_items


class TestHTMLStubIndex(unittest.TestCase):
    def test_generate_index_stub(self):
        post = {
            "date": "2026-06-15",
            "slug": "hello",
            "title": "Hello",
        }

        result = html_stub_index(post)

        self.assertIn("<li>", result)
        self.assertIn("date", result)
        self.assertIn("2026-06-15", result)
        self.assertIn("hello", result)
        self.assertIn("Hello", result)
        self.assertIn("</li>", result)
        self.assertIn("\n", result)

    def test_generate_index_stub_has_newline(self):
        post = {
            "date": "2026-06-15",
            "slug": "test",
            "title": "Test",
        }

        result = html_stub_index(post)

        self.assertTrue(result.endswith("\n"))

    def test_generate_index_stub_with_special_chars(self):
        post = {
            "date": "2026-06-15",
            "slug": "test-article",
            "title": "Test & More <HTML>",
        }

        result = html_stub_index(post)
        # Note: html_stub_index does not escape special chars
        self.assertIn("&", result)
        self.assertIn("<", result)


class TestHTMLStubFeedItems(unittest.TestCase):
    @unittest.skip("import a config first")
    def test_basic_feed_item(self):
        post = {
            "date": "2026-06-15",
            "slug": "hello",
            "title": "Hello",
        }
        html = "<p>Hello world</p>"

        result = html_stub_feed_items(post, html)

        self.assertIn("<item>", result)
        self.assertIn("<title>Hello</title>", result)
        self.assertIn("<link>http://localhost:8000/posts/hello.html</link>", result)
        self.assertIn("<pubDate>2026-06-15</pubDate>", result)
        self.assertIn("<description>", result)
        self.assertIn("Hello world", result)
        self.assertIn("</item>\n", result)

    @unittest.skip("import a config first")
    def test_feed_item_with_special_chars(self):
        post = {
            "date": "2026-06-15",
            "slug": "test",
            "title": "Test <Title>",
        }
        html = "<p>Test & More</p>"

        result = html_stub_feed_items(post, html)
        # Note: html_stub_feed_items does not escape special chars
        self.assertIn("&", result)
        self.assertIn("<", result)

    @unittest.skip("import a config first")
    def test_feed_item_with_html(self):
        post = {
            "date": "2026-06-15",
            "slug": "test",
            "title": "Test",
        }
        html = "<p><strong>HTML content</strong></p>"

        result = html_stub_feed_items(post, html)

        self.assertIn("CDATA", result)
        self.assertIn("HTML content", result)

    @unittest.skip("import a config first")
    def test_feed_item_structure(self):
        post = {
            "date": "2026-06-15",
            "slug": "test",
            "title": "Test",
        }
        html = "<p>Content</p>"

        result = html_stub_feed_items(post, html)

        lines = result.strip().split("\n")
        self.assertGreater(len(lines), 5)
        self.assertIn("<title>Test</title>", lines[1])
        self.assertIn("<link>http://localhost:8000/posts/test.html</link>", lines[2])


if __name__ == "__main__":
    unittest.main()
