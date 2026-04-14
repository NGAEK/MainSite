"""Раздел «Абитуриентам»: зеркалированные страницы."""
from __future__ import annotations

import logging
import os
from flask import abort, render_template

from page.applicant_mirror_config import APPLICANT_SLUGS, APPLICANT_SOURCE_PATHS
from page.student_pages import _sanitize_loaded_fragment

logger = logging.getLogger(__name__)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MIRROR_DIR = os.path.join(_ROOT, "data", "applicants_mirror")
_LEGACY_BASE = "https://ngaek.by/index.php/ru/"

SLUG_TO_TITLEKEY: dict[str, str] = {
    "spetsialnosti": "spetsialnosti",
    "kontrolnye-tsifry-priema": "kontrolnye_tsifry",
    "tselevaya-podgotovka": "tselevaya_podgotovka",
    "prokhodnye-bally": "prokhodnye_bally",
    "stoimost-obucheniya": "stoimost_obucheniya",
    "sroki-vstupitelnoj-kampanii": "sroki_kampanii",
    "dokumenty-dlya-postupleniya": "dokumenty_postupleniya",
    "normativnye-pravovye-dokumenty": "normativnye_dokumenty",
    "chasto-zadavaemye-voprosy": "chasto_voprosy",
    "goryachaya-liniya": "goryachaya_liniya",
    "konsultatsionnyj-punkt": "konsultatsionnyj_punkt",
    "trudoustrojstvo": "trudoustrojstvo",
    "obshchezhitie": "obshchezhitie",
    "organizatsiya-pitaniya": "organizatsiya_pitaniya",
}


def applicants_hub_handler(request):
    return render_template("pages/applicants_hub.html")


def applicants_article_handler(request, slug: str):
    if slug not in APPLICANT_SLUGS:
        abort(404)
    path = os.path.join(_MIRROR_DIR, f"{slug}.html")
    if not os.path.isfile(path):
        logger.error("applicants: нет зеркала для slug=%s (%s)", slug, path)
        abort(404)
    with open(path, encoding="utf-8") as f:
        body_html = f.read()
    body_html = _sanitize_loaded_fragment(body_html)
    title_key = SLUG_TO_TITLEKEY.get(slug)
    legacy_url = _LEGACY_BASE + APPLICANT_SOURCE_PATHS[slug]
    return render_template(
        "pages/applicants_article.html",
        slug=slug,
        title_key=title_key,
        body_html=body_html,
        legacy_url=legacy_url,
    )
