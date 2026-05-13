"""
Поиск по строкам локализации (static/locales/messages.json).
Основной контент сайта в БД не дублируется — фамилии, подписи и т.п. часто лежат только в JSON.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from util.locale_routes import resolve_locale_key_path

_MESSAGES_PATH = Path(__file__).resolve().parent.parent / "static" / "locales" / "messages.json"

_LANG_UI_TO_JSON = {"ru": "RU", "be": "BY", "en": "EN"}


def href_with_lang(path: str, fragment: str, lang_ui: str) -> str:
    """Собирает URL с ?lang= так, чтобы якорь оставался в конце."""
    frag = f"#{fragment}" if fragment else ""
    if lang_ui == "ru":
        return path + frag
    sep = "&" if "?" in path else "?"
    return f"{path}{sep}lang={lang_ui}{frag}"


def _is_i18n_leaf(node: object) -> bool:
    if not isinstance(node, dict):
        return False
    if "RU" not in node or "BY" not in node:
        return False
    return isinstance(node.get("RU"), str) and isinstance(node.get("BY"), str)


def _blob_for_match(node: dict) -> str:
    chunks = []
    for k in ("RU", "BY", "EN"):
        v = node.get(k)
        if isinstance(v, str):
            chunks.append(v)
    return " ".join(chunks)


def _title_for_lang(node: dict, lang_ui: str) -> str:
    jk = _LANG_UI_TO_JSON.get(lang_ui, "RU")
    return (node.get(jk) or node.get("RU") or "").strip() or "…"


def search_locale_strings(query: str, lang_ui: str, messages_path: Path | None = None) -> list[dict]:
    """
    Ищет подстроку (без учёта регистра) во всех i18n-листьях messages.json.
    Возвращает элементы: title, excerpt, href, path (для отладки).
    """
    q = (query or "").strip()
    if not q:
        return []

    path = messages_path or _MESSAGES_PATH
    if not path.is_file():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    q_lower = q.lower()
    hits: list[dict] = []
    seen_paths: set[str] = set()

    def walk(obj: object, parts: list[str]) -> None:
        if isinstance(obj, dict):
            if _is_i18n_leaf(obj):
                key_path = ".".join(parts)
                if key_path in seen_paths:
                    return
                blob = _blob_for_match(obj)
                if q_lower not in blob.lower():
                    return
                seen_paths.add(key_path)
                base, frag = resolve_locale_key_path(key_path)
                title = _title_for_lang(obj, lang_ui)
                excerpt = _make_excerpt_plain(blob, q)
                href = href_with_lang(base, frag, lang_ui)
                hits.append(
                    {
                        "path": key_path,
                        "title": title,
                        "excerpt": excerpt,
                        "href": href,
                    }
                )
                return
            for k, v in obj.items():
                if str(k).startswith("_"):
                    continue
                walk(v, parts + [str(k)])
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, parts + [str(i)])

    walk(data, [])
    # Одна ссылка — один пункт (убираем дубли с разных ключей, напр. nav.* и applicants.pages.*)
    by_href: dict[str, dict] = {}
    for h in hits:
        href = h["href"]
        prev = by_href.get(href)
        if prev is None or len(h["path"]) > len(prev["path"]):
            by_href[href] = h
    return sorted(by_href.values(), key=lambda x: (x["title"].lower(), x["path"]))


_EXCERPT_LEN = 200
_WS_RE = re.compile(r"\s+")


def _make_excerpt_plain(text: str, query: str, length: int = _EXCERPT_LEN) -> str:
    clean = _WS_RE.sub(" ", (text or "").strip())
    idx = clean.lower().find(query.lower())
    if idx == -1:
        return clean[:length] + ("…" if len(clean) > length else "")
    start = max(0, idx - length // 3)
    end = min(len(clean), start + length)
    excerpt = clean[start:end]
    if start > 0:
        excerpt = "…" + excerpt
    if end < len(clean):
        excerpt = excerpt + "…"
    return excerpt
