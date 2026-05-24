from api import locale_content as lc


def test_unwrap_body_html_strips_wrapper():
    raw = "<html><body><section><p>Текст</p></section></body></html>"
    assert "<p>Текст</p>" in lc.unwrap_body_html(raw)


def test_resolve_namespace_migrated_slug():
    ns = lc.resolve_namespace("istoriya", "/pages/istoriya")
    assert ns == "migrated"


def test_get_locale_page_istoriya_has_body():
    page = lc.get_locale_page("istoriya", "/pages/istoriya")
    assert page is not None
    assert page["namespace"] == "migrated"
    assert page["has_content"]
    assert "1946" in page["content_html"]
