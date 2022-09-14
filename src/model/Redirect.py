from dataclasses import dataclass


@dataclass
class Redirect:
    from_word: str
    to_word: str