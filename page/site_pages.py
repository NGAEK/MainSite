"""Статические страницы: политика ПДн, одно окно, карта сайта."""
from flask import render_template
import logging
import os
from db import news_repository
from db import tabs_repository
from db import pages_repository
from page.site_mirror_config import SITE_PAGE_MIRROR

logger = logging.getLogger(__name__)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MIRROR_DIR = os.path.join(_ROOT, "data", "site_pages_mirror")


def _managed_page_or_template(slug: str, fallback_template: str):
    page = pages_repository.get_page_by_slug(slug)
    if page and bool(page.get("is_active")):
        return render_template("pages/managed_page.html", page=page)
    mirrored = _mirrored_page(slug)
    if mirrored:
        return render_template("pages/managed_page.html", page=mirrored)
    return render_template(fallback_template)


def _mirrored_page(slug: str):
    path = os.path.join(_MIRROR_DIR, f"{slug}.html")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            content_html = f.read()
    except OSError:
        return None
    title = (SITE_PAGE_MIRROR.get(slug) or {}).get("title") or slug.replace("-", " ").title()
    return {"title": title, "content_html": content_html}


def privacy_handler(request):
    return _managed_page_or_template("privacy", "pages/privacy.html")


def one_window_handler(request):
    return _managed_page_or_template("one-window", "pages/one_window.html")


def sitemap_handler(request):
    try:
        news_list = news_repository.get_all_news()
    except Exception as e:
        logger.warning("sitemap: не удалось загрузить новости: %s", e)
        news_list = []
    return render_template("pages/sitemap.html", news_list=news_list)


def contacts_handler(request):
    return _managed_page_or_template("contacts", "pages/contacts.html")


def cookies_handler(request):
    return _managed_page_or_template("cookies", "pages/cookies.html")


def specialties_handler(request):
    return _managed_page_or_template("specialties", "pages/specialties.html")


def custom_page_handler(request, slug: str):
    page = pages_repository.get_page_by_slug(slug)
    if page and bool(page.get("is_active")):
        return render_template("pages/managed_page.html", page=page)
    mirrored = _mirrored_page(slug)
    if mirrored:
        return render_template("pages/managed_page.html", page=mirrored)
    tab = tabs_repository.get_tab_by_slug(slug)
    if not tab or not bool(tab.get("is_active")):
        return render_template("errors/404.html"), 404
    return render_template("pages/custom_tab.html", tab=tab)
