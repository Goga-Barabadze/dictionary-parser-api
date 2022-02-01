import re

from src.logic.dictionary import *
from src.model.Model import *


def parse_definitions(text):
    def _cleanse_definition(_text):
        regular_expressions = [
            (r":\[([0-9]*?)\]", r"\1."),
            (r"::", r"")
        ]

        for regular_expression, replace_text in regular_expressions:
            _text = re.sub(
                regular_expression,
                replace_text,
                _text
            )

        return _text

    def _split_definitions(_text):
        # Add \n to the start of the match
        _text = re.sub(r"(:\[[0-9][^a-z])", r"\n\1", _text)
        _text = _text.split("\n\n")
        _text[0] = _text[0][1:]

        # "1a. Hi\n1b. Hello" -> ["1a. Hi", "1b. Hello"]
        for _definition in _text:
            _definition = _definition.split("\n")

        return _text

    if type(text) != str:
        raise TypeError("Input must be string.")

    definitions = []

    definitions_chunk = re.findall(r"(?<={{definitions}}\n)[\s\S]*?(?=\n\n)", text)
    split_definitions = _split_definitions(definitions_chunk[0]) if len(definitions_chunk) > 0 else ""

    if len(definitions_chunk) == 0:
        return []

    for definition in split_definitions:
        definitions.append(
            Definition(_cleanse_definition(definition))
        )

    return definitions


def parse_gender(text):
    if type(text) != str:
        raise TypeError("Input must be string.")

    gender = re.findall(r"(?<={{)[\S]{1,2}(?=}})", text)

    if len(gender) != 1:
        return Gender.not_applicable

    if gender[0] == "f":
        return Gender.feminine
    elif gender[0] == "m":
        return Gender.masculine
    elif gender[0] == "n":
        return Gender.neuter
    elif gender[0] == "mf":
        return Gender.masculine_and_feminine
    else:
        return Gender.not_applicable


def parse_language(text):
    if type(text) != str:
        raise TypeError("Text must be string.")

    text = re.findall(r"(?<==== )[\s\S]*?(?====)", text)[0]
    text = re.findall(r"[^\n\S\s]*?\|[\S\s]*?}}", text)[0]
    text = re.sub(r"}}", "", text)
    text = re.findall(r"(?<=\|)[\s\S]*?(?=\n|\|)", text + "\n")

    return text[len(text) - 1]


def parse_derivation_table(text):
    if type(text) != str:
        raise TypeError("Input must be string.")

    text = re.search(r"(?<={{)[\S]*? (verb|noun|adjective|adverb) overview\n[\s\S]*?(?=}})", text)

    if text is None:
        return {}

    text = text.group(0)

    # Drop first line. it's just the overview header
    text = re.sub(r"(?<=\A)[\s\S]*?(?=\n)", "", text)

    # Create dicts with entries
    entries = re.findall(r"(?=\|)[\s\S]*?(?=\n|\Z)", text)

    dictionary = {}

    for entry in entries:
        name = re.findall(r"(?<=\|)[\s\S]*?(?==)", entry)
        word = re.findall(r"(?<==)[\s\S]*?(?=\n|\Z)", entry)

        if len(name) == 0 or len(word) == 0:
            continue

        if word[0] == "—" or word[0] == "–":
            continue

        # TODO: Make this more general, add elegant way for all languages
        # TODO: This is still not working. Still Hilfsverb in the dictionary
        if name[0] == "Genus" or "Hilfsverb" in name[0]:
            continue

        dictionary[name[0]] = word[0]

    return dictionary


def parse_root_word(text):
    if type(text) != str:
        raise TypeError("Text must be string.")

    root_words = re.findall(r"(?<={{root-form-reference\|)[\S\s]*?(?=}}|\|)", text)

    if len(text) == 0:
        return []

    return root_words


def parse_generic_word_forms(text, name):
    if type(text) != str or type(name) != str:
        raise TypeError("Inputs must be strings.")

    text = re.findall(r"(?<={{" + name + r"}}\n)[\s\S]*?(?=\n\n|\Z)", text)

    if len(text) == 0:
        return None

    lines = text[0].split("\n")

    words = []

    for line in lines:
        found_words = re.findall(r"(?<=\[\[|[\s\S]\|)[\S]*?(?=\]\])", line)

        for word in found_words:
            if "#" in word:
                words.append(re.sub(r"#[\S]*?(\n|\Z)", "", word))
            else:
                words.append(word)

    return words


def parse_section(text):
    if type(text) != str:
        raise TypeError("Input must be string.")

    part_of_speech = re.findall(r"(?<=speech\|)[\s\S]*?(?=\||}})", text)[0]
    language = parse_language(text)
    derivation_table = parse_derivation_table(text)
    root_words = parse_root_word(text)
    female_word_forms = parse_generic_word_forms(text, "female-word-form")
    male_word_forms = parse_generic_word_forms(text, "male-word-form")
    secondary_forms = parse_generic_word_forms(text, "secondary-forms")
    outdated_forms = parse_generic_word_forms(text, "outdated-forms")
    grammatical_features = parse_generic_word_forms(text, "grammatical-features")
    gender = parse_gender(text)
    definitions = parse_definitions(text)

    # TODO: Pronomina-Tabelle
    # TODO: Add support for "Flexion:" -> https://de.wiktionary.org/wiki/Hilfe:Flexionsseiten
    # TODO: Translate languages (eg "Deutsch" -> "german")
    # TODO: Übersetzungen

    return Word(
        part_of_speech,
        language,
        gender,
        definitions,
        derivation_table,
        root_words,
        female_word_forms,
        male_word_forms,
        secondary_forms,
        outdated_forms,
        grammatical_features
    )


def parse_page(text):
    title = re.findall(r"(?<=<title>)[\s\S]*?(?=<\/title>)", text)[0]

    words_in_page = re.findall(r"=== {{part-of-speech[\s\S]*?===[\s\S]*?(?=<|===)", text)
    words = []

    for word in words_in_page:
        parsed_word = parse_section(word)

        words.append(
            parsed_word
        )

    return Page(title, words)


def parse_document(content):
    pages = re.findall(r"<page>[\s\S]*?<\/page>", content)
    parsed_pages = []

    for page in pages:
        parsed = parse_page(page)
        parsed_pages.append(parsed)

    dictionary = save_to_dictionary(parsed_pages)

    pages.clear()
    parsed_pages.clear()

    # have -> komisch formatierte definitionen
    # &quot;
    # 1 -> gives back all the singular 1s and plural 1s from deriv table

    look_up("seine have", dictionary)
