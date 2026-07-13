"""Unit tests for warp.py"""
import hashlib
import pytest
from pathlib import Path
import tempfile

from lotek.lib.dirs import Dirs
from lotek.lib.warp import Warp, warp_content
from lotek.lib.site_config import load_config


def get_test_dirs(tmpdir):
    """Create test Dirs object with proper config."""
    cfg = load_config(Path(tmpdir) / "site-config.toml")
    cfg.site.url = "http://localhost:8000"
    cfg.site.title = "lotek.run"
    cfg.site.description = "test"

    dirs = Dirs(Path(tmpdir))
    return dirs


class TestWarp:
    """Test Warp class can_warp method."""

    def test_file_changed_returns_false(self, tmp_path):
        """Test that can_warp returns False when file is new or changed."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        # Create a test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nContent here.\n")

        # First call should return False (no hash exists yet)
        result = warp.can_warp(test_file, "posts")
        assert result is False

    def test_file_unchanged_returns_true(self, tmp_path):
        """Test that can_warp returns True when file hash matches."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        # Create a test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nContent here.\n")

        # First call creates hash
        warp.can_warp(test_file, "posts")

        # Second call should return True (hash matches)
        result = warp.can_warp(test_file, "posts")
        assert result is True

    def test_file_changed_after_edit_returns_false(self, tmp_path):
        """Test that can_warp returns False when file is modified."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        # Create a test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nContent here.\n")

        # First call creates hash
        warp.can_warp(test_file, "posts")

        # Modify the file
        test_file.write_text("# Test\n\nModified content.\n")

        # Second call should return False (hash changed)
        result = warp.can_warp(test_file, "posts")
        assert result is False

    def test_nonexistent_file_raises_error(self, tmp_path):
        """Test that can_warp raises FileNotFoundError for non-existent files."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        non_existent = tmp_path / "nonexistent.md"
        with pytest.raises(FileNotFoundError, match="No file found"):
            warp.can_warp(non_existent, "posts")

    def test_invalid_path_type_raises_error(self, tmp_path):
        """Test that can_warp raises ValueError for invalid path_type."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\n")

        with pytest.raises(ValueError, match="Invalid path type"):
            warp.can_warp(test_file, "invalid")

    def test_pages_path_type(self, tmp_path):
        """Test can_warp with 'pages' path_type."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\n")

        result = warp.can_warp(test_file, "pages")
        assert result is False

    def test_warp_dir_created(self, tmp_path):
        """Test that Warp creates LOTEK_WARP_POSTS and LOTEK_WARP_PAGES directories."""
        dirs = get_test_dirs(tmp_path)
        warp = Warp(dirs)

        assert dirs.LOTEK_WARP_PAGES.exists()
        assert dirs.LOTEK_WARP_POSTS.exists()


class TestWarpContent:
    """Test warp_content function."""

    def test_all_posts_can_warp(self, tmp_path):
        """Test that warp_content returns empty list when all posts have matching hashes."""
        dirs = get_test_dirs(tmp_path)

        # Create test posts
        post1 = tmp_path / "post1.md"
        post1.write_text("# Post 1\n\nContent 1.\n")
        post2 = tmp_path / "post2.md"
        post2.write_text("# Post 2\n\nContent 2.\n")

        # First build creates hashes
        buildable = warp_content(dirs, [post1, post2], "posts")
        assert len(buildable) == 2

        # Second call should return empty list (all can warp)
        buildable = warp_content(dirs, [post1, post2], "posts")
        assert len(buildable) == 0

    def test_some_posts_changed(self, tmp_path):
        """Test that warp_content returns changed posts only."""
        dirs = get_test_dirs(tmp_path)

        # Create test posts
        post1 = tmp_path / "post1.md"
        post1.write_text("# Post 1\n\nContent 1.\n")
        post2 = tmp_path / "post2.md"
        post2.write_text("# Post 2\n\nContent 2.\n")

        # First build creates hashes
        warp_content(dirs, [post1, post2], "posts")

        # Modify post1
        post1.write_text("# Post 1\n\nModified 1.\n")

        # Should only return post1
        buildable = warp_content(dirs, [post1, post2], "posts")
        assert len(buildable) == 1
        assert buildable[0] == post1

    def test_mixed_path_objects_and_dicts(self, tmp_path):
        """Test warp_content with both Path objects and dicts."""
        dirs = get_test_dirs(tmp_path)

        post1 = tmp_path / "post1.md"
        post1.write_text("# Post 1\n\n")

        post_dict = {"path": tmp_path / "post2.md"}
        post2 = post_dict["path"]
        post2.write_text("# Post 2\n\n")

        # First build
        warp_content(dirs, [post1, post_dict], "posts")

        # Modify post1
        post1.write_text("# Post 1\n\nModified\n")

        # Should return only changed post
        buildable = warp_content(dirs, [post1, post_dict], "posts")
        assert len(buildable) == 1
        assert buildable[0] == post1

    def test_pages_content_type(self, tmp_path):
        """Test warp_content with 'pages' content type."""
        dirs = get_test_dirs(tmp_path)

        page = tmp_path / "page.md"
        page.write_text("# Page\n\n")

        buildable = warp_content(dirs, [page], "pages")
        assert len(buildable) == 1

        # Second call should be empty
        buildable = warp_content(dirs, [page], "pages")
        assert len(buildable) == 0

    def test_empty_posts_list(self, tmp_path):
        """Test warp_content with empty posts list."""
        dirs = get_test_dirs(tmp_path)

        buildable = warp_content(dirs, [], "posts")
        assert buildable == []
