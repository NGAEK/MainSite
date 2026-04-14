"""Статические страницы: политика ПДн, одно окно, карта сайта."""
from flask import render_template
import logging
from db import news_repository
from db import tabs_repository

logger = logging.getLogger(__name__)


def privacy_handler(request):
    return render_template("pages/privacy.html")


def one_window_handler(request):
    return render_template("pages/one_window.html")


def sitemap_handler(request):
    try:
        news_list = news_repository.get_all_news()
    except Exception as e:
        logger.warning("sitemap: не удалось загрузить новости: %s", e)
        news_list = []
    return render_template("pages/sitemap.html", news_list=news_list)


def contacts_handler(request):
    return render_template("pages/contacts.html")


def cookies_handler(request):
    return render_template("pages/cookies.html")


def specialties_handler(request):
    return render_template("pages/specialties.html")


def custom_page_handler(request, slug: str):
    tab = tabs_repository.get_tab_by_slug(slug)
    if not tab or not bool(tab.get("is_active")):
        return render_template("errors/404.html"), 404
    return render_template("pages/custom_tab.html", tab=tab)
