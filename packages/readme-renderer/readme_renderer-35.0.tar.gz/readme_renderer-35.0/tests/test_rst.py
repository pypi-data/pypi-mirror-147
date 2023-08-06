import io
import glob
import os.path

import pytest

from readme_renderer.rst import render


@pytest.mark.parametrize(
    ("rst_filename", "html_filename"),
    [
        (fn, os.path.splitext(fn)[0] + ".html")
        for fn in glob.glob(
            os.path.join(os.path.dirname(__file__), "fixtures", "test_*.rst")
        )
    ],
)
def test_rst_fixtures(rst_filename, html_filename):
    # Get our Markup
    with io.open(rst_filename, encoding='utf-8') as f:
        rst_markup = f.read()

    # Get our expected
    with io.open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    out = render(rst_markup)

    if "<" in expected:
        assert out == expected
    else:
        assert out is None


def test_rst_001():
    assert render('Hello') == '<p>Hello</p>\n'


def test_rst_002():
    assert render('http://mymalicioussite.com/') == (
        '<p><a href="http://mymalicioussite.com/" rel="nofollow">'
        'http://mymalicioussite.com/</a></p>\n'
    )


def test_rst_raw():
    warnings = io.StringIO()
    assert render("""
.. raw:: html
    <script>I am evil</script>

""", stream=warnings) is None

    assert '"raw" directive disabled' in warnings.getvalue()


def test_rst_empty_file():
    warnings = io.StringIO()
    assert render("", stream=warnings) is None

    assert "No content rendered from RST source." in warnings.getvalue()


def test_rst_header_only():
    warnings = io.StringIO()
    assert render("""
Header
======
""", stream=warnings) is None

    assert "No content rendered from RST source." in warnings.getvalue()


def test_header_and_malformed_emits_docutils_warning_only():
    warnings = io.StringIO()
    assert render("""
Header
======

======
""", stream=warnings) is None

    assert len(warnings.getvalue().splitlines()) == 1
    assert "No content rendered from RST source." not in warnings.getvalue()
