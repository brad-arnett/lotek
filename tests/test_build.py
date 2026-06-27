"""Test build pipeline."""

import unittest
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from lotek.lib.init import init
from lotek.lib.dirs import Dirs
from lotek.build import (
    load_posts,
    generate_posts,
    generate_index_landing,
    wipe_and_copy_to_output_dir,
    build,
)

def get_temp_dir():
    return Path(tempfile.mkdtemp())


class TestLoadPosts(unittest.TestCase):
    def setUp(self):
        self.temp_dir = get_temp_dir()
        init(self.temp_dir)
        self.dirs = Dirs(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        self.temp_dir = None
        self.dirs = None

    def test_load_posts_with_post(self):
        posts_dir = self.dirs.CONTENT_POSTS
        #posts_dir.mkdir(parents=True)
        (posts_dir / "test-post.md").write_text(
            "---\ntitle: Test Post\ndate: 2026-06-15\ndesc: Test description\n---\n\nThis is a test post.\n"
        )
        try:
            with patch("lotek.lib.posts.parse_frontmatter") as mock_pm:
                mock_pm.return_value = (
                    {"title": "Test Post", "date": "2026-06-15", "desc": "Test description"},
                    "Test body",
                )
                posts = load_posts(self.dirs, posts_dir)
                self.assertEqual(len(posts), 2)
                self.assertEqual(posts[0]["title"], "Test Post")
                self.assertEqual(posts[0]["slug"], "test-post")
                self.assertEqual(posts[0]["date"], "2026-06-15")
        finally:
            shutil.rmtree(posts_dir.parent)

    def test_load_posts_empty(self):
        posts_dir = self.dirs.CONTENT_POSTS
        #posts_dir.mkdir(parents=True)
        try:
            posts = load_posts(self.dirs, posts_dir)
            # init() creates an example post, so expect one post
            self.assertEqual(len(posts), 1)
            self.assertEqual(posts[0]["title"], "Welcome to Lotek")
        finally:
            shutil.rmtree(posts_dir.parent)

    def test_load_posts_no_directory(self):
        posts = load_posts(Dirs(Path("/tmp/nonexistent-lotek-posts-dir")))
        self.assertEqual(posts, [])

    def test_load_posts_publish_false_skipped(self):
        posts_dir = self.dirs.CONTENT_POSTS
        #posts_dir.mkdir(parents=True)
        (posts_dir / "hidden-post.md").write_text(
            "---\ntitle: Hidden Post\ndate: 2026-06-15\npublish: false\n---\n\nHidden.\n"
        )
        try:
            with patch(
                "lotek.lib.posts.parse_frontmatter",
                return_value=({"title": "Hidden Post", "date": "2026-06-15", "publish": "false"}, "Hidden body"),
            ):
                posts = load_posts(self.dirs, posts_dir)
                self.assertEqual(len(posts), 0)
        finally:
            shutil.rmtree(posts_dir.parent)

    def test_load_posts_publish_true_included(self):
        posts_dir = self.dirs.CONTENT_POSTS
        (posts_dir / "published-post.md").write_text(
            "---\ntitle: Published Post\ndate: 2026-06-15\npublish: true\n---\n\nPublished.\n"
        )
        try:
            with patch(
                "lotek.lib.posts.parse_frontmatter",
                return_value=({"title": "Published Post", "date": "2026-06-15", "publish": "true"}, "Published body"),
            ):
                posts = load_posts(self.dirs, posts_dir)
                self.assertEqual(len(posts), 2)
                self.assertEqual(posts[0]["title"], "Published Post")
        finally:
            shutil.rmtree(posts_dir.parent)

    def test_load_posts_no_publish_tag_included(self):
        posts_dir = self.dirs.CONTENT_POSTS
        #posts_dir.mkdir(parents=True)
        (posts_dir / "default-post.md").write_text(
            "---\ntitle: Default Post\ndate: 2026-06-15\n---\n\nDefault.\n"
        )
        try:
            with patch(
                "lotek.lib.posts.parse_frontmatter",
                return_value=({"title": "Default Post", "date": "2026-06-15"}, "Default body"),
            ):
                posts = load_posts(self.dirs, posts_dir)
                self.assertEqual(len(posts), 2) # +1 because init creates a welcome post
                self.assertEqual(posts[0]["title"], "Default Post")
        finally:
            shutil.rmtree(posts_dir.parent)

    def test_load_posts_mixed_publish_status(self):
        posts_dir = self.dirs.CONTENT_POSTS
        #posts_dir.mkdir(parents=True)
        (posts_dir / "published.md").write_text("Published body.")
        (posts_dir / "hidden.md").write_text("Hidden body.")
        (posts_dir / "default.md").write_text("Default body.")

        def mock_pm_side_effect(text):
            if "Published" in text:
                return ({"title": "Published Post", "date": "2026-06-15", "publish": "true"}, "Published body")
            elif "Hidden" in text:
                return ({"title": "Hidden Post", "date": "2026-06-15", "publish": "false"}, "Hidden body")
            else:
                return ({"title": "Default Post", "date": "2026-06-15"}, "Default body")

        try:
            with patch("lotek.lib.posts.parse_frontmatter", side_effect=mock_pm_side_effect):
                posts = load_posts(self.dirs, posts_dir)
                self.assertEqual(len(posts), 3) # +1 because init creates a welcome post
                titles = [p["title"] for p in posts]
                self.assertIn("Published Post", titles)
                self.assertIn("Default Post", titles)
                self.assertNotIn("Hidden Post", titles)
        finally:
            shutil.rmtree(posts_dir.parent)


class TestGeneratePosts(unittest.TestCase):
    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(self.test_output)

    def tearDown(self):
        shutil.rmtree(self.test_output)
        self.test_output = None
        self.dirs = None

    def test_generate_posts_creates_directory(self):
        posts = [{"title": "Test", "slug": "test", "date": "2026-06-15", "desc": "Desc", "body": "Body"}]
        generate_posts(self.dirs, posts, self.test_output)
        self.assertTrue((self.test_output / "posts").exists())

    def test_generate_posts_creates_html(self):
        posts = [{"title": "Test Post", "slug": "test", "date": "2026-06-15", "desc": "Desc", "body": "Body"}]
        generate_posts(self.dirs, posts, self.test_output)
        self.assertTrue((self.test_output / "posts" / "test.html").exists())

    def test_generate_posts_content(self):
        posts = [{"title": "Test Title", "slug": "test", "date": "2026-06-15", "desc": "Desc", "body": "<p>Test body</p>"}]
        generate_posts(self.dirs, posts, self.test_output)
        content = (self.test_output / "posts" / "test.html").read_text()
        self.assertIn("Test Title", content)
        self.assertIn("Test body", content)


class TestWipeAndCopyToOutputDir(unittest.TestCase):
    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(self.test_output)

    def tearDown(self):
        shutil.rmtree(self.test_output)
        self.test_output = None
        self.dirs = None


    def test_wipe_and_copy_creates_static(self):
        wipe_and_copy_to_output_dir(self.dirs, self.dirs.STATIC)
        self.assertTrue((self.test_output / "static").exists())

    def test_wipe_and_copy_contents(self):
        wipe_and_copy_to_output_dir(self.dirs, self.dirs.STATIC)
        self.assertTrue((self.test_output / "static" / "style.css").exists())

    def test_wipe_and_copy_wipes_existing(self):
        static_dir = self.dirs.STATIC # project/static
        self.dirs.OUTPUT.mkdir(exist_ok = True)
        self.dirs.OUTPUT_STATIC.mkdir(exist_ok = True)
        (self.dirs.OUTPUT_STATIC / "old.css").write_text("old")
        wipe_and_copy_to_output_dir(self.dirs, Path(self.dirs.OUTPUT))
        self.assertFalse((self.dirs.OUTPUT_STATIC / "old.css").exists())
        self.assertTrue((static_dir / "style.css").exists())


class TestGenerateIndexLanding(unittest.TestCase):
    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(Path(self.test_output))

    def tearDown(self):
        shutil.rmtree(self.test_output)

    def test_generate_index_creates_index(self):
        generate_index_landing(self.dirs, [], self.test_output)
        self.assertTrue((self.test_output / "index.html").exists())

    def test_generate_index_with_posts(self):
        posts = [{"date": "2026-06-15", "slug": "hello", "title": "Hello"}]
        generate_index_landing(self.dirs, posts, self.test_output)
        content = (self.test_output / "index.html").read_text()
        self.assertIn("Hello", content)


class TestFullBuild(unittest.TestCase):
    def setUp(self):
        self.test_output = get_temp_dir()
        init(self.test_output)
        self.dirs = Dirs(self.test_output)

    def tearDown(self):
        shutil.rmtree(self.test_output)
        self.test_output = None
        self.dirs = None

    @patch("lotek.build.wipe_and_copy_to_output_dir")
    @patch("lotek.build.generate_posts")
    @patch("lotek.build.generate_robots")
    @patch("lotek.build.generate_rss")
    @patch("lotek.build.generate_index_landing")
    @patch("lotek.build.load_posts")
    def test_build_executes_all(
        self, mock_load, mock_gen_idx, mock_rss, mock_robots, mock_posts, mock_wipe
    ):
        mock_load.return_value = []
        build(self.dirs)
        mock_load.assert_called_once()
        mock_gen_idx.assert_called_once()
        mock_rss.assert_called_once()
        mock_robots.assert_called_once()


if __name__ == "__main__":
    unittest.main()
