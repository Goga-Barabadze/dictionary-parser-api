from src.Regex import Regex
from src.constants.regular_expressions import *


def language_code_of_dump_file(string):
    _language_code = Regex.findall(FIND_LANGUAGE_CODE_FOR_DUMP_REGEX, string)
    if len(_language_code) == 0:
        raise Exception("Could not find the language code for the wiktionary dump.")
    elif len(_language_code) > 1:
        raise Exception("Found more than one language code even though only one was expected.")
    return _language_code[0]


def dump_file_created_at(string):
    _created_at_string = Regex.findall(FIND_DATE_FROM_DUMP_FILE_NAME_REGEX, string)
    if len(_created_at_string) == 0:
        raise Exception("Could not find the timestamp in the filename.")
    elif len(_created_at_string) > 1:
        raise Exception("Found more than one match where only one was expected.")
    from datetime import datetime
    return datetime.strptime(_created_at_string[0], '%Y%m%d')


def pages(string):
    _pages = Regex.findall(FIND_ALL_PAGES_REGEX, string)
    if len(_pages) == 0:
        raise Exception("Could not find any pages.")
    return _pages


def page(string):
    _match = Regex.search(FIND_ALL_PAGES_REGEX, string)
    _page = string[_match.regs[0][0] : _match.regs[0][1]]
    if len(_page) == 0:
        raise Exception("Could not find any page.")
    return _page, _match.regs[0][0], _match.regs[0][1]


def namespace(string):
    _namespace = Regex.findall(FIND_NAMESPACE_REGEX, string)
    if len(_namespace) == 0:
        raise Exception("Could not find the namespace.")
    elif len(_namespace) > 1:
        raise Exception("Found more than one namespace where only one was expected.")
    return int(_namespace[0])


def page_title(string):
    _page_title = Regex.findall(FIND_PAGE_TITLE_REGEX, string)
    if len(_page_title) == 0:
        raise Exception("Could not find the page title.")
    elif len(_page_title) > 1:
        raise Exception("Found more than one page title where only one was expected.")
    return _page_title[0]


def page_id(string):
    _id = Regex.findall(FIND_PAGE_ID_REGEX, string)
    if len(_id) == 0:
        raise Exception("Could not find the page id.")
    elif len(_id) > 1:
        raise Exception("Found more than one page id where only one was expected.")
    return _id[0]


def page_redirect(string):
    _redirect = Regex.findall(FIND_PAGE_REDIRECT_REGEX, string)
    # Doesn't throw an exception if page has no redirect, few have them
    if len(_redirect) > 1:
        raise Exception("Found more than one page redirect where only one was expected.")
    return _redirect[0] if len(_redirect) == 1 else None


def page_content(string):
    _content = Regex.findall(FIND_PAGE_CONTENT_REGEX, string)
    # Doesn't throw an exception if page has no content, some don't have a text tag
    if len(_content) > 1:
        raise Exception("Found more than one page content where only one was expected.")
    return _content[0] if len(_content) == 1 else None


def page_language_sections(string):
    # Don't throw exception if nothing was found, some pages don't have sections -> it's rare tho
    return Regex.findall(FIND_ALL_PAGE_LANGUAGE_SECTIONS, string)


def part_of_speech_sections(regex, string):
    # Don't throw exception if nothing was found
    return Regex.findall(regex, string)
