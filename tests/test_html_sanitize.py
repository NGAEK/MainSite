from util.html_sanitize import sanitize_template_html


def test_sanitize_removes_contenteditable():
    raw = '<div class="header-wrapper" contenteditable="true" spellcheck="true"><header>Hi</header></div>'
    out = sanitize_template_html(raw)
    assert "contenteditable" not in out
    assert "spellcheck" not in out
    assert "<header>Hi</header>" in out


def test_sanitize_removes_constructor_id():
    raw = '<div id="constructor-editable-body" class="constructor-preview-bleed"><p>x</p></div>'
    out = sanitize_template_html(raw)
    assert "constructor-editable-body" not in out
    assert "constructor-preview-bleed" not in out
