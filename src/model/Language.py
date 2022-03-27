import csv
from pathlib import Path


class Language:
    @staticmethod
    def does_language_code_exist(language_code):
        cwd = str(Path(__file__).resolve().parent.parent.parent)
        with open(cwd + "/language_codes.csv", mode="r") as file:
            csv_content = csv.reader(file)

            for line in csv_content:
                columns = line[0].split(';')
                if columns[0] == language_code:
                    return True

            return False
