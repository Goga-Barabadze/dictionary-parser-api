import pytest

from src.logic.declutter import *


@pytest.mark.parametrize("test_input, expected", [
    ("\n", "\n"),
    ("\n" * 2, "\n"),
    ("A" + "\n" * 2, "A" + "\n" * 2),
    ("\n" * 3, "\n"),
    ("\n" * 3 + "hello", "\nhello"),
    ("\n" * 10 + "hello", "\nhello"),
    ("\n" * 3 + "hello" + "\n", "\nhello\n"),
    ("\n" * 3 + "hello" + "\n" * 20, "\nhello\n"),
    ("\r\n", "\r\n"),
    ("\r\n" * 10, "\n")
])
def test_declutter_from_linebreaks(test_input, expected):
    assert declutter_from_linebreaks(test_input) == expected


@pytest.mark.parametrize("test_input", [dict(), list(), 10, 1.0, False])
def test_declutter_from_linebreaks_type(test_input):
    with pytest.raises(TypeError):
        declutter_from_linebreaks(test_input)


@pytest.mark.parametrize("test_input, expected", [
    ("<mediawiki\">", ""),
    ("<mediawiki hello how are you today \n? \n \n \">", ""),
    ("<siteinfo></siteinfo>", ""),
    ("<siteinfo>This is a \n sample text</siteinfo>", ""),
    ("<siteinfo>This is a \n sample text</siteinfo>Hello, I am a survivor",
     "Hello, I am a survivor"),
    ("<page>\n    <title>Nothing special</title></page>\n<page>",
     "<page>\n    <title>Nothing special</title></page>\n<page>"),
    ("<page>\n    <title>something:special</title></page>\n<page>", "<page>"),
    ("<page>\n    <title>something#special too</title></page>\n<page>", "<page>"),
    ("</mediawiki>", ""),
    ("</mediawiki>hello</mediawiki>", "hello"),
    ("&lt;ref&gt;&lt;/ref&gt;", ""),
    ("&lt;ref&gt; hier kann alles stehen &lt;/ref&gt;", "")
])
def test_declutter_universally_redundant_parts(test_input, expected):
    assert declutter_universally_redundant_parts(test_input) == expected


@pytest.mark.parametrize("test_input", [1, dict(), True, -1.5])
def test_declutter_universally_redundant_parts_type(test_input):
    with pytest.raises(TypeError):
        declutter_universally_redundant_parts(test_input)


@pytest.mark.parametrize("test_input, expected", [
    ("</revision>\n<page>", "</revision>\n  </page>\n  <page>"),
    ("</revision>\n</page>\n<page>", "</revision>\n</page>\n<page>"),
    ("</revision>\n\n\n<page>", "</revision>\n  </page>\n  <page>")
])
def test_close_unclosed_pages(test_input, expected):
    assert close_unclosed_pages(test_input) == expected


@pytest.mark.parametrize("test_input", [dict(), list(), 10, True])
def test_close_unclosed_pages_type(test_input):
    with pytest.raises(TypeError):
        close_unclosed_pages(test_input)


@pytest.mark.parametrize("text, columns, expected", [
    ("abc", ["en", "abc"], ""),
    ("abc", ["de", "a", "b"], "c"),
    ("hello\n my name is Goga", ["fr", r"h[\s\S]*?(?=\n)"], "\n my name is Goga")
])
def test_declutter_with_regex_instructions(text, columns, expected):
    assert declutter_with_regex_instructions(text, columns) == expected


@pytest.mark.parametrize("text, columns", [
    (dict(), ["en", "abc"]),
    ("abc", [1, 2, 3])
])
def test_declutter_with_regex_instructions_type(text, columns):
    with pytest.raises(TypeError):
        declutter_with_regex_instructions(text, columns)
