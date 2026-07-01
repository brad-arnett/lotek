"""Site configuration for lotek.run."""

import os
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo
from lotek.lib.logger import log

try:
    import tomllib
except ImportError:
    import tomli as tomllib


ROOT = Path(__file__).parent.parent
DEFAULT_CONFIG_TEMPLATE_PATH = ROOT / "site-default.toml"


def _ns(d):
    if isinstance(d, dict):
        return SimpleNamespace(**{k: _ns(v) for k, v in d.items()})
    if isinstance(d, list):
        return [_ns(i) for i in d]
    return d


def _load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def _merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, val in override.items():
        if isinstance(val, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **val}
        else:
            merged[key] = val
    return merged


def load_config(config_path=None):
    if config_path is None:
        config_path = Path(os.getcwd()) / "site-config.toml"
    if not config_path.exists():
        log.warning("config not found at %s, creating from template...", config_path)
        config_path.write_text(DEFAULT_CONFIG_TEMPLATE_PATH.read_text())

    defaults = _load_toml(DEFAULT_CONFIG_TEMPLATE_PATH).get("site", {})
    user = _load_toml(config_path).get("site", {})
    cfg = _ns(_merge(defaults, user))
    return cfg
