"""Рендер страницы MainSite для превью в админ-конструкторе."""
from __future__ import annotations

import re
from html import unescape

_TITLE_RE = re.compile(r"<title[^>]*>([\s\S]*?)</title>", re.IGNORECASE)
_H1_RE = re.compile(r"<h1[^>]*class=\"[^\"]*(?:static-page-title|branch-page-title)[^\"]*\"[^>]*>([\s\S]*?)</h1>", re.IGNORECASE)
_BODY_CLASS_RE = re.compile(
    r"<div[^>]*class=\"[^\"]*(?:static-page-body|branch-page-panel)[^\"]*\"[^>]*>([\s\S]*?)</div>",
    re.IGNORECASE,
)
_MAIN_RE = re.compile(r"<main[^>]*>([\s\S]*?)</main>", re.IGNORECASE)
_BLOCK_CONTENT_RE = re.compile(
    r"\{%-?\s*block\s+content\s*-?%\}([\s\S]*?)\{%-?\s*endblock\s*-?%\}",
    re.IGNORECASE,
)


def extract_preview_html(full_html: str) -> str:
    """Выделяет редактируемое тело страницы из полного HTML ответа."""
    text = str(full_html or "")
    if not text.strip():
        return ""
    for pattern in (_BODY_CLASS_RE, _MAIN_RE):
        match = pattern.search(text)
        if match and match.group(1).strip():
            return match.group(1).strip()
    body_match = re.search(r"<body[^>]*>([\s\S]*?)</body>", text, re.IGNORECASE)
    if body_match:
        inner = body_match.group(1).strip()
        if inner:
            return inner
    return text.strip()


def extract_preview_title(full_html: str) -> str:
    text = str(full_html or "")
    match = _H1_RE.search(text)
    if match:
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = unescape(title).strip()
        if title:
            return title
    match = _TITLE_RE.search(text)
    if match:
        title = unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()
        if title:
            return title
    return ""


def render_route_preview(app, route: str, lang: str = "ru") -> dict | None:
    """GET маршрута через test_client; возвращает content_html как на сайте."""
    path = str(route or "").strip() or "/"
    if not path.startswith("/"):
        path = f"/{path}"
    query = f"?lang={lang}" if lang and lang != "ru" else ""
    url = f"{path}{query}" if "?" not in path else path
    with app.test_client() as client:
        response = client.get(url)
    if response.status_code != 200:
        return None
    full_html = response.get_data(as_text=True)
    content_html = extract_preview_html(full_html)
    if not content_html.strip():
        return None
    return {
        "route": path.split("?")[0],
        "title": extract_preview_title(full_html),
        "content_html": content_html,
    }
