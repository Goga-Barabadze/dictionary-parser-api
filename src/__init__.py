"""
The main entrypoint of this project
"""

import os

from pathlib import Path
from box import Box

from src.routine import routine
from src.utils.runners import *

from src.model.Word import Word

config = Box.from_yaml(filename='../config.yaml')

root_directory = os.path.dirname(Path(__file__).parent)
dump_folder_path = root_directory + "/" + config.paths.dumpsFolder
files = os.listdir(dump_folder_path)

NAMESPACE_LITERAL_FOR_WIKTIONARY_WORD_PAGE = 0

for current_filepath in files:
    filepath = dump_folder_path + current_filepath

    if not filepath.endswith(".xml"):
        continue

    with open(filepath, "r", encoding="utf-8") as file:
        file_content_buffer = ""
        word_count = 0
        failure_count = 0
        redirect_buffer = {}

        dump_created_at = run(routine["meta"]["dumped_at"], current_filepath)

        file_content_buffer += file.readline()
        dump_file_language_code = run(routine["meta"]["language_code"], file_content_buffer)

        while file.readable():

            if failure_count >= 10000:
                break

            for _ in range(25):
                if file.readable():
                    file_content_buffer += file.readline()

            if len(file_content_buffer) % 50 != 0:
                file_content_buffer = ""
                continue

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
                redirect_buffer[page_title] = page_redirect
                continue

            page_content = run(routine["parse"]["page_content"], page[50:])

            print(page_id + " - " + page_title + " - " + str(word_count))
            print(page_content)