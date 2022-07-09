def run(funcs, seed=""):
    for function in funcs:
        seed = function(seed)
    return seed
