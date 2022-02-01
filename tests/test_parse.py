import pytest

from src.logic.parse import *


@pytest.mark.parametrize("test_input, expected", [
    ("{{mf}}\n", Gender.masculine_and_feminine),
    ("\n{{m}}", Gender.masculine),
    ("{{f}}", Gender.feminine),
    ("{{n}}", Gender.neuter),
    ("\n=== {{part-of-speech|noun|german}}, {{n}} ===\n\n", Gender.neuter),
    ("=== {{part-of-speech|noun|latin}}, {{m}} ===", Gender.masculine),
    ("=== {{part-of-speech|verb|english}} ===", Gender.not_applicable)
])
def test_parse_gender(test_input, expected):
    assert parse_gender(test_input) == expected


@pytest.mark.parametrize("test_input", [dict(), 100, list(), -10])
def test_parse_gender_type(test_input):
    with pytest.raises(TypeError):
        parse_gender(test_input)


@pytest.mark.parametrize("test_input, expected", [
    ("=== {{part-of-speech|noun|german}}, {{n}} ===", "german"),
    ("=== {{part-of-speech|verb|latin}}, {{m}} ===", "latin"),
    ("=== {{part-of-speech|noun|german}}, {{m}}, {{part-of-speech|Toponym|german}} ===", "german")
])
def test_parse_language(test_input, expected):
    assert parse_language(test_input) == expected


@pytest.mark.parametrize("test_input", [dict(), 100, list()])
def test_parse_language_type(test_input):
    with pytest.raises(TypeError):
        parse_language(test_input)


@pytest.mark.parametrize("test_input, expected", [
    ("\n{{root-form-reference|serius|lang=la}}", ["serius"]),
    ("{{root-form-reference|Augusta|lang=pl}}\n{{root-form-reference|oni|lang=sk}}\n", ["Augusta", "oni"])
])
def test_parse_root_word(test_input, expected):
    assert parse_root_word(test_input) == expected


@pytest.mark.parametrize("test_input", [dict(), list(), 100])
def test_parse_root_word_type(test_input):
    with pytest.raises(TypeError):
        parse_root_word(test_input)


@pytest.mark.parametrize("test_input, name, expected", [
    ("{{female-word-form}}\n:[1, 2] ''Besitzer ist grammatisch weiblich:'' [[ihr]]\n\n", "female-word-form", ["ihr"]),
    ("{{male-word-form}}\n:[1] [[Vater]]\n\n", "male-word-form", ["Vater"]),
    ("{{secondary-forms}}\n:[[Haues]]\n\n", "secondary-forms", ["Haues"]),
    ("{{outdated-forms}}\n:[[Schloß]]\n\n", "outdated-forms", ["Schloß"]),
    ("{{grammatical-features}}\n:[[Genitiv]] Singular nach [[pater]], [[mater]]\n\n", "grammatical-features",
     ["Genitiv", "pater", "mater"])
])
def test_parse_generic_word_forms(test_input, name, expected):
    assert parse_generic_word_forms(test_input, name) == expected


@pytest.mark.parametrize("test_input, name", [
    ("ello", dict()),
    (list(), "bibi"),
    (100, 100)
])
def test_parse_generic_word_forms_type(test_input, name):
    with pytest.raises(TypeError):
        parse_generic_word_forms(test_input, name)


def test_parse_section():
    test_input = """
    === {{part-of-speech|noun|german}}, {{n}} ===

{{Deutsch noun overview
|Genus=n
|Nominativ Singular=Hallo
|Nominativ Plural=Hallos
|Genitiv Singular=Hallos
|Genitiv Plural=Hallos
|Dativ Singular=Hallo
|Dativ Plural=Hallos
|Akkusativ Singular=Hallo
|Akkusativ Plural=Hallos
}}

{{definitions}}
:[1] lautes Rufen; fröhliches, lautes Durcheinander

{{Ähnlichkeiten 1|[[Hall]], [[halle]], [[Halle]], [[Halo]], [[Holle]]|Anagramme=[[holla]]}}
    
{{grammatical-features}}
*Nominativ Singular Maskulinum der starken Deklination des Positivs des Adjektivs '''[[wegredend]]'''
    
{{root-form-reference|wegredend}}

{{female-word-form}}
:[1] [[Emmentalerin]]

{{secondary-forms}}
:[[unliniert]]

{{outdated-forms}}
:[[Schrotschuß]]

{{male-word-form}}
:[1] [[Schrotthändler]]
    """

    output = parse_section(test_input)
    expected = Word("noun", "german", Gender.neuter,
                    [
                        Definition("1. lautes Rufen; fröhliches, lautes Durcheinander")
                    ], {
                        "Nominativ Singular": "Hallo", "Nominativ Plural": "Hallos",
                        "Genitiv Singular": "Hallos",
                        "Genitiv Plural": "Hallos", "Dativ Singular": "Hallo", "Dativ Plural": "Hallos",
                        "Akkusativ Singular": "Hallo",
                        "Akkusativ Plural": "Hallos"
                    }, ["wegredend"], ["Emmentalerin"], ["Schrotthändler"],
                    ["unliniert"], ["Schrotschuß"], ["wegredend"])

    assert output.root_words == expected.root_words
    assert output.outdated_forms == expected.outdated_forms
    assert output.language == expected.language
    assert output.male_word_forms == expected.male_word_forms
    assert output.female_word_forms == expected.female_word_forms
    assert output.secondary_forms == expected.secondary_forms
    assert output.gender == expected.gender
    assert output.grammar_forms == expected.grammar_forms
    assert output.part_of_speech == expected.part_of_speech
    assert output.derivatives == expected.derivatives

    for def1, def2 in zip(output.definitions, expected.definitions):
        assert def1.description == def2.description


