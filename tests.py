import pytest
from main import BooksCollector


class TestBooksCollector:

    # 1. Тест метода add_new_book — валидные и невалидные названия (параметризованный)
    @pytest.mark.parametrize("name, expected_in_dict, expected_genre", [
        ("A", True, ""),                     # 1 символ
        ("Война и мир", True, ""),           # кириллица
        ("A" * 40, True, ""),                # ровно 40 символов
        ("", False, None),                   # пустая строка
        ("A" * 41, False, None)              # 41 символ
    ])
    def test_add_new_book(self, name, expected_in_dict, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected_in_dict
        if expected_in_dict:
            assert collector.get_book_genre(name) == expected_genre

    # 2. Тест: повторное добавление книги не перезаписывает её жанр
    def test_add_new_book_duplicate_preserves_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Колобок")
        collector.set_book_genre("Колобок", "Мультфильмы")
        collector.add_new_book("Колобок")          # попытка добавить повторно
        assert collector.get_book_genre("Колобок") == "Мультфильмы"

    # 3. Тест метода set_book_genre (параметризованный)
    @pytest.mark.parametrize("name, genre, expected_genre", [
        ("Мастер и Маргарита", "Фантастика", "Фантастика"),   # книга есть, жанр допустим
        ("Мастер и Маргарита", "Роман", ""),                  # книга есть, жанр недопустим
        ("Несуществующая", "Фантастика", None)                # книги нет в словаре
    ])
    def test_set_book_genre(self, name, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book("Мастер и Маргарита")
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected_genre

    # 4. Тест метода get_book_genre (параметризованный)
    @pytest.mark.parametrize("name, expected", [
        ("Война и мир", "Фантастика"),   # жанр установлен
        ("Без жанра", ""),               # книга без жанра
        ("Неизвестная", None)            # книга отсутствует
    ])
    def test_get_book_genre(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Фантастика")
        collector.add_new_book("Без жанра")   # жанр не задаём
        assert collector.get_book_genre(name) == expected

    # 5. Тест метода get_books_with_specific_genre (параметризованный)
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Пикник на обочине"]),
        ("Детективы", []),                     # книг с таким жанром нет
        ("Роман", []),                         # жанр не в списке допустимых
        ("Мультфильмы", [])                    # жанр допустим, но книг нет
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book("Пикник на обочине")
        collector.set_book_genre("Пикник на обочине", "Фантастика")
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_books_with_specific_genre(genre) == expected_books

    # 6. Тест метода get_books_genre
    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Алиса в стране чудес")
        collector.set_book_genre("Алиса в стране чудес", "Мультфильмы")
        collector.add_new_book("Преступление и наказание")
        expected = {
            "Алиса в стране чудес": "Мультфильмы",
            "Преступление и наказание": ""
        }
        assert collector.get_books_genre() == expected

    # 7. Тест метода get_books_for_children (параметризованный)
    @pytest.mark.parametrize("books_data, expected_children", [
        (
            [("Винни-Пух", "Мультфильмы"), ("Оно", "Ужасы"), ("Три товарища", "")],
            ["Винни-Пух"]                     # книга без жанра не подходит
        ),
        (
            [("Шерлок Холмс", "Детективы"), ("Кладбище домашних животных", "Ужасы")],
            []                                # все книги с возрастным рейтингом
        ),
        (
            [("Гарри Поттер", "Фантастика"), ("Карлсон", "Мультфильмы")],
            ["Гарри Поттер", "Карлсон"]       # обе подходят детям
        )
    ])
    def test_get_books_for_children(self, books_data, expected_children):
        collector = BooksCollector()
        for name, genre in books_data:
            collector.add_new_book(name)
            if genre:
                collector.set_book_genre(name, genre)
        assert collector.get_books_for_children() == expected_children

    # 8. Тест метода add_book_in_favorites (параметризованный, включая проверку на дубли)
    @pytest.mark.parametrize("name, add_to_books, call_times, expected_length", [
        ("Муха-Цокотуха", True, 1, 1),    # книга есть, добавляется 1 раз
        ("Неизвестная", False, 1, 0),     # книги нет, не добавляется
        ("Муха-Цокотуха", True, 2, 1)     # дважды одна и та же книга — дубля нет
    ])
    def test_add_book_in_favorites(self, name, add_to_books, call_times, expected_length):
        collector = BooksCollector()
        if add_to_books:
            collector.add_new_book(name)
        for _ in range(call_times):
            collector.add_book_in_favorites(name)
        assert len(collector.favorites) == expected_length
        if expected_length > 0:
            assert name in collector.favorites

    # 9. Тест метода delete_book_from_favorites (параметризованный)
    @pytest.mark.parametrize("name, in_favorites_initially, expected_after_delete", [
        ("Буратино", True, False),   # удаление существующей в избранном книги
        ("Буратино", False, False)   # удаление книги, которой нет в избранном
    ])
    def test_delete_book_from_favorites(self, name, in_favorites_initially, expected_after_delete):
        collector = BooksCollector()
        collector.add_new_book(name)
        if in_favorites_initially:
            collector.add_book_in_favorites(name)
        collector.delete_book_from_favorites(name)
        assert (name in collector.favorites) == expected_after_delete

    # 10. Тест метода get_list_of_favorites_books
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Сказка о царе Султане")
        collector.add_new_book("Руслан и Людмила")
        collector.add_book_in_favorites("Сказка о царе Султане")
        assert collector.get_list_of_favorites_books() == ["Сказка о царе Султане"]