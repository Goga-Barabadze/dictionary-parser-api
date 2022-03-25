from pathlib import Path
from shutil import copyfile

from src.logic.parse import parse_document
from src.logic.declutter import declutter_with_regex_instructions, declutter_universally_redundant_parts
from src.logic.IndexGenerator import IndexGenerator

import re
import os
import csv
import sys


def main():
    cwd = str(Path(__file__).resolve().parent.parent)
    input_file_paths = os.listdir(cwd + "/input")

    for current_filepath in input_file_paths:

        if not current_filepath.endswith(".xml"):
            continue

        output_dict_path, input_file_path = _filepaths(cwd, current_filepath)

        if "fresh-copy" in sys.argv:
            copyfile(input_file_path, output_dict_path)

        with open(output_dict_path, 'r+', encoding="utf-8") as dict_file:

            with open(cwd + '/declutter-instructions-by-language.csv',
                      mode='r') as declutter_regex_file:

                csv_content = csv.reader(declutter_regex_file)

                dict_file_content = dict_file.read()

                for line in csv_content:

                    columns = line[0].split(';')
                    language_code = columns[0]
                    filename_without_extension = re.sub(r"\.+.+", "", current_filepath)

                    if language_code != filename_without_extension:
                        continue

                    dict_file_content = _declutter(columns, cwd, dict_file_content)

                _save_changes(dict_file, dict_file_content)

                if "parse" in sys.argv:
                    dictionary = parse_document(dict_file_content)

                if "generate-index" in sys.argv:
                    ig = IndexGenerator(dictionary, filename_without_extension)
                    ig.generate()

        _print_size_difference(input_file_path, output_dict_path)


def _filepaths(current_working_directory, current_dict_filename):
    output_dict_path = os.path.join(current_working_directory + "/output", current_dict_filename)
    input_file_path = os.path.join(current_working_directory + "/input", current_dict_filename)
    return output_dict_path, input_file_path


def _declutter(columns, current_working_directory, dict_file_content):
    if "translate" in sys.argv:
        dict_file_content = _translate_keywords_to_english(dict_file_content, current_working_directory)
    if "declutter-universal" in sys.argv:
        dict_file_content = declutter_universally_redundant_parts(dict_file_content)
    if "declutter-language-specific" in sys.argv:
        dict_file_content = declutter_with_regex_instructions(dict_file_content, columns)
    return dict_file_content


def _save_changes(dict_file, dict_file_content):
    # set position to 0
    dict_file.seek(0)
    # remove everything in new copy
    dict_file.truncate()
    dict_file.write(dict_file_content)


def _print_size_difference(file_now, file_before):
    size_now = os.stat(file_now).st_size
    size_before = os.stat(file_before).st_size
    print("Size reduced by: " + str(round(100 - (size_before / size_now) * 100, 2)) + "%")


def _translate_keywords_to_english(content, current_working_directory):

    temp = content

    with open(current_working_directory + "/keywords.csv", mode="r") as keywords_file:
        csv_content = csv.reader(keywords_file)

        for line in csv_content:
            columns = line[0].split(';')

            column_range = range(1, len(columns))

            for column_index in column_range:

                # TODO: Only go to column for this language
                print(columns[column_index])
                temp = re.sub(columns[column_index], columns[0], temp)

    return temp

# TODO: Install eslint
if __name__ == "__main__":
    main()
