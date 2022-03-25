import copy

from src.model.Model import *


def save_to_dictionary(pages: [Page]):

    dictionary = {}

    for page in pages:
        dictionary[page.title] = {"page": page}

    add_references(dictionary, pages)

    return dictionary


def add_references(dictionary, _pages):
    def smart_access_dict(_indices, _dictionary, offset=0):
        if _indices[offset] not in _dictionary and len(_indices) != 1:
            _dictionary[_indices[offset]] = dict()

        if len(_indices) - 1 == offset:
            return

        if len(_indices) - 2 == offset:
            if _indices[offset + 1] in _dictionary[_indices[offset]]:
                return
            arr = _indices[offset + 1] if type(_indices[offset + 1]) == list else [_indices[offset + 1]]
            if type(_dictionary[_indices[offset]]) == dict:
                _dictionary[_indices[offset]] = arr
            else:
                _dictionary[_indices[offset]] += arr
        else:
            smart_access_dict(_indices, _dictionary[_indices[offset]], offset + 1)

    for _page in _pages:
        for _word in _page.words:

            # Three kinds of redirects:
            # 1. Pointing back to this page because this is the lemma. Point back to me
            # derivatives, outdated_forms, secondary_forms
            for _word_form in _word.word_forms_which_point_back():
                if _word_form == _page.title:
                    continue
                smart_access_dict([_word_form, "redirects", _page.title], dictionary)

            # 2. Pointing to another page because this is derived form. Point away
            # grammar_forms, root_words, translations
            for _word_form in _word.word_forms_which_point_away():
                if _word_form == _page.title or _word_form not in dictionary:
                    continue
                smart_access_dict([_page.title, "redirects", _word_form], dictionary)

            # 3. Related. Point away and back to me.
            # female_word_forms, male_word_forms
            for _word_form in _word.word_forms_related():
                smart_access_dict([_page.title, "redirects", _word_form], dictionary)
                smart_access_dict([_word_form, "redirects", _page.title], dictionary)


# TODO: Add case-insensitive support
# Proof of concept function
def look_up(_text, _dictionary, _depth=2, _history=[]):
    if _depth == 0:
        return
    if len(_history) != 0 and _text in _history:
        return
    if type(_text) != str:
        raise TypeError("Text must be a string.")
    if type(_dictionary) != dict:
        raise TypeError("Dictionary must be a dict.")

    if " " in _text:
        for word in _text.split(" "):
            look_up(word, _dictionary, _depth=_depth)
        return

    if _text not in _dictionary:
        print("No result found")
        return

    if _text in _dictionary and "page" in _dictionary[_text]:
        page = _dictionary[_text]["page"]
        for word in page.words:
            print(f"{word.language}, {page.title} ({word.part_of_speech})")
            for definition in word.definitions:
                print(f"\t{definition.description}")

    if _text in _dictionary and "redirects" in _dictionary[_text]:
        for redirect_to in _dictionary[_text]["redirects"]:
            copied_history = copy.deepcopy(_history)
            copied_history.append(_text)
            look_up(redirect_to, _dictionary, _depth=_depth - 1, _history=copied_history)


def has_at_least_one_definition(_text, _dictionary, _depth=20, _history=[]):
    if _text not in _dictionary:
        return False

    if _text in _dictionary and "page" in _dictionary[_text]:
        page = _dictionary[_text]["page"]
        for word in page.words:
            if len(word.definitions) > 0:
                return True

    if _text in _dictionary and "redirects" in _dictionary[_text]:
        for redirect_to in _dictionary[_text]["redirects"]:
            copied_history = copy.deepcopy(_history)
            copied_history.append(_text)

            result = has_at_least_one_definition(redirect_to, _dictionary, _depth=_depth - 1, _history=copied_history)

            if result:
                return True

    return False
