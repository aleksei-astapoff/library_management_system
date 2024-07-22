from constants import DICT_SEARCH_FIELD, DICT_STATUS_BOOK
from utilities import load_data, check_data, save_data, representation_book


def start_menu(first_start) -> tuple[str, bool]:
    """Выводит приветственное сообщение."""

    welocme_text = '''
    Добро пожаловать в библиотеку!

    Возможности библиотеки:
    '''

    text = f'''
        {welocme_text if first_start else 'Выберите действие:'}
        1. Добавить книгу
        2. Удалить книгу
        3. Найти книгу
        4. Вывести список книг
        5. Изменить статус книги
        6. Выход
        '''

    return text


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
        'title': title,
        'author': author,
        'year': year,
        'status': 'в наличии',
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
            return representation_book(book_id, del_book)
        else:
            raise ValueError(f'Ошибка при удалении книги с ID: {book_id}.')
    else:
        raise ValueError(f'Книга с ID: {book_id} не найдена.')


def search_book(query, field) -> list:
    """Поиск книг по заданному критерию."""

    if field not in DICT_SEARCH_FIELD.keys():
        raise ValueError(f'Неверное поле для поиска: {field}.')
    data = check_data()
    books = {}
    for book_id, book in data.items():
        if book[DICT_SEARCH_FIELD[field]].casefold() == query.casefold():
            books[book_id] = book

    if not books:
        raise ValueError('С данными критериями ничего не найдено.')
    search_book: list = '\n'.join(
        representation_book(book_id, book) for book_id, book in books.items()
        )
    print(f'\n Найдено книг: {len(books)}.')
    return search_book


def list_books() -> str:
    """Выводит список книг."""

    data = check_data()
    print(f'Число книг на складе: {len(data)}.')
    for book_id, book in data.items():
        print(representation_book(book_id, book))
    return "Список книг успешно выведен."


def change_book_status(book_id, status) -> str:
    """Изменяет статус книги."""

    status = status.casefold()
    data = check_data()
    if status not in DICT_STATUS_BOOK.keys():
        raise ValueError('Неверное значение статуса.')
    if book_id not in data:
        raise ValueError(f'Книги с ID: {book_id} нет.')
    if data[book_id]['status'] == DICT_STATUS_BOOK[status]:
        raise ValueError(
            f'Статус книги с ID: {book_id} уже "{DICT_STATUS_BOOK[status]}".'
            )
    data[book_id]['status'] = DICT_STATUS_BOOK[status]
    if save_data(data):
        return (
            f'''
        Статус книги с ID: {book_id} изменен на "{DICT_STATUS_BOOK[status]}".
        '''
        )
    else:
        raise ValueError(
            f'Ошибка при изменении статуса книги с ID: {book_id}.'
            )


def main() -> None:
    """Основная функция."""

    first_start = True
    while True:
        print(start_menu(first_start))
        user_сhoice: str = input(
            'Выберите действие, введя соответствующую цифру: '
            ).strip()
        try:
            if user_сhoice not in map(str, range(1, 7)):
                raise ValueError(
                    f'Неверное значение: "{user_сhoice}" Попробуйте ещё раз.'
                    )

            if user_сhoice == '1':
                title = input('Введите название книги: ').strip()
                author = input('Введите автора книги: ').strip()
                year = input('Введите год издания книги: ').strip()
                print(add_book(title, author, year))
            elif user_сhoice == '2':
                book_id = input('Введите ID книги: ').strip()
                print(delete_book(book_id))
                print('Книга успешно удалена.')
            elif user_сhoice == '3':
                field = input(
                 'Введите поле для поиска: 1 - название, 2 - автор, 3 - год.'
                 '\n Ввод: '
                    ).strip().lower()
                query = input('Введите критерий поиска: ').strip()
                print(search_book(query, field))
                print('Поиск завершен.')
            elif user_сhoice == '4':
                print(list_books())
            elif user_сhoice == '5':
                book_id = input('Введите ID книги: ').strip()
                status = input(
                    'Введите статус книги: 1 - в наличии, 2 - выдана.'
                    '\n Ввод: '
                    ).strip()
                print(change_book_status(book_id, status))
            elif user_сhoice == '6':
                print('\n Программа завершена. Спасибо что в6ыбрали нас!')
                break

        except Exception as error:
            print(f'\n При работе программы возникло исключение: {error}')
        finally:
            first_start = False


if __name__ == "__main__":

    main()
