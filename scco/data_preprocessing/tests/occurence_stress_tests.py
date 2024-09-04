from tools.dict_occurrence import DictOccurrenceManager
import unittest
import time


class TestStressOccurrence(unittest.TestCase):
    def setUp(self):
        self.dict_list = ['Вакансия', 'Слово', 'Яблоко']
        self.dictionary = set(self.dict_list)
        self.occurrence_manager = DictOccurrenceManager(self.dictionary)
        self.errors_num = 2

    def check_message(self, message, answer):
        self.assertEqual(
            self.occurrence_manager
            .check_occurrence_with_errors(message, self.errors_num),
            answer)

    def basic_try(self, size, answer, message, timelimit=None):
        begin_time = time.time()
        self.check_message(message, answer)
        whole_time = time.time() - begin_time
        print(f'Время работы теста на {size} слов со словарем размера {len(self.dict_list)}: {round(whole_time, 5)} (Answer = {answer})')
        if timelimit is not None:
            self.assertEqual(whole_time <= timelimit, True)

    def try_no_occurrence(self, size):
        messages = ['Груша']*size
        concat = ' '.join(messages)
        self.basic_try(size, False, concat)

    def test_medium_no_occurrence(self):
        self.try_no_occurrence(1000)

    def test_big_no_occurrence(self):
        self.try_no_occurrence(1000000)

    def try_with_occurrence(self, size, occurrence_idx=0):
        messages = ['Груша']*size
        messages[min(1000, size - 1)] = self.dict_list[occurrence_idx]
        self.basic_try(size, True, ' '.join(messages))

    def test_short_with_occurrence(self):
        self.try_with_occurrence(100, 2)

    def test_medium_with_occurrence(self):
        self.try_with_occurrence(1000, 0)

    def test_big_with_occurrence(self):
        self.try_with_occurrence(20000000, 1)
