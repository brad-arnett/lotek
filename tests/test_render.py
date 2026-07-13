"""Test template rendering and markdown conversion."""

import unittest
import tempfile
from pathlib import Path
from lotek.lib.dirs import Dirs
from lotek.lib.render import md_to_html, render, render_wrap
from lotek.lib.init import init
from lotek.lib.site_config import load_config

def get_temp_dir():
    return Path(tempfile.mkdtemp())

class TestTemplateRendering(unittest.TestCase):

    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(Path(self.test_output))
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        import shutil
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.dirs = None
        self.config = None

    def test_template_substitution(self):
        result = render(self.dirs,
            "base.html",
            {
                "SITE_TITLE": "Test Site",
                "SITE_URL": "https://test.com",
                "SITE_DESC": "A test description",
                "TITLE": "Page Title",
                "CONTENT": "<main>Content</main>",
                "META_DESC": "Meta desc",
                "META_URL": "https://test.com",
                "META_TYPE": "website",
            },
        )
        self.assertIn("Test Site", result)
        self.assertIn("https://test.com", result)

    def test_template_missing(self):
        with self.assertRaises(FileNotFoundError):
            render(self.dirs, "nonexistent.html", {})

    def test_template_without_replacements(self):
        result = render(self.dirs,
            "base.html",
            {
                "SITE_TITLE": "value1",
                # SITE_URL is missing
            },
        )
        self.assertIn("value1", result)

    def test_template_with_all_replacements(self):
        result = render(self.dirs,
            "base.html",
            {
                "SITE_TITLE": "My Site",
                "SITE_URL": "https://my.site",
                "SITE_DESC": "A description",
                "TITLE": "Page Title",
                "CONTENT": "<main>Content</main>",
                "RSS_FEED_URL": "https://my.site/feed.xml",
                "META_DESC": "Meta description",
                "META_URL": "https://my.site",
                "META_TYPE": "website",
            },
        )
        self.assertIn("My Site", result)
        self.assertIn("Page Title", result)
        self.assertIn("Content", result)


class TestRenderWrap(unittest.TestCase):
    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(Path(self.test_output))
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        import shutil
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.dirs = None
        self.config = None

    def test_wrap_basic(self):
        content = "<main>Content</main>"
        result = render_wrap(self.dirs, self.config,
            content, "Page Title", desc="Description", url="https://test.com"
        )
        self.assertIn("Page Title", result)
        self.assertIn("Content", result)
        self.assertIn("Description", result)
        self.assertIn("https://test.com", result)

    def test_wrap_default_url(self):
        content = "<main>Content</main>"
        result = render_wrap(self.dirs, self.config, content, "Page Title", desc="Description")
        self.assertIn("http://localhost:8000", result)

    def test_wrap_page_type(self):
        content = "<main>Content</main>"
        article = render_wrap(self.dirs, self.config, content, "Article", desc="Desc", page_type="article")
        self.assertIn("article", article)


class TestMarkdownToHtml(unittest.TestCase):
    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(Path(self.test_output))
        self.config = load_config(self.test_output / "site-config.toml")

    def tearDown(self):
        import shutil
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        self.dirs = None
        self.config = None
    def test_empty_text(self):
        result = md_to_html(self.dirs, "", self.config)
        self.assertEqual(result.strip(), "")

    def test_just_text(self):
        text = "Plain text without markdown."
        result = md_to_html(self.dirs, text, self.config)
        self.assertIn("Plain text", result)

    def test_escaped_special_chars(self):
        text = "Text with & ampersand < and > symbols."
        result = md_to_html(self.dirs, text, self.config)
        self.assertIn("Text", result)

    def test_code_block_preserved(self):
        text = "Text\n```\ncode\n```\nmore text"
        result = md_to_html(self.dirs, text, self.config)
        self.assertIn("code", result)

    def test_code_block_highlighted(self):
        text = "```python\ncode\n```"
        result = md_to_html(self.dirs, text, self.config)
        self.assertIn('class="highlight"', result)

    def test_code_block_escaped(self):
        text = "```python\nprint('<script>')\n```"
        result = md_to_html(self.dirs, text, self.config)
        self.assertIn("&lt;script&gt;", result)


if __name__ == "__main__":
    unittest.main()
