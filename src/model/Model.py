class Page:

    def __init__(self, title, words):
        self.title = title
        self.words = words


class Word:
    root_words = None
    derivatives = {}

    def __init__(self, part_of_speech, language, gender, definitions, derivatives, root_words, female_word_forms,
                 male_word_forms, secondary_forms, outdated_forms, grammar_forms, translations):
        self.part_of_speech = part_of_speech
        self.language = language
        self.gender = gender
        self.definitions = definitions
        self.derivatives = derivatives
        self.root_words = root_words
        self.female_word_forms = female_word_forms
        self.male_word_forms = male_word_forms
        self.secondary_forms = secondary_forms
        self.outdated_forms = outdated_forms
        self.grammar_forms = grammar_forms
        self.translations = translations

    def all_word_forms(self):

        word_forms = []

        word_forms += list(self.derivatives.values())
        word_forms += self.female_word_forms if self.female_word_forms is not None else list()
        word_forms += self.male_word_forms if self.male_word_forms is not None else list()
        word_forms += self.secondary_forms if self.secondary_forms is not None else list()
        word_forms += self.outdated_forms if self.outdated_forms is not None else list()
        word_forms += self.grammar_forms if self.grammar_forms is not None else list()
        word_forms += [tl[1] for tl in self.translations] if self.translations is not None else list()

        return list(dict.fromkeys(word_forms))

    def word_forms_which_point_back(self):
        word_forms = []

        word_forms += list(self.derivatives.values())
        word_forms += self.secondary_forms if self.secondary_forms is not None else list()
        word_forms += self.outdated_forms if self.outdated_forms is not None else list()

        # Remove duplicates
        return list(dict.fromkeys(word_forms))

    def word_forms_which_point_away(self):
        word_forms = []

        word_forms += self.grammar_forms if self.grammar_forms is not None else list()
        word_forms += self.root_words if self.root_words is not None else list()
        word_forms += [tl[1] for tl in self.translations] if self.translations is not None else list()

        # Remove duplicates
        return list(dict.fromkeys(word_forms))

    def word_forms_related(self):
        word_forms = []

        word_forms += self.female_word_forms if self.female_word_forms is not None else list()
        word_forms += self.male_word_forms if self.male_word_forms is not None else list()

        # Remove duplicates
        return list(dict.fromkeys(word_forms))


class Definition:

    def __init__(self, description):
        self.description = description
