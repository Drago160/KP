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
        self.buff = [0]
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
        text_pref_slice = np.array(self.buff[len(pattern):len(pattern) + len(text) + len(self._delim)])
        return np.where(text_pref_slice >= len(pattern))[0] - len(pattern) - len(self._delim) + 1

    def count_matches(self, pattern, text: str) -> int:
        """
            count all positions, where pattern in text
        """
        return len(self.get_matching_positions(pattern, text))

    def _prefix_func(self, string):  # only prefix with size of string
        self._reserve(len(string))
        for i in range(1, len(string)):
            prev = self.buff[i - 1]
            while prev > 0 and string[prev] != string[i]:
                prev = self.buff[prev - 1]
            if string[prev] == string[i]:
                prev += 1
            self.buff[i] = prev

    def _reserve(self, size):
        while len(self.buff) < size:
            self.buff.append(0)


# Вот примеры:
# m = Matcher(lambda s: s.lower())
# print(m.count_matches('ищу', '#ищу того кто соберет или продаст клиентскую базу салонов красотыкосметологических центров москвы пишите пожалуйста сразу с ценой',))
# print(m.get_matching_positions("Я наверное хотел бы, ну или не хотел бы", "Хотел")) # [11, 31]
# print(m.get_matching_positions("Я наверное не хотел бы, ну или хотел бы", "Хотел")) # [14, 31]
# print(m.get_matching_positions("Я наверное бы, ну или не бы", "Хотел")) # []
# print(m.get_matching_positions("Я наверное бы хоте, ну или не хтел", "Хотел")) # []
# print(m.get_matching_positions("Я наверное бы хоте, ну или не хтел", "Хотел")) # []

# Я запускал на стресстестах, вроде норм пашет, если найдешь багу - пиши, зафикшу
