import json

from pathlib import Path
from typing.io import IO


class IndexGenerator:
    words = []
    index_length = 3

    def __init__(self, words, language_code, index_length=3):
        self.words = words
        self.language_code = language_code
        self.index_length = index_length

    def generate(self):

        sorted_words = sorted(self.words)
        old_index = ""

        current_working_directory = str(Path(__file__).resolve().parent.parent)

        path = current_working_directory + "/output/" + self.language_code + "/"
        Path(path).mkdir(exist_ok=True)

        index_file = IO()

        for word in sorted_words:

            max_length = len(word) if len(word) < self.index_length else self.index_length
            index = word[0:max_length]

            if old_index != index:
                index_file.close()
                index_file = open(path + index + ".txt", "a+")

            dictionary = {
                "word":"Word",
                "definition":"1. Definition"
            }

            index_file.write(json.dumps(dictionary) + "\n")

        index_file.close()