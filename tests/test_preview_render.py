from api.preview_render import extract_preview_html, render_route_preview


def test_extract_preview_html_static_body():
    html = '<div class="static-page-body"><p>Текст страницы</p></div>'
    assert "Текст страницы" in extract_preview_html(html)


def test_render_route_preview_istoriya():
    from app import app

    row = render_route_preview(app, "/pages/istoriya")
    assert row is not None
    assert "1946" in row["content_html"]


def test_render_route_preview_home():
    from app import app

    row = render_route_preview(app, "/")
    assert row is not None
    assert len(row["content_html"]) > 200
