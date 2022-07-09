from dataclasses import dataclass


@dataclass
class Translation:
    language_code: str
    translation: str
