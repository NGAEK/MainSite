"""
Защита Jinja-блоков в шаблонах при сохранении через API.

Редактор часто отдаёт только тело {% block content %}, из-за чего пропадают
{% block extra_css %}, {% block extra_js %}, {% block breadcrumbs %} и преамбула (extends, import).
"""
from __future__ import annotations

import re

# Блоки, которые всегда восстанавливаются из файла на диске, если в запросе пусты или отсутствуют.
PROTECTED_BLOCKS = frozenset({"extra_css", "extra_js", "breadcrumbs"})
EDITABLE_BLOCK = "content"

_BLOCK_RE = re.compile(
    r"(\{%-?\s*block\s+(\w+)\s*-?%\})(.*?)(\{%-?\s*endblock\s*-?%\})",
    re.DOTALL | re.IGNORECASE,
)
_EXTENDS_RE = re.compile(r"\{%-?\s*extends\b", re.IGNORECASE)


def _find_blocks(text: str) -> dict[str, dict[str, str]]:
    blocks: dict[str, dict[str, str]] = {}
    for m in _BLOCK_RE.finditer(text):
        name = m.group(2)
        blocks[name] = {
            "full": m.group(0),
            "inner": m.group(3),
            "open": m.group(1),
            "close": m.group(4),
        }
    return blocks


def _block_order(text: str) -> list[str]:
    return [m.group(2) for m in _BLOCK_RE.finditer(text)]


def _preamble(text: str) -> str:
    m = re.search(r"\{%-?\s*block\s+\w+", text, re.IGNORECASE)
    if not m:
        return text
    return text[: m.start()]


def _block_empty(block: dict[str, str] | None) -> bool:
    if not block:
        return True
    inner = block.get("inner") or ""
    return not inner.strip()


def _wrap_block(name: str, inner: str, template: str) -> str:
    """Формат open/end как в исходном шаблоне (если блок уже был)."""
    blocks = _find_blocks(template)
    ref = blocks.get(name)
    if ref:
        return f"{ref['open']}{inner}{ref['close']}"
    return f"{{% block {name} %}}{inner}{{% endblock %}}"


def _is_body_only(incoming: str) -> bool:
    """Только HTML/тело без каркаса extends и без набора block-ов."""
    t = incoming.strip()
    if not t:
        return True
    if _EXTENDS_RE.search(t):
        return False
    blocks = _find_blocks(t)
    if not blocks:
        return True
    if set(blocks) == {EDITABLE_BLOCK}:
        return True
    return False


def merge_jinja_template(original: str, incoming: str) -> str:
    """
    Объединяет сохранённый из API текст с текущим файлом шаблона.

    - Если в запросе только тело content — подставляет его в {% block content %} оригинала.
    - Если пришёл полный шаблон — подставляет content из запроса, остальные защищённые block-и
      берёт из original, если в запросе они пустые или отсутствуют.
    - Преамбула (extends, import, from) всегда из original, если в original она есть.
    """
    original = original or ""
    incoming = incoming or ""

    if not original.strip():
        return incoming

    orig_blocks = _find_blocks(original)
    inc_blocks = _find_blocks(incoming)

    if not orig_blocks:
        return incoming

    if _is_body_only(incoming):
        if EDITABLE_BLOCK in orig_blocks:
            new_inner = incoming.strip()
            return _replace_block_inner(original, EDITABLE_BLOCK, new_inner)
        return incoming

    order = _block_order(original)
    preamble = _preamble(original)

    new_content_inner: str | None = None
    if EDITABLE_BLOCK in inc_blocks:
        new_content_inner = inc_blocks[EDITABLE_BLOCK]["inner"]
    elif EDITABLE_BLOCK in orig_blocks:
        new_content_inner = orig_blocks[EDITABLE_BLOCK]["inner"]

    parts: list[str] = [preamble]
    for name in order:
        if name == EDITABLE_BLOCK:
            inner = new_content_inner if new_content_inner is not None else orig_blocks[name]["inner"]
            parts.append(_wrap_block(name, inner, original))
            continue

        inc = inc_blocks.get(name)
        orig = orig_blocks.get(name)
        if name in PROTECTED_BLOCKS or name != EDITABLE_BLOCK:
            if inc and not _block_empty(inc):
                parts.append(inc["full"])
            elif orig:
                parts.append(orig["full"])
            elif inc:
                parts.append(inc["full"])
        elif orig:
            parts.append(orig["full"])

    tail = _tail_after_blocks(original)
    if tail:
        parts.append(tail)
    return "".join(parts)


def _replace_block_inner(template: str, block_name: str, new_inner: str) -> str:
    def repl(m: re.Match) -> str:
        if m.group(2) != block_name:
            return m.group(0)
        return f"{m.group(1)}{new_inner}{m.group(4)}"

    return _BLOCK_RE.sub(repl, template, count=0)


def _tail_after_blocks(text: str) -> str:
    """Текст после последнего {% endblock %} (если есть)."""
    last = None
    for m in _BLOCK_RE.finditer(text):
        last = m
    if not last:
        return ""
    return text[last.end() :]


def extract_editable_content(template: str) -> str:
    """Внутренность {% block content %} для редактора (без служебных block-ов)."""
    blocks = _find_blocks(template)
    if EDITABLE_BLOCK in blocks:
        return blocks[EDITABLE_BLOCK]["inner"]
    return template
