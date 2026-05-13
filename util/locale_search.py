"""
Поиск по строкам локализации (static/locales/messages.json).
Основной контент сайта в БД не дублируется — фамилии, подписи и т.п. часто лежат только в JSON.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_MESSAGES_PATH = Path(__file__).resolve().parent.parent / "static" / "locales" / "messages.json"

_LANG_UI_TO_JSON = {"ru": "RU", "be": "BY", "en": "EN"}

# Корневой ключ messages.json -> путь на сайте (без учёта языка; якорь отдельно)
_ROOT_ROUTES: dict[str, tuple[str, str]] = {
    "teachers": ("/", "administration"),
    "contact": ("/", "contact"),
    "achievements": ("/", ""),
    "gallery": ("/", ""),
    "hero": ("/", ""),
    "specialties": ("/specialties", ""),
    "students": ("/students", ""),
    "applicants": ("/applicants", ""),
    "footer": ("/", ""),
    "header": ("/", ""),
    "nav": ("/", ""),
    "common": ("/", ""),
    "cookies": ("/cookies", ""),
    "404": ("/", ""),
    "errors": ("/", ""),
    "accessibility": ("/", ""),
    "breadcrumbs": ("/", ""),
    "news": ("/news", ""),
    "search": ("/search", ""),
    "news_detail": ("/news", ""),
    "pages": ("/", ""),
}


def href_with_lang(path: str, fragment: str, lang_ui: str) -> str:
    """Собирает URL с ?lang= так, чтобы якорь оставался в конце."""
    frag = f"#{fragment}" if fragment else ""
    if lang_ui == "ru":
        return path + frag
    sep = "&" if "?" in path else "?"
    return f"{path}{sep}lang={lang_ui}{frag}"


def _route_for_key_path(key_path: str) -> tuple[str, str]:
    """
    Возвращает (path, fragment) для ссылки.
    pages.* — эвристика по имени ключа (контакты, политика и т.д.).
    """
    parts = key_path.split(".")
    root = parts[0] if parts else ""

    if root == "pages" and len(parts) > 1:
        tail = ".".join(parts[1:]).lower()
        if "contact" in tail:
            return ("/contacts", "")
        if "privacy" in tail:
            return ("/privacy", "")
        if "cookie" in tail:
            return ("/cookies", "")
        if "specialt" in tail or "spec" in tail:
            return ("/specialties", "")
        if "sitemap" in tail:
            return ("/sitemap", "")
        if "one_window" in tail or "one-window" in tail:
            return ("/one-window", "")
        return ("/", "")

    base = _ROOT_ROUTES.get(root, ("/", ""))
    return base


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
                base, frag = _route_for_key_path(key_path)
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
    return hits


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
