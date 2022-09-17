"""
This file handles the different ways to interact with the routines
"""

FALLBACK_LANGUAGE_CODE = "en"


def run(funcs, seed=""):
    for function in funcs:
        seed = function(seed)
    return seed


def run_vars(path, language_code, passed_vars):
    """ Calls a function and adds the passed vars to the predefined ones in the routine """
    use_langauge_code = language_code
    if language_code not in path:
        use_langauge_code = FALLBACK_LANGUAGE_CODE

    predefined_vars = path[use_langauge_code]["vars"]
    return path[use_langauge_code]["func"](*predefined_vars, *passed_vars)
