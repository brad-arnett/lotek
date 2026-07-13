"""Test robots.txt and sitemap.xml generation."""

import unittest
import tempfile
import shutil
from pathlib import Path
from lotek.plugins.robots import generate_robots, sitemap_url
from lotek.lib.site_config import load_config


class TestGenerateRobots(unittest.TestCase):
    """Test robots.txt generation."""

    def setUp(self):
        """Set up test output directory."""
        self.test_output = Path(tempfile.mkdtemp())
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        """Clean up test output directory."""
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.config = None

    def test_robots_txt_exists(self):
        """Test robots.txt is generated."""
        posts = []
        generate_robots(self.config, posts, self.test_output)

        robots_txt = self.test_output / "robots.txt"
        self.assertTrue(robots_txt.exists())

    def test_robots_txt_content(self):
        """Test robots.txt has correct content."""
        posts = []
        generate_robots(self.config, posts, self.test_output)

        robots_txt = self.test_output / "robots.txt"
        content = robots_txt.read_text()

        self.assertIn("User-agent: *", content)
        self.assertIn("Allow: /", content)
        self.assertIn("Sitemap:", content)

    def test_robots_txt_url(self):
        """Test robots.txt references sitemap."""
        posts = []
        generate_robots(self.config, posts, self.test_output)

        robots_txt = self.test_output / "robots.txt"
        content = robots_txt.read_text()

        self.assertIn("sitemap.xml", content)
        self.assertIn("http://localhost:8000", content)

    def test_robots_txt_no_posts(self):
        """Test robots.txt with no posts."""
        posts = []
        generate_robots(self.config, posts, self.test_output)

        robots_txt = self.test_output / "robots.txt"
        content = robots_txt.read_text()

        self.assertIn("User-agent: *", content)
        self.assertIn("Allow: /", content)


class TestSitemapURL(unittest.TestCase):
    """Test sitemap.xml generation."""

    def setUp(self):
        """Set up test output directory."""
        self.test_output = Path(tempfile.mkdtemp())
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        """Clean up test output directory."""
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.config = None

    def test_sitemap_xml_exists(self):
        """Test sitemap.xml is generated."""
        posts = []
        sitemap_url(posts, self.test_output, self.config)

        sitemap_xml = self.test_output / "sitemap.xml"
        self.assertTrue(sitemap_xml.exists())

    def test_sitemap_xml_content(self):
        """Test sitemap.xml has correct content."""
        posts = []
        sitemap_url(posts, self.test_output, self.config)

        sitemap_xml = self.test_output / "sitemap.xml"
        content = sitemap_xml.read_text()

        self.assertIn("<?xml version", content)
        self.assertIn("<urlset", content)
        self.assertIn("</urlset>", content)

    def test_sitemap_xml_structure(self):
        """Test sitemap.xml has proper structure."""
        posts = [
            {
                "slug": "hello",
                "date": "2026-06-15",
            },
            {
                "slug": "world",
                "date": "2026-06-16",
            },
        ]
        sitemap_url(posts, self.test_output, self.config)

        sitemap_xml = self.test_output / "sitemap.xml"
        content = sitemap_xml.read_text()

        self.assertIn("<url><loc>http://localhost:8000/</loc></url>", content)
        self.assertIn("posts/hello.html", content)
        self.assertIn("posts/world.html", content)
        self.assertIn("lastmod>2026-06-15</lastmod>", content)
        self.assertIn("lastmod>2026-06-16</lastmod>", content)

    def test_sitemap_xml_no_posts(self):
        """Test sitemap.xml with no posts."""
        posts = []
        sitemap_url(posts, self.test_output, self.config)

        sitemap_xml = self.test_output / "sitemap.xml"
        content = sitemap_xml.read_text()

        self.assertIn("<url><loc>http://localhost:8000/</loc></url>", content)
        self.assertNotIn("posts/", content)

    def test_sitemap_xml_with_many_posts(self):
        """Test sitemap.xml with many posts."""
        posts = [{"slug": f"post-{i}", "date": "2026-06-15"} for i in range(100)]
        sitemap_url(posts, self.test_output, self.config)

        sitemap_xml = self.test_output / "sitemap.xml"
        content = sitemap_xml.read_text()

        self.assertIn("<url>", content)
        self.assertEqual(content.count("<url>"), 101)


class TestGenerateRobotsIntegration(unittest.TestCase):
    """Test robots generation with posts."""

    def setUp(self):
        """Set up test output directory."""
        self.test_output = Path(tempfile.mkdtemp())
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        """Clean up test output directory."""
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.config = None

    def test_generate_robots_with_posts(self):
        """Test generate_robots generates sitemap when called with posts."""
        posts = [
            {
                "slug": "hello",
                "date": "2026-06-15",
            }
        ]

        generate_robots(self.config, posts, self.test_output)

        robots_txt = self.test_output / "robots.txt"
        sitemap_xml = self.test_output / "sitemap.xml"

        self.assertTrue(robots_txt.exists())
        self.assertTrue(sitemap_xml.exists())

    def test_sitemap_references_correct_url(self):
        """Test sitemap references posts at correct URL."""
        posts = [
            {
                "slug": "test-post",
                "date": "2026-06-15",
            }
        ]

        generate_robots(self.config, posts, self.test_output)

        sitemap_xml = self.test_output / "sitemap.xml"
        content = sitemap_xml.read_text()

        self.assertIn("posts/test-post.html", content)
        self.assertIn("lastmod>2026-06-15</lastmod>", content)


if __name__ == "__main__":
    unittest.main()
