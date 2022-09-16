"""
The main entrypoint of this project
"""

import os

from pathlib import Path
from box import Box

from src.model.Redirect import Redirect
from src.routine import routine
from src.utils.runners import *

from src.model.Word import Word

MAX_FAILURES_UNTIL_TERMINATION = 10000
NAMESPACE_LITERAL_FOR_WIKTIONARY_WORD_PAGE = 0

redirect_pool = []

def main():
    config = Box.from_yaml(filename='../config.yaml')

    root_directory = os.path.dirname(Path(__file__).parent)
    dump_folder_path = root_directory + "/" + config.paths.dumpsFolder
    files = os.listdir(dump_folder_path)

    for current_filepath in files:
        filepath = dump_folder_path + current_filepath

        if not filepath.endswith(".xml"):
            continue

        with open(filepath, "r", encoding="utf-8") as file:
            file_content_buffer = ""
            word_count = 0
            failure_count = 0

            dump_created_at = run(routine["meta"]["dumped_at"], current_filepath)

            file_content_buffer += file.readline()
            dump_file_language_code = run(routine["meta"]["language_code"], file_content_buffer)

            while file.readable():

                if failure_count >= MAX_FAILURES_UNTIL_TERMINATION:
                    break

                file_content_buffer = read_lines_into_buffer(file, file_content_buffer)

                try:
                    page, start, end = run(routine["parse"]["page"], file_content_buffer)
                    failure_count = 0
                except AttributeError:
                    # Didn't succeed to read, let's try again with more lines in the buffer
                    failure_count += 1
                    continue

                file_content_buffer = file_content_buffer[end + 1:]

                namespace = run(routine["parse"]["namespace"], page[30:300])

                if namespace != NAMESPACE_LITERAL_FOR_WIKTIONARY_WORD_PAGE:
                    continue

                word_count += 1

                page_title = run(routine["parse"]["page_title"], page[10:290])
                page_id = run(routine["parse"]["page_id"], page[30:500])
                page_redirect = run(routine["parse"]["page_redirect"], page[30:700])

                if page_redirect is not None:
                    redirect_pool.append(Redirect(from_word=page_title, to_word=page_redirect))
                    continue

                page_content = run(routine["parse"]["page_content"], page[50:])

                for language_section in run(routine["parse"]["page_language_sections"], page_content):
                    print(language_section)


def read_lines_into_buffer(file, file_content_buffer, number_of_lines=25):
    """Reads lines into buffer from file and returns the new buffer"""
    for _ in range(number_of_lines):
        if file.readable():
            file_content_buffer += file.readline()
    return file_content_buffer


def redirect_pool_runner():
    """
    Iterates over a set number of redirect_pool entries and writes them to the database
    if the to_word is already available.
    If the to_word is not available after the parsing is done, it deletes the entry.
    """
    for redirect_entry in redirect_pool:
        print(redirect_entry.from_word + "->" + redirect_entry.to_word)
        redirect_pool.remove(redirect_entry)


if __name__ == "__main__":
    main()
