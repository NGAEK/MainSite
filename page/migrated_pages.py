"""Мигрированные статические страницы — контент в static/locales/content.json."""

from __future__ import annotations

import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONTENT_PATH = os.path.join(_ROOT, "static", "locales", "content.json")


def migrated_slugs() -> frozenset[str]:
    try:
        with open(_CONTENT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return frozenset((data.get("migrated") or {}).keys())
    except (OSError, json.JSONDecodeError):
        return frozenset()
