"""Чтение и запись страниц из static/locales/content.json для админ API."""
from __future__ import annotations

import json
import re
from pathlib import Path

from page.migrated_pages import migrated_slugs
from util.locale_search import content_page_href

_CONTENT_PATH = Path(__file__).resolve().parent.parent / "static" / "locales" / "content.json"
_CONTENT_NAMESPACES = ("migrated", "students_mirror", "applicants_mirror", "site_mirror")
_DEFAULT_LANG = "RU"
_LANG_KEYS = ("RU", "BY", "EN")

_BODY_WRAPPER_RE = re.compile(
    r"^\s*<html[^>]*>\s*<body[^>]*>\s*<section[^>]*>([\s\S]*)</section>\s*</body>\s*</html>\s*$",
    re.IGNORECASE,
)
_SECTION_RE = re.compile(r"^\s*<section[^>]*>([\s\S]*)</section>\s*$", re.IGNORECASE)


def _is_i18n_leaf(node: object) -> bool:
    if not isinstance(node, dict):
        return False
    return isinstance(node.get("RU"), str) and isinstance(node.get("BY"), str)


def _lang_value(node: object, lang: str = _DEFAULT_LANG) -> str:
    if not _is_i18n_leaf(node):
        return ""
    return str(node.get(lang) or node.get("RU") or "").strip()


def _load_content_data() -> dict:
    if not _CONTENT_PATH.is_file():
        return {}
    with _CONTENT_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _save_content_data(data: dict) -> None:
    _CONTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _CONTENT_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def unwrap_body_html(html: str) -> str:
    """Убирает обёртки <html><body><section> для редактора."""
    s = str(html or "").strip()
    if not s:
        return ""
    m = _BODY_WRAPPER_RE.match(s)
    if m:
        return m.group(1).strip()
    m = _SECTION_RE.match(s)
    if m:
        return m.group(1).strip()
    m = re.search(r"<body[^>]*>([\s\S]*)</body>", s, re.IGNORECASE)
    if m:
        inner = m.group(1).strip()
        m2 = _SECTION_RE.match(inner)
        return m2.group(1).strip() if m2 else inner
    return s


def wrap_body_html(inner: str) -> str:
    """Формат, принятый в content.json после миграции."""
    body = str(inner or "").strip()
    if not body:
        return ""
    if _BODY_WRAPPER_RE.match(body) or re.search(r"<html[\s>]", body, re.IGNORECASE):
        return body
    return f"<html><body><section>\n\n{body}\n\n</section></body></html>"


def resolve_namespace(slug: str, route: str = "") -> str | None:
    slug = str(slug or "").strip()
    if not slug:
        return None
    data = _load_content_data()
    route_norm = str(route or "").split("?")[0].rstrip("/").lower()

    if route_norm.startswith("/students"):
        bucket = data.get("students_mirror") or {}
        return "students_mirror" if slug in bucket else None
    if route_norm.startswith("/applicants"):
        bucket = data.get("applicants_mirror") or {}
        return "applicants_mirror" if slug in bucket else None

    migrated = data.get("migrated") or {}
    site_mirror = data.get("site_mirror") or {}
    if slug in migrated and slug in migrated_slugs():
        return "migrated"
    if slug in site_mirror:
        return "site_mirror"
    if slug in migrated:
        return "migrated"
    for namespace in _CONTENT_NAMESPACES:
        if slug in (data.get(namespace) or {}):
            return namespace
    return None


def get_locale_page(slug: str, route: str = "", lang: str = _DEFAULT_LANG) -> dict | None:
    namespace = resolve_namespace(slug, route)
    if not namespace:
        return None
    data = _load_content_data()
    page = (data.get(namespace) or {}).get(slug)
    if not isinstance(page, dict):
        return None
    title = _lang_value(page.get("title"), lang)
    body_raw = _lang_value(page.get("body"), lang)
    body_inner = unwrap_body_html(body_raw)
    route_out = content_page_href(namespace, slug)
    return {
        "slug": slug,
        "namespace": namespace,
        "route": route_out,
        "title": title,
        "content_html": body_inner,
        "body_wrapped": body_raw,
        "has_content": bool(body_inner.strip()),
    }


def list_locale_pages() -> list[dict]:
    data = _load_content_data()
    items: list[dict] = []
    for namespace in _CONTENT_NAMESPACES:
        bucket = data.get(namespace)
        if not isinstance(bucket, dict):
            continue
        for slug, page in bucket.items():
            if not isinstance(page, dict):
                continue
            title = _lang_value(page.get("title"))
            body_inner = unwrap_body_html(_lang_value(page.get("body")))
            if not title and not body_inner.strip():
                continue
            items.append(
                {
                    "slug": slug,
                    "namespace": namespace,
                    "route": content_page_href(namespace, slug),
                    "title": title or slug,
                    "has_content": bool(body_inner.strip()),
                }
            )
    items.sort(key=lambda row: (row["namespace"], row["route"]))
    return items


def update_locale_page(
    slug: str,
    *,
    route: str = "",
    title: str | None = None,
    content_html: str | None = None,
    lang: str = _DEFAULT_LANG,
) -> dict | None:
    namespace = resolve_namespace(slug, route)
    if not namespace:
        return None
    data = _load_content_data()
    bucket = data.setdefault(namespace, {})
    page = bucket.get(slug)
    if not isinstance(page, dict):
        page = {"title": {k: slug for k in _LANG_KEYS}, "body": {k: "" for k in _LANG_KEYS}}
        bucket[slug] = page

    if title is not None:
        title = str(title).strip()
        for key in _LANG_KEYS:
            node = page.setdefault("title", {})
            if not isinstance(node, dict):
                node = {}
                page["title"] = node
            if not _is_i18n_leaf(node):
                node = {k: "" for k in _LANG_KEYS}
                page["title"] = node
            node[key] = title

    if content_html is not None:
        wrapped = wrap_body_html(content_html)
        body_node = page.setdefault("body", {})
        if not isinstance(body_node, dict):
            body_node = {k: "" for k in _LANG_KEYS}
            page["body"] = body_node
        if not _is_i18n_leaf(body_node):
            body_node = {k: "" for k in _LANG_KEYS}
            page["body"] = body_node
        for key in _LANG_KEYS:
            body_node[key] = wrapped

    _save_content_data(data)
    return get_locale_page(slug, route, lang)
