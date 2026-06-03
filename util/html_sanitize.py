"""Удаление артефактов визуального редактора из HTML шаблонов."""
from __future__ import annotations

import re

_CONTENTEDITABLE_RE = re.compile(r'\s*contenteditable\s*=\s*["\'][^"\']*["\']', re.I)
_SPELLCHECK_RE = re.compile(r'\s*spellcheck\s*=\s*["\'][^"\']*["\']', re.I)
_CONSTRUCTOR_ID_RE = re.compile(r'\sid\s*=\s*["\']constructor-editable-body["\']', re.I)
_CONSTRUCTOR_DATA_RE = re.compile(
    r'\sdata-constructor-[\w-]+\s*=\s*["\'][^"\']*["\']',
    re.I,
)
_CONSTRUCTOR_PREVIEW_STYLE_RE = re.compile(
    r"<style[^>]*id\s*=\s*['\"]constructor-preview-editor-style['\"][^>]*>[\s\S]*?</style>",
    re.I,
)
_CONSTRUCTOR_BLEED_CLASS_RE = re.compile(
    r'\sclass\s*=\s*["\']constructor-preview-bleed["\']',
    re.I,
)


def sanitize_template_html(content: str) -> str:
    """Убирает contenteditable и разметку конструктора — только для публичных шаблонов."""
    text = content or ""
    if not text.strip():
        return text
    text = _CONSTRUCTOR_PREVIEW_STYLE_RE.sub("", text)
    text = _CONTENTEDITABLE_RE.sub("", text)
    text = _SPELLCHECK_RE.sub("", text)
    text = _CONSTRUCTOR_ID_RE.sub("", text)
    text = _CONSTRUCTOR_DATA_RE.sub("", text)
    text = _CONSTRUCTOR_BLEED_CLASS_RE.sub("", text)
    return text
