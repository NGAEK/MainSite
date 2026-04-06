from util.i18n_url import build_hreflang_url


def test_hreflang_preserves_query_and_sets_lang():
    url = build_hreflang_url(
        "http://localhost:8080/",
        "/search",
        {"q": "test", "lang": "ru"},
        "en",
    )
    assert url.startswith("http://localhost:8080/search?")
    assert "lang=en" in url
    assert "q=test" in url


def test_hreflang_root():
    url = build_hreflang_url("https://example.by/", "/", {}, "be")
    assert url == "https://example.by/?lang=be"
