from util.locale_routes import resolve_locale_key_path
from util.locale_search import (
    href_with_lang,
    search_content_pages,
    search_localized_site,
    search_locale_strings,
)


def test_href_with_lang_fragment_after_query():
    assert href_with_lang("/", "administration", "be") == "/?lang=be#administration"
    assert href_with_lang("/contacts", "", "ru") == "/contacts"


def test_locale_search_finds_director_surname():
    hits = search_locale_strings("Трус", "ru")
    paths = {h["path"] for h in hits}
    assert "teachers.director_name" in paths
    director = next(h for h in hits if h["path"] == "teachers.director_name")
    assert director["href"].startswith("/")
    assert "administration" in director["href"]


def test_locale_search_empty_query():
    assert search_locale_strings("   ", "ru") == []
    assert search_locale_strings("", "be") == []


def test_resolve_applicants_documents_page():
    assert resolve_locale_key_path("applicants.pages.dokumenty_postupleniya") == (
        "/applicants/dokumenty-dlya-postupleniya",
        "",
    )


def test_resolve_nav_documents():
    assert resolve_locale_key_path("nav.documents") == ("/applicants/dokumenty-dlya-postupleniya", "")


def test_locale_search_dokumenty_includes_admission_page():
    hits = search_locale_strings("документы", "ru")
    hrefs = {h["href"] for h in hits}
    assert any("dokumenty-dlya-postupleniya" in x for x in hrefs)


def test_content_search_finds_body_text():
    hits = search_content_pages("цикловых", "ru")
    paths = {h["path"] for h in hits}
    assert "migrated.education-cycle-commissions" in paths
    assert hits[0]["href"] == "/pages/education-cycle-commissions"


def test_content_search_finds_migrated_corruption_page():
    hits = search_content_pages("антикоррупц", "ru")
    assert any(h["path"] == "migrated.antikorruptsionnaya-deyatelnost" for h in hits)


def test_localized_site_merges_messages_and_content():
    hits = search_localized_site("Трус", "ru")
    paths = {h["path"] for h in hits}
    assert "teachers.director_name" in paths
    assert "migrated.education-cycle-commissions" in paths
