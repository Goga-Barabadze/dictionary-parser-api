"""
A regex wrapper which internally handles caching
"""

import re
from functools import lru_cache


class Regex:

    @staticmethod
    @lru_cache
    def _compile(pattern):
        return re.compile(pattern)

    @staticmethod
    def match(pattern, string):
        return Regex._compile(pattern).match(string)

    @staticmethod
    def findall(pattern, string):
        return Regex._compile(pattern).findall(string)

    @staticmethod
    def search(pattern, string):
        return Regex._compile(pattern).search(string)
