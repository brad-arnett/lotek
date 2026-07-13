"""config test shim"""
import pytest
import tempfile
from pathlib import Path
from lotek.lib.dirs import Dirs
from lotek.lib.site_config import load_config


@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    """Point file lookups at package assets and pin config values so tests
    don't depend on whether a site-config.toml exists in the cwd."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dirs = Dirs(Path(tmpdir))
        monkeypatch.setattr(dirs, "TEMPLATES", dirs.PKG_TEMPLATES)
        monkeypatch.setattr(dirs, "STATIC", dirs.PKG_STATIC)
        
        cfg = load_config(Path(tmpdir) / "site-config.toml")
        
        # Patch key modules
        import lotek.lib.posts as posts_module
        import lotek.lib.render as render_module
        import lotek.plugins.rss as rss_module
        import tests.test_rss as test_rss
        
        # Patch site attributes
        monkeypatch.setattr(cfg.site, "url", "https://lotek.run")
        monkeypatch.setattr(cfg.site, "title", "lotek.run")
        monkeypatch.setattr(cfg.site, "description", "a tiny static site generator")
        
        # Patch key modules
        import lotek.lib.posts as posts_module
        import lotek.lib.render as render_module
        import lotek.plugins.rss as rss_module
        import tests.test_rss as test_rss
        
        # Patch site attributes
        monkeypatch.setattr(cfg.site, "url", "https://lotek.run")
        monkeypatch.setattr(cfg.site, "title", "lotek.run")
        monkeypatch.setattr(cfg.site, "description", "a tiny static site generator")
