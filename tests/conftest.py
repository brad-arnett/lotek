import pytest
from lotek.lib.dirs import dirs
from lotek.lib.site_config import config


@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    """Point file lookups at package assets and pin config values so tests
    don't depend on whether a site-config.toml exists in the cwd."""
    monkeypatch.setattr(dirs, "TEMPLATES", dirs.PKG_TEMPLATES)
    monkeypatch.setattr(dirs, "STATIC", dirs.PKG_STATIC)
    monkeypatch.setattr(config.site, "url", "https://lotek.run")
    monkeypatch.setattr(config.site, "title", "lotek.run")
    monkeypatch.setattr(config.site, "description", "dispatches from the margins")
