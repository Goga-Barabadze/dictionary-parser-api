import random

def smart_access_dict(_indices, _dictionary, offset=0):
    if _indices[offset] not in _dictionary and len(_indices) != 1:
        _dictionary[_indices[offset]] = dict()

    if len(_indices) - 1 == offset:
        return

    if len(_indices) - 2 == offset:
        if _indices[offset + 1] in _dictionary[_indices[offset]]:
            return
        arr = _indices[offset + 1] if type(_indices[offset + 1]) == list else [_indices[offset + 1]]
        if type(_dictionary[_indices[offset]]) == dict:
            _dictionary[_indices[offset]] = arr
        else:
            _dictionary[_indices[offset]] += arr
    else:
        smart_access_dict(_indices, _dictionary[_indices[offset]], offset + 1)

dictionary = {"entries": ["hallo"]}

smart_access_dict(["entries", "hallo"], dictionary)



print(dictionary)