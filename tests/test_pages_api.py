"""API динамических страниц site_pages."""
from __future__ import annotations

from api import routes as api_routes


def test_page_row_from_payload_with_branch():
    row, err = api_routes._page_row_from_payload(
        {
            "title": "Тестовая",
            "slug": "test-page",
            "branch_id": "education",
            "content_html": "<p>x</p>",
        }
    )
    assert err is None
    assert row["slug"] == "test-page"
    assert row["branch_id"] == "education"


def test_serialize_page_adds_route():
    out = api_routes._serialize_page({"id": 1, "slug": "foo", "title": "Foo"})
    assert out["route"] == "/pages/foo"


def test_normalize_branch_id_empty():
    assert api_routes._normalize_branch_id("") is None
    assert api_routes._normalize_branch_id("education") == "education"
