"""
Собирает HTML-контент из templates/migrated и data/*_mirror в static/locales/content.json.
Для BY/EN пока копируется RU (как в fill_messages_en).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIGRATED_DIR = ROOT / "templates" / "migrated"
OUT = ROOT / "static" / "locales" / "content.json"

_TITLE_RE = re.compile(
    r'<h1[^>]*class="[^"]*static-page-title[^"]*"[^>]*>(.*?)</h1>',
    re.DOTALL | re.IGNORECASE,
)
_BODY_RE = re.compile(
    r'<div[^>]*class="[^"]*static-page-body[^"]*"[^>]*>(.*)</div>\s*</div>\s*</section>',
    re.DOTALL | re.IGNORECASE,
)
_BC_PARENT_RE = re.compile(r"<li><a[^>]*>([^<]+)</a></li>\s*<li><span", re.DOTALL)
_BC_CURRENT_RE = re.compile(r'aria-current="page"[^>]*>([^<]+)</span>', re.IGNORECASE)


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("/", "").strip()


def _leaf(text: str) -> dict:
    t = text.strip()
    return {"RU": t, "BY": t, "EN": t}


def _leaf_html(html: str) -> dict:
    h = html.strip()
    return {"RU": h, "BY": h, "EN": h}


def _parse_migrated(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    slug = path.stem
    title_m = _TITLE_RE.search(raw)
    body_m = _BODY_RE.search(raw)
    title = _strip_tags(title_m.group(1)) if title_m else slug.replace("-", " ").title()
    body = body_m.group(1).strip() if body_m else ""
    crumbs = {}
    if "breadcrumbs" in raw:
        pm = _BC_PARENT_RE.search(raw)
        cm = _BC_CURRENT_RE.search(raw)
        if pm:
            crumbs["parent"] = _leaf(_strip_tags(pm.group(1)))
        if cm:
            crumbs["current"] = _leaf(_strip_tags(cm.group(1)))
    entry = {"title": _leaf(title), "body": _leaf_html(body)}
    if crumbs:
        entry["breadcrumbs"] = crumbs
    return entry


def _mirror_entry(path: Path) -> dict:
    body = path.read_text(encoding="utf-8").strip()
    slug = path.stem
    title = slug.replace("-", " ").title()
    return {"title": _leaf(title), "body": _leaf_html(body)}


def main() -> None:
    data: dict = {"migrated": {}, "students_mirror": {}, "applicants_mirror": {}, "site_mirror": {}}

    for p in sorted(MIGRATED_DIR.glob("*.html")):
        if p.name == "migration_report.json":
            continue
        data["migrated"][p.stem] = _parse_migrated(p)

    for sub, key in (
        ("data/students_mirror", "students_mirror"),
        ("data/applicants_mirror", "applicants_mirror"),
        ("data/site_pages_mirror", "site_mirror"),
    ):
        d = ROOT / sub
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.html")):
            data[key][p.stem] = _mirror_entry(p)

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
