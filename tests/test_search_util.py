from util.search_util import sanitize_search_query


def test_sanitize_search_query_strips_and_truncates():
    q = '";waitfor delay \'0:0:5\'--' + "x" * 200
    out = sanitize_search_query(q)
    assert "waitfor" in out
    assert len(out) <= 120
    assert "\x00" not in out
