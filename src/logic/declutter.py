import re


def declutter_with_regex_instructions(text, csv_line):
    if type(text) != str:
        raise TypeError("Text must be a string.")

    if type(csv_line) != list:
        raise TypeError("Csv-line must be a string.")

    # Skip over first because it's the language code
    regex_columns = range(1, len(csv_line))

    for column in regex_columns:
        declutter_regex_instruction = csv_line[column]
        print(declutter_regex_instruction)
        text = re.sub(declutter_regex_instruction, "", text)

    return declutter_from_linebreaks(text)


def close_unclosed_pages(text):
    if type(text) != str:
        raise TypeError("Text must be a string.")

    return re.sub(
        r"</revision>(\n\r|\n)*?<page>",
        r"</revision>\n  </page>\n  <page>",
        text
    )


def declutter_universally_redundant_parts(text):
    if type(text) != str:
        raise TypeError("Text must be a string.")

    text = close_unclosed_pages(text)

    universal_regex = [
        (r"<mediawiki[\s\S]*?\">", r""),
        (r"<siteinfo>[\s\S]*?<\/siteinfo>", r""),
        (r"<page>\n    <title>[\S]*?(:|#)[\s\S]*?(?=<page>|\Z)", r""),
        (r"<\/mediawiki>", r""),
        (r"&lt;ref&gt;[\s\S]*?&lt;\/ref&gt;", r""),
        ("&quot;", "\"")
    ]

    for regex, replace_string in universal_regex:
        print(regex)
        text = re.sub(regex, replace_string, text)

    return declutter_from_linebreaks(text)


def declutter_from_linebreaks(text):
    if type(text) != str:
        raise TypeError("Text must be a string.")

    return re.sub(
        r"(\n|\r\n){3,}|\A(\n|\r\n){2,}",
        r"\n",
        text
    )
