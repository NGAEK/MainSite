"""Раздел «Учащимся»: структура меню и страницы с зеркалированным контентом."""
from __future__ import annotations

import logging
import os
import re
from flask import abort, render_template

from page.student_mirror_config import STUDENT_SLUGS, STUDENT_SOURCE_PATHS

logger = logging.getLogger(__name__)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MIRROR_DIR = os.path.join(_ROOT, "data", "students_mirror")
_LEGACY_BASE = "https://ngaek.by/index.php/ru/"

# Ключи в t.students.pages (messages.json)
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
    path = os.path.join(_MIRROR_DIR, f"{slug}.html")
    if not os.path.isfile(path):
        logger.error("students: нет зеркала для slug=%s (%s)", slug, path)
        abort(404)
    with open(path, encoding="utf-8") as f:
        body_html = f.read()
    body_html = _sanitize_loaded_fragment(body_html)
    title_key = SLUG_TO_TITLEKEY.get(slug)
    legacy_url = _LEGACY_BASE + STUDENT_SOURCE_PATHS[slug]
    return render_template(
        "pages/students_article.html",
        slug=slug,
        title_key=title_key,
        body_html=body_html,
        legacy_url=legacy_url,
    )


def _sanitize_loaded_fragment(html: str) -> str:
    """На случай устаревших файлов без постобработки в fetch-скрипте."""
    html = re.sub(
        r'<div\s+class="socbuttons"[^>]*>.*?</div>\s*</div>\s*<div\s+style="clear:both;"></div>',
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"</footer\s*>", "", html, flags=re.IGNORECASE)
    html = html.replace("https://ngaek.by/..\\docs\\", "https://ngaek.by/docs/")
    html = html.replace("https://ngaek.by/../docs/", "https://ngaek.by/docs/")
    return html
