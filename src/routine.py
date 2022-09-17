from src.functions import language_code_of_dump_file, dump_file_created_at, pages, page, namespace, page_title, page_id, \
    page_redirect, page_content, page_language_sections, part_of_speech_sections
from src.constants.regular_expressions import FIND_ALL_PART_OF_SPEECH_SECTIONS_ENGLISH, \
    FIND_ALL_PART_OF_SPEECH_SECTIONS_GERMAN

routine = {
    "meta": {
        "language_code": {language_code_of_dump_file},
        "dumped_at": {dump_file_created_at}
    },
    "before": {

    },
    "parse": {
        "pages": {pages},
        "page": {page},
        "namespace": {namespace},
        "page_title": {page_title},
        "page_id": {page_id},
        "page_redirect": {page_redirect},
        "page_content": {page_content},
        "page_language_sections": {page_language_sections},
        "part_of_speech_sections": {
            "en": {
                "func": part_of_speech_sections,
                "vars": {FIND_ALL_PART_OF_SPEECH_SECTIONS_ENGLISH},
            },
            "de": {
                "func": part_of_speech_sections,
                "vars": {FIND_ALL_PART_OF_SPEECH_SECTIONS_GERMAN},
            }
        }
    },
    "after": {

    },
}
