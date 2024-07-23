import os
import json
import unittest
from unittest.mock import patch

import utilities
from library_management_system import (generate_id, add_book, delete_book,
                                       search_book, list_books, 
                                       change_book_status, start_menu, main)
from utilities import (load_data, save_data, check_data, representation_book)


class Tests(unittest.TestCase):
    """Тесты."""

    TEST_DATA_FILE = "test_data.json"

    def setUp(self) -> None:
        """Инициализация. Создаёт файл с тестовыми данными."""

        self.test_data = {
            '1': {
                'title': 'Тестовая книга',
                'author': 'Тест',
                'year': '2020',
                'status': 'в наличии'
                },
            '2': {
                'title': 'Стихи',
                'author': 'Пушкин',
                'year': '1825',
                'status': 'в наличии'
                },
            '3': {
                'title': 'Поэма',
                'author': 'Есенин',
                'year': '1920',
                'status': 'выдана'
            },
            '4': {
                'title': 'Тестовая книга',
                'author': 'Тест',
                'year': '2020',
                'status': 'выдана'
            },
        }
        with open(self.TEST_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.test_data, file, ensure_ascii=False, indent=4)

        # Переопределение DATA_FILE в модулях
        utilities.DATA_FILE = self.TEST_DATA_FILE

    def tearDown(self) -> None:
        """Очистка. Удаляет файл с тестовыми данными."""

        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def test_load_data(self) -> None:
        """Тест функции load_data."""

        self.assertEqual(load_data(), self.test_data)

    def test_save_data(self) -> None:
        """Тест функции save_data."""

        self.assertTrue(save_data(self.test_data))

    def test_check_data(self) -> None:
        """Тест функции check_data."""

        self.assertEqual(check_data(), self.test_data)

    def test_generate_id(self) -> None:
        """Тест функции generate_id."""

        self.assertEqual(generate_id(load_data()), '5')

    def test_representation_book(self) -> None:
        """Тест функции representation_book."""

        book_id = '1'
        book = self.test_data['1']
        result = representation_book(book_id, book)
        expected = (
            f'''
            ID: {book_id},
            Название: {book['title']},
            Автор: {book['author']},
            Год издания: {book['year']},
            Статус: {book['status']}
            '''
        )

        self.assertEqual(
            result.replace(' ', '').replace('\n', ''),
            expected.replace(' ', '').replace('\n', '')
            )

    def test_add_book(self) -> None:
        """Тест функции add_book."""

        self.assertEqual(
            add_book('Рассказ', 'Чехов', '1890'),
            'Книга успешно добавлена.'
        )

    def test_delete_book(self) -> None:
        """Тест функции delete_book."""

        delete_book('1')
        data = load_data()
        self.assertNotIn('1', data)

    def test_search_book(self):
        """Тест функции search_book."""

        result, count_book = search_book('Тест', '2')
        self.assertIn("2020", result) and self.assertEqual(2, count_book)

    @patch("builtins.print")
    def test_list_books(self, mock_print) -> None:
        """Тест функции list_books."""

        self.assertIn("Список книг успешно выведен.", list_books())

    def test_change_book_status(self) -> None:
        change_book_status("1", "выдана")
        data = load_data()
        self.assertEqual(data["1"]["status"], "выдана")

    def test_start_menu(self) -> None:
        """Тест функции start_menu."""

        self.assertIn(
            "Добро пожаловать в библиотеку!", start_menu(True)
            ) and self.assertIn(
                'Выберите действие:', start_menu(False)
                )

    @patch("builtins.print")  # Подавление вывода print
    @patch("builtins.input", side_effect=["6"])
    def test_first_start_false(self, mock_input, mock_print):
        """
        Проверка, что first_start устанавливается в False.
        После первой итерации.
        """

        first_start = main()
        self.assertFalse(first_start)


if __name__ == '__main__':
    unittest.main()
