from util.locale_search import href_with_lang, search_locale_strings


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
