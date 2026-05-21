"""Раздел «Учащимся»: контент из static/locales/content.json."""
from __future__ import annotations

import logging
from flask import abort, render_template

from page.student_mirror_config import STUDENT_SLUGS
from util.locale_search import href_with_lang

logger = logging.getLogger(__name__)

SLUG_TO_TITLEKEY: dict[str, str] = {
    "grafik-uchebnogo-protsessa": "grafik_uchebnogo_protsessa",
    "proizvodstvennoe-obuchenie": "proizvodstvennoe_obuchenie",
    "grafik-prokhozhdeniya-uchebnykh-i-proizvodstvennykh-praktik": "grafik_praktik",
    "pamyatka-uchashchemusya": "pamyatka_uchashchemusya",
    "obraztsy-dokumentov": "obraztsy_dokumentov",
    "kursovoe-i-diplomnoe-proektirovanie": "kursovoe_diplomnoe",
    "normativnye-dokumenty": "normativnye_dokumenty",
    "raspredelenie-i-trudoustrojstvo-vypusknikov": "raspredelenie_vypusknikov",
    "uchebnaya-programma-preddiplomnoj-praktiki": "programma_preddiplomnoj_praktiki",
    "grafik-uchebnogo-protsessa-zaochnogo-otdeleniya": "grafik_zaochnogo",
    "stoimost-obucheniya": "stoimost_obucheniya",
    "vypusknikam": "vypusknikam",
    "informatsiya-dlya-uchashchikhsya-prekrativshim-dosrochno-obrazovatelnye-otnosheniya-i-prokhodivshim-attestatsiyu-v-poryadke-eksternata": "informatsiya_eksternat",
}


def students_hub_handler(request):
    return render_template("pages/students_hub.html")


def students_article_handler(request, slug: str):
    if slug not in STUDENT_SLUGS:
        abort(404)

    from app import get_locale, get_translations

    lang = get_locale()
    tr = get_translations()
    if slug not in (tr.get("students_mirror") or {}):
        logger.error("students: нет контента в content.json для slug=%s", slug)
        abort(404)

    title_key = SLUG_TO_TITLEKEY.get(slug)
    title_override = None
    if title_key:
        title_override = (tr.get("students") or {}).get("pages", {}).get(title_key)

    page_title = title_override or tr["students_mirror"][slug]["title"]
    breadcrumbs = [
        {"label": tr["nav"]["home"], "url": href_with_lang("/", lang)},
        {"label": tr["nav"]["students"], "url": href_with_lang("/students", lang)},
        {"label": page_title, "url": None},
    ]

    return render_template(
        "pages/content_page.html",
        content_namespace="students_mirror",
        content_key=slug,
        title_override=title_override,
        breadcrumbs=breadcrumbs,
        section_class="section bg-light branch-page",
        inner_class="container",
        title_class="branch-page-title",
        body_class="legacy-article-content static-page-body branch-page-panel branch-page-panel--article",
        back_href=href_with_lang("/students", lang),
        back_label=tr.get("students", {}).get("back_to_hub"),
        back_class="branch-page-actions",
    )
