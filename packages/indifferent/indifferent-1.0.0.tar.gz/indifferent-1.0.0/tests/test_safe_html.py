from indifferent.indifferent import _safe_html


def test_empty():
    assert _safe_html("") == ""


def test_safe():
    assert _safe_html("tabby cat") == "tabby cat"


def test_escape_html():
    assert _safe_html("cat->tabby") == "cat-&gt;tabby"


def test_line_breaks():
    assert _safe_html("tabby\ncat") == "tabby<br />cat"


def test_tabs_to_spaces():
    assert _safe_html("\tcat") == "&nbsp;&nbsp;&nbsp;&nbsp;cat"