@pytest.mark.parametrize("test_input", [dict(), list(), 100])
def test_parse_section_type(test_input):
    with pytest.raises(TypeError):
        parse_section(test_input)


def test_parse_definitions():
    test_input = """
=== {{part-of-speech|noun|german}}, {{n}} ===

{{Deutsch noun overview
|Genus=n
|Nominativ Singular=Hallo
|Nominativ Plural=Hallos
|Genitiv Singular=Hallos
|Genitiv Plural=Hallos
|Dativ Singular=Hallo
|Dativ Plural=Hallos
|Akkusativ Singular=Hallo
|Akkusativ Plural=Hallos
}}

{{definitions}}
:[1] lautes Rufen; fröhliches, lautes Durcheinander
:[2] lautes Rufen; fröhliches, lautes Durcheinander
:[3] lautes Rufen; fröhliches, lautes Durcheinander

{{Ähnlichkeiten 1|[[Hall]], [[halle]], [[Halle]], [[Halo]], [[Holle]]|Anagramme=[[holla]]}}
    """

    expected_definitions = [
        Definition("1. lautes Rufen; fröhliches, lautes Durcheinander"),
        Definition("2. lautes Rufen; fröhliches, lautes Durcheinander"),
        Definition("3. lautes Rufen; fröhliches, lautes Durcheinander")
    ]

    output_definitions = parse_definitions(test_input)

    for def1, def2 in zip(output_definitions, expected_definitions):
        assert def1.description == def2.description


@pytest.mark.parametrize("test_input", [dict(), list(), 100])
def test_parse_definitions_type(test_input):
    with pytest.raises(TypeError):
        parse_definitions(test_input)


def test_parse_derivation_table_noun():
    test_input = """
=== {{part-of-speech|noun|german}}, {{n}} ===

{{Deutsch noun overview
|Genus=n
|Nominativ Singular=Hallo
|Nominativ Plural=Hallos
|Genitiv Singular=Hallos
|Genitiv Plural=Hallos
|Dativ Singular=Hallo
|Dativ Plural=Hallos
|Akkusativ Singular=Hallo
|Akkusativ Plural=Hallos
}}

{{definitions}}
:[1] lautes Rufen; fröhliches, lautes Durcheinander

{{Ähnlichkeiten 1|[[Hall]], [[halle]], [[Halle]], [[Halo]], [[Holle]]|Anagramme=[[holla]]}}
    """

    derivation_table = {
        "Nominativ Singular": "Hallo",
        "Nominativ Plural": "Hallos",
        "Genitiv Singular": "Hallos",
        "Genitiv Plural": "Hallos",
        "Dativ Singular": "Hallo",
        "Dativ Plural": "Hallos",
        "Akkusativ Singular": "Hallo",
        "Akkusativ Plural": "Hallos"
    }

    assert parse_derivation_table(test_input) == derivation_table


def test_parse_derivation_table_verb():
    test_input = """
=== {{part-of-speech|verb|german}}, {{n}} ===

{{Deutsch verb overview
|Präsens_ich=müffle
|Präsens_ich*=müffele
|Präsens_du=müffelst
|Präsens_er, sie, es=müffelt
|Präteritum_ich=müffelte
|Partizip II=gemüffelt
|Konjunktiv II_ich=müffelte
|Imperativ Singular=müffle
|Imperativ Singular*=müffele
|Imperativ Plural=müffelt
|Hilfsverb=haben
}}

{{definitions}}
:[1] lautes Rufen; fröhliches, lautes Durcheinander

{{Ähnlichkeiten 1|[[Hall]], [[halle]], [[Halle]], [[Halo]], [[Holle]]|Anagramme=[[holla]]}}
    """

    derivation_table = {
         'Imperativ Plural': 'müffelt',
         'Imperativ Singular': 'müffle',
         'Imperativ Singular*': 'müffele',
         'Konjunktiv II_ich': 'müffelte',
         'Partizip II': 'gemüffelt',
         'Präsens_du': 'müffelst',
         'Präsens_er, sie, es': 'müffelt',
         'Präsens_ich': 'müffle',
         'Präsens_ich*': 'müffele',
         'Präteritum_ich': 'müffelte'
    }

    assert parse_derivation_table(test_input) == derivation_table


def test_parse_derivation_table_adjective():
    test_input = """
=== {{part-of-speech|adjective|german}}, {{n}} ===

{{Polnisch adjective overview
|Positiv=absyntowy
|Komparativ=—
|Superlativ=—
}}

{{definitions}}
:[1] lautes Rufen; fröhliches, lautes Durcheinander

{{Ähnlichkeiten 1|[[Hall]], [[halle]], [[Halle]], [[Halo]], [[Holle]]|Anagramme=[[holla]]}}
    """

    derivation_table = {
        'Positiv': 'absyntowy'
    }

    assert parse_derivation_table(test_input) == derivation_table


def test_parse_derivation_table_adverb():
    test_input = """
=== {{part-of-speech|adjective|german}}, {{n}} ===

{{Tschechisch adverb overview
|Positiv=často
|Komparativ=častěji
|Superlativ=nejčastěji
}}

{{definitions}}
:[1] lautes Rufen; fröhliches, lautes Durcheinander

{{Ähnlichkeiten 1|[[Hall]], [[halle]], [[Halle]], [[Halo]], [[Holle]]|Anagramme=[[holla]]}}
    """

    derivation_table = {
        'Komparativ': 'častěji',
        'Positiv': 'často',
        'Superlativ': 'nejčastěji'
    }

    assert parse_derivation_table(test_input) == derivation_table


@pytest.mark.parametrize("test_input", [dict(), list(), 100])
def test_parse_derivation_table_type(test_input):
    with pytest.raises(TypeError):
        parse_derivation_table(test_input)
