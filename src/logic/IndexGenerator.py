import re
import jsonpickle

from pathlib import Path
from typing.io import IO


class IndexGenerator:
    def __init__(self, dictionary, language_code, index_length=3):
        self.dictionary = dictionary
        self.language_code = language_code
        self.index_length = index_length

    def generate(self):

        old_index = ""

        current_working_directory = str(Path(__file__).resolve().parent.parent.parent)

        path = current_working_directory + "/output/" + self.language_code + "/"
        Path(path).mkdir(exist_ok=True)

        index_file = IO()

        while len(self.dictionary) != 0:
            buffer = []
            for _ in range(0, 10000):
                if len(self.dictionary) > 0:
                    buffer.append(self.dictionary.popitem())

            buffer = sorted(buffer)

            for key, value in buffer:

                page = value["page"]
                title = key

                max_length = len(title) if len(title) < self.index_length else self.index_length
                index = title[0:max_length]

                if old_index != index:
                    index_file.close()
                    index_file = open(path + index + ".txt", "a+")

                index_file.write(jsonpickle.encode(value + "\n"))

        index_file.close()
