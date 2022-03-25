from src.logic.IndexGenerator import IndexGenerator

dictionary = {
    "word1": {
        "page": {
            "title": "qwkejbqjdb"
        }
    },
    "ABC": {
        "page": {
            "title": "asdad"
        }
    },
    "askjd": {
        "page": {
            "title": "adlasld"
        }
    },
    "askd": {
        "page": {
            "title": "ölkökö"
        }
    },
    "qweu": {
        "page": {
            "title": "qiuwehq"
        }
    },
    "zzz": {
        "page": {
            "title": "mylkxlyc"
        }
    },

}

ig = IndexGenerator(dictionary, "de")
ig.generate()
