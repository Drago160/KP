import numpy as np


class Matcher:
    def __init__(self, transform=None):
        """
            transform: function from string to string
            mb you need some preprocessing

            If you use it, remember, that
            other methods will give you mathing between
            transormed text and pattern
        """
        self.buff = []
        if transform is None:
            self.transform = lambda s: s
        else:
            self.transform = transform
        self._delim = "$$$$$"

    def get_matching_positions(self, pattern: str, text: str) -> np.array:
        """
            return: position i, where text[i:] start with pattern
        """
        text, pattern = self.transform(text), self.transform(pattern)
        self._prefix_func(pattern + self._delim + text)  # pref_func(PT)
        text_pref_slice = np.array(
            self.buff[len(pattern) + len(self._delim):len(pattern) + len(text) + len(self._delim)])
        return np.where(text_pref_slice >= len(pattern))[0] - len(pattern) + 1

    def count_matches(self, pattern, text: str) -> int:
        """
            count all positions, where pattern in text
        """
        return len(self.get_matching_positions(pattern, text))

    def _prefix_func(self, string):  # only prefix with size of string
        self.buff = [0]
        for i in range(1, len(string)):
            k = self.buff[i-1]
            while k > 0 and string[i] != string[k]:
                k = self.buff[k - 1]
            if string[i] == string[k]:
                k += 1
            self.buff.append(k)
