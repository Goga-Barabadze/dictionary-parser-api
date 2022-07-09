from dataclasses import dataclass

from src.model.Gender import Gender
from src.model.Translation import Translation


@dataclass
class Word:
    """
    A class representing a word in any language
    """
    id: int
    word: str
    language_code: str
    part_of_speech: str
    definitions: [str]
    pronunciations: [str]
    example_usages: [str]
    cases: [str]
    hyphenations: [str]
    plurals: [str]
    singulars: [str]
    etymologies: [str]
    lemma: str
    stem: str
    synonymes: [str]
    antinomes: [str]
    female_forms: [str]
    male_forms: [str]
    outdated_forms: [str]
    abbreviations: [str]
    genders: [Gender]
    translations: [Translation]
    root_words: [str]
