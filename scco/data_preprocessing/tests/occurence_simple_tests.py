import unittest
from tools.dict_occurrence import DictOccurrenceManager


class TestExactOccurrenceSimple(unittest.TestCase):
    def setUp(self):
        dictionary = set(['Вакансия'])
        self.occurrence_manager = DictOccurrenceManager(dictionary)

    def check_message(self, message, answer):
        self.assertEqual(self.occurrence_manager.check_exact_occurrence(message), answer)

    def test_small(self):
        self.check_message('Вакансия', True)

    def test_medium(self):
        self.check_message('Моя Вакансия и еще какие-то слова и ! знаки , припи.нания', True)

    def test_big(self):
        word_list = ['слово'] * 42
        self.check_message(' '.join(word_list), False)


class TestOccurrenceWithErrorsSimple(unittest.TestCase):
    def setUp(self):
        dictionary = set(['Вакансия'])
        self.occurrence_manager = DictOccurrenceManager(dictionary)
        self.errors_num = 2

    def check_message(self, message, answer):
        self.assertEqual(self.occurrence_manager.check_occurrence_with_errors(message, self.errors_num), answer)

    # small tests
    def test_equal_1(self):
        self.check_message('Вакансия', True)

    def test_splitted(self):
        self.check_message('Ва   кан  сия', False)

    def test_edit_1(self):
        self.check_message('Вакансии', True)

    def test_edit_2(self):
        self.check_message('Воканsиа', False)  # 3 edits

    def test_insert_1(self):
        self.check_message('Вакансиии', True)

    def test_insert_2(self):
        self.check_message('Вакаансииии', False)  # 3 insertions

    def test_remove_1(self):
        self.check_message('Вкансии', True)

    def test_remove_2(self):
        self.check_message('Вканс', False)
