"""Test RSS feed generation."""

import unittest
from pathlib import Path
from unittest.mock import patch
from lotek.lib.site_config import config
from lotek.plugins.rss import generate_rss


class TestRSSFeedGeneration(unittest.TestCase):
    """Test RSS feed generation."""

    def setUp(self):
        """Set up test output directory."""
        import tempfile

        self.test_output = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test output directory."""
        import shutil

        if self.test_output.exists():
            shutil.rmtree(self.test_output)

    def test_feed_xml_exists(self):
        """Test feed.xml is generated."""
        posts = []
        generate_rss(posts, self.test_output)

        feed_xml = self.test_output / "feed.xml"
        self.assertTrue(feed_xml.exists())

    def test_feed_xml_content(self):
        """Test feed.xml has correct RSS content."""
        posts = []
        generate_rss(posts, self.test_output)

        feed_xml = self.test_output / "feed.xml"
        content = feed_xml.read_text()

        self.assertIn("<?xml version", content)
        self.assertIn('<rss version="2.0">', content)
        self.assertIn("<channel>", content)
        self.assertIn("</channel>", content)
        self.assertIn("</rss>", content)

    def test_feed_xml_site_info(self):
        """Test feed.xml contains site info."""
        posts = []
        generate_rss(posts, self.test_output)

        feed_xml = self.test_output / "feed.xml"
        content = feed_xml.read_text()

        self.assertIn("https://lotek.run", content)
        self.assertIn("https://lotek.run", content)
        self.assertIn("dispatches from the margins", content)

    def test_feed_xml_build_date(self):
        """Test feed.xml has build date."""
        posts = []
        generate_rss(posts, self.test_output)

        feed_xml = self.test_output / "feed.xml"
        content = feed_xml.read_text()

        self.assertIn("<lastBuildDate>", content)
        self.assertIn("</lastBuildDate>", content)

    def test_feed_xml_with_posts(self):
        """Test feed.xml with posts."""
        posts = [
            {
                "date": "2026-06-15",
                "slug": "hello",
                "title": "Hello",
                "desc": "Hello description",
                "body": "Hello body text",
            },
            {
                "date": "2026-06-16",
                "slug": "world",
                "title": "World",
                "desc": "World description",
                "body": "World body text",
            },
        ]

        generate_rss(posts, self.test_output)

        feed_xml = self.test_output / "feed.xml"
        content = feed_xml.read_text()

        self.assertIn("<title>Hello</title>", content)
        self.assertIn("posts/hello.html", content)
        self.assertIn("<title>World</title>", content)
        self.assertIn("posts/world.html", content)

    def test_feed_xml_limit(self):
        """Test feed.xml respects RSS_LIMIT."""
        posts = [
            {
                "date": "2026-06-01",
                "slug": f"post-{i}",
                "title": f"Post {i}",
                "desc": f"Desc {i}",
                "body": f"Body {i}",
            }
            for i in range(50)
        ]

        generate_rss(posts, self.test_output)

        feed_xml = self.test_output / "feed.xml"
        content = feed_xml.read_text()

        title_count = content.count("<title>Post")
        self.assertLessEqual(title_count, config.rss.limit)


class TestRSSFeedDate(unittest.TestCase):
    """Test RSS feed date format."""

    def setUp(self):
        """Set up test output directory."""
        import tempfile

        self.test_output = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test output directory."""
        import shutil

        if self.test_output.exists():
            shutil.rmtree(self.test_output)

    def test_rfc5322_format(self):
        """Test feed date is in RFC 5322 format."""
        posts = []

        with patch.object(config.rss, "timezone", "UTC"):
            generate_rss(posts, self.test_output)

            feed_xml = self.test_output / "feed.xml"
            content = feed_xml.read_text()

            self.assertIn("<lastBuildDate>", content)
            self.assertIn("+0000", content)


if __name__ == "__main__":
    unittest.main()
