import os
import json

DATA_FILE = 'data.json'


def load_data() -> dict:
    """Загружает данные из JSON-файла. Если файл не существует, создает его."""

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            json.dump({}, file)
    with open(DATA_FILE, 'r') as file:
        return json.load(file)


def save_data(data) -> bool:
    """Сохраняет данные в JSON-файл."""

    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        return True

    except Exception as error:
        raise ValueError(f'Ошибка при сохранении данных: {error}')


def check_data() -> dict:
    """Проверяет данные на наличие ошибок."""
    data = load_data()
    if not data:
        raise ValueError('Список книг пуст.')
    return data


def generate_id(data) -> str:
    """Генерирует уникальный идентификатор book_id для новой книги."""

    if not data or not data.keys():
        book_id = 1
    else:
        book_id = max(int(id) for id in data.keys()) + 1

    return str(book_id)


def add_book(title, author, year) -> str:
    """Добавляет книгу в список."""

    data = load_data()
    book_id = generate_id(data)
    data[book_id] = {
        'title': title.strip(),
        'author': author.strip(),
        'year': year,
        'status': 'в наличии'
    }

    if save_data(data):
        return 'Книга успешно добавлена.'
    else:
        raise ValueError('Ошибка при добавлении книги.')


def delete_book(book_id) -> str:
    """Удаляет книгу из списка."""

    data = check_data()
    if book_id in data:
        del_book = data.pop(book_id)
        if del_book and save_data(data):
            return (
                f'''
                ID: {book_id},
                Название: {del_book["title"]},
                Автор: {del_book["author"]},
                Год издания: {del_book["year"]},
                Статус: {del_book["status"]}
                '''
            )
        else:
            raise ValueError(
                f'Ошибка при удалении книги с ID: {book_id}.'
                )
    else:
        raise ValueError(f'Книга с ID: {book_id} не найдена.')


def search_book(query, field) -> list:
    """Поиск книг по заданному критерию."""

    if field not in ('title', 'author', 'year'):
        raise ValueError('Неверное поле для поиска.')
    data = check_data()
    books = [
        book for book in data.values()
        if book[field].casefold() == query.strip().casefold()
    ]
    if not books:
        raise ValueError('С данными критериями ничего не найдено.')
    return books


def list_books() -> str:
    """Выводит список книг."""

    data = check_data()
    for book_id, book in data.items():
        print(
            f'''
            ID: {book_id}, Название: {book["title"]}, Автор: {book["author"]},
            Год издания: {book["year"]}, Статус: {book["status"]}
            '''
        )
    return 'Список книг успешно выведен.'


def change_book_status(book_id, status) -> str:
    """Изменяет статус книги."""

    status = status.strip().casefold()
    data = check_data()
    if status not in ('в наличии', 'выдана'):
        raise ValueError('Неверное значение статуса.')
    if book_id not in data:
        raise ValueError(f'Книги с ID: {book_id} нет.')
    data[book_id]['status'] = status
    if save_data(data):
        return f'Статус книги с ID: {book_id} успешно изменен на {status}.'
    else:
        raise ValueError(
            f'Ошибка при изменении статуса книги с ID: {book_id}.'
            )
