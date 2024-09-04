from Levenshtein import distance
import re


# default: all possible punctuation
def split_by_regex(text, regex):
    normalize_text = re.sub(regex, '', text)
    return normalize_text.split(' ')


class DictOccurrenceManager:
    def __init__(self, dictionary: set):
        self.dictionary = dictionary
        self.punctuation_regex = '[^\w\s]'

    # Time ~ len(message)
    def check_exact_occurrence(self, message):
        splitted_message = split_by_regex(message, self.punctuation_regex)
        for word in splitted_message:
            if len(word) == 0:  # split can return empty word between spaces
                continue
            if word in self.dictionary:
                return True
        return False

    # error == k <=> Levenshtein dist == k
    # Time ~ O(D*n^2), where n is average len(word), D = len(dict)
    def check_occurrence_with_errors(self, message, errors_num):
        # <= errors_num errors
        splitted_message = split_by_regex(message, self.punctuation_regex)
        for word in splitted_message:
            if len(word) < errors_num:
                continue
            for dict_word in self.dictionary:
                if distance(dict_word, word) <= errors_num:
                    return True
        return False

    def check_occurence_adaptive(self, message):
        splitted_message = split_by_regex(message, self.punctuation_regex)
        for word in splitted_message:
            if len(word) == 0:  # split can return empty word between spaces
                continue
            elif len(word) < 4:
                if word in self.dictionary:
                    return True
            elif len(word) < 7:
                for dict_word in self.dictionary:
                    if distance(dict_word, word) <= 1:
                        return True
            else:
                for dict_word in self.dictionary:
                    if distance(dict_word, word) <= 2:
                        return True
        return False

    # Возможные улучшения:
    # 1) Текст обрабатывать по частям, чтобы очень большие тексты не разбивать
    #    полностью, мб поможет, если встречается ближе к началу сообщения
    # 2) Убрать двойные пробелы мб стоит (или нет?)
    # 3) Обобщить общую часть алгоритмов (или нет?)
    # 4) Можно на плюсах суфф автомат написать и быстро искать вхождения
    #    (без ошибки точно, с ошибкой уже не строго по ливенштейну, но
    #    приставку и суффикс отбросить можно)
