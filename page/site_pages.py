"""Статические страницы: политика ПДн, одно окно, карта сайта."""
from flask import render_template
import logging
from db import news_repository
from db import tabs_repository
from db import pages_repository
from page.migrated_pages import migrated_slugs

logger = logging.getLogger(__name__)


def _has_content(namespace: str, slug: str) -> bool:
    from app import get_translations

    bucket = (get_translations().get(namespace) or {})
    return slug in bucket and bool(bucket[slug].get("body"))


def _managed_page_or_template(slug: str, fallback_template: str):
    page = pages_repository.get_page_by_slug(slug)
    if page and bool(page.get("is_active")):
        return render_template("pages/managed_page.html", page=page)
    if _has_content("site_mirror", slug):
        return render_template(
            "pages/content_page.html",
            content_namespace="site_mirror",
            content_key=slug,
            show_back_home=True,
        )
    return render_template(fallback_template)


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
    if slug in migrated_slugs():
        return render_template(
            "pages/content_page.html",
            content_namespace="migrated",
            content_key=slug,
            section_class="static-page migrated-page",
            inner_class="static-page-inner",
            title_class="static-page-title",
            body_class="static-page-body",
            parent_url=None,
        )

    page = pages_repository.get_page_by_slug(slug)
    if page and bool(page.get("is_active")):
        return render_template("pages/managed_page.html", page=page)

    if _has_content("site_mirror", slug):
        return render_template(
            "pages/content_page.html",
            content_namespace="site_mirror",
            content_key=slug,
            show_back_home=True,
        )

    tab = tabs_repository.get_tab_by_slug(slug)
    if not tab or not bool(tab.get("is_active")):
        return render_template("errors/404.html"), 404
    return render_template("pages/custom_tab.html", tab=tab)
