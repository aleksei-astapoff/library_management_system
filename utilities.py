import os
import json

from constants import DATA_FILE


def load_data() -> dict:
    """Загружает данные из JSON-файла. Если файл не существует, создает его."""

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data) -> bool:
    """Сохраняет данные в JSON-файл."""

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True

    except Exception as error:
        raise ValueError(f'Ошибка при сохранении данных: {error}')


def check_data() -> dict:
    """Проверяет данные на наличие книг."""

    data = load_data()
    if not data:
        raise ValueError('Список книг пуст.')
    return data


def representation_book(book_id, book) -> str:
    """Возвращает "f" строку с информацией о книге."""

    return (
        f'''
        ID: {book_id},
        Название: {book['title']},
        Автор: {book['author']},
        Год издания: {book['year']},
        Статус: {book['status']}
        '''
        )
