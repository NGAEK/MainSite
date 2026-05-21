"""Раздел «Абитуриентам»: контент из static/locales/content.json."""
from __future__ import annotations

import logging
from flask import abort, render_template

from page.applicant_mirror_config import APPLICANT_SLUGS
from util.locale_search import href_with_lang

logger = logging.getLogger(__name__)

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

    from app import get_locale, get_translations

    lang = get_locale()
    tr = get_translations()
    if slug not in (tr.get("applicants_mirror") or {}):
        logger.error("applicants: нет контента в content.json для slug=%s", slug)
        abort(404)

    title_key = SLUG_TO_TITLEKEY.get(slug)
    title_override = None
    if title_key:
        title_override = (tr.get("applicants") or {}).get("pages", {}).get(title_key)

    page_title = title_override or tr["applicants_mirror"][slug]["title"]
    breadcrumbs = [
        {"label": tr["nav"]["home"], "url": href_with_lang("/", "", lang)},
        {"label": tr["nav"]["enrollee"], "url": href_with_lang("/applicants", "", lang)},
        {"label": page_title, "url": None},
    ]

    return render_template(
        "pages/content_page.html",
        content_namespace="applicants_mirror",
        content_key=slug,
        title_override=title_override,
        breadcrumbs=breadcrumbs,
        section_class="section bg-light branch-page",
        inner_class="container",
        title_class="branch-page-title",
        body_class="legacy-article-content static-page-body branch-page-panel branch-page-panel--article",
        back_href=href_with_lang("/applicants", "", lang),
        back_label=tr.get("applicants", {}).get("back_to_hub"),
        back_class="branch-page-actions",
    )
