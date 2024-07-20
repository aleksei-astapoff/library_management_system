import os
import json


DATA_FILE = 'data.json'


def load_data():
    """Загружает данные из JSON-файла. Если файл не существует, создает его."""

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            json.dump({}, file)
    with open(DATA_FILE, 'r') as file:
        return json.load(file)


def save_data(data):
    """Сохраняет данные в JSON-файл."""

    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def generate_id(data):
    """Генерирует уникальный идентификатор book_id для новой книги."""

    if not data:
        return 1
    return max(data.keys()) + 1


def add_book(title, author, year):
    """Добавляет книгу в список."""

    data = load_data()
    book_id = generate_id(data)
    data[book_id] = {
        'title': title,
        'author': author,
        'year': year,
        'status': 'В наличии'
    }
    save_data(data)
    print('Книга успешно добавлена.')


def delete_book(book_id):
    """Удаляет книгу из списка."""

    data = load_data()
    if book_id in data:
        del_book = data.pop(book_id)
        save_data(data)
        print(f'Книга{del_book['title']}успешно удалена.')
    else:
        print('Книга не найдена.')
