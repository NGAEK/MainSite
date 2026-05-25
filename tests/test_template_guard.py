from api.template_guard import extract_editable_content, merge_jinja_template, validate_jinja_syntax

ORIGINAL = """{% extends "base.html" %}
{% from 'macros/url.html' import u %}
{% block extra_css %}
<link rel="stylesheet" href="/static/css/foo.css">
{% endblock %}
{% block breadcrumbs %}
{% include 'partials/breadcrumbs.html' %}
{% endblock %}
{% block content %}
<section class="old">Old body</section>
{% endblock %}
{% block extra_js %}
<script src="/static/js/page.js"></script>
{% endblock %}
"""


def test_merge_body_only_preserves_extra_blocks():
    incoming = "<section class=\"new\">New body</section>"
    merged = merge_jinja_template(ORIGINAL, incoming)
    assert "{% block extra_css %}" in merged
    assert "/static/css/foo.css" in merged
    assert "{% block extra_js %}" in merged
    assert "/static/js/page.js" in merged
    assert "{% block breadcrumbs %}" in merged
    assert "New body" in merged
    assert "Old body" not in merged
    assert '{% extends "base.html" %}' in merged


def test_merge_full_template_restores_empty_extra_css():
    incoming = """{% extends "base.html" %}
{% block content %}
<p>Updated</p>
{% endblock %}
"""
    merged = merge_jinja_template(ORIGINAL, incoming)
    assert "/static/css/foo.css" in merged
    assert "<p>Updated</p>" in merged
    assert "{% block extra_js %}" in merged


def test_extract_editable_content():
    assert "Old body" in extract_editable_content(ORIGINAL)
    assert "{% block extra_css %}" not in extract_editable_content(ORIGINAL)


def test_validate_jinja_syntax_rejects_bad_ampersand():
    bad = '{% if a & b %}x{% endif %}'
    err = validate_jinja_syntax(bad, source="test.html")
    assert err is not None
    assert "test.html" in err


def test_validate_jinja_syntax_accepts_url_macro_style():
    ok = '{{ path ~ "&lang=" ~ current_lang }}'
    assert validate_jinja_syntax(ok) is None
