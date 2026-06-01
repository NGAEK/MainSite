"""Общая логика поиска для веб-страницы и API."""
from __future__ import annotations

import re

_MAX_QUERY_LEN = 120
_TAG_RE = re.compile(r"<[^>]+>")
_SUPPORTED_LANGS = frozenset({"ru", "be", "en"})


def sanitize_search_query(query: str) -> str:
    """Ограничивает длину и убирает управляющие символы (сканеры/SQLi в логах)."""
    q = (query or "").replace("\x00", "").strip()
    if len(q) > _MAX_QUERY_LEN:
        q = q[:_MAX_QUERY_LEN]
    return q


def normalize_search_lang(lang: str | None, cookie_lang: str | None = None) -> str:
    candidate = (lang or cookie_lang or "ru").strip().lower()
    return candidate if candidate in _SUPPORTED_LANGS else "ru"
