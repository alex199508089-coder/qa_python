import pytest
from main import BooksCollector


class TestBooksCollector:

    # 1a. Валидные названия
    @pytest.mark.parametrize("name", ["A", "Война и мир", "A" * 40]) [
    def test_add_new_book_valid_names(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.books_genre
        assert collector.get_book_genre(name) == ""

        # 1b. Невалидные названия
    @pytest.mark.parametrize("name", ["", "A" * 41])
    def test_add_new_book_invalid_names(self, collector, name):
        collector.add_new_book(name)
        assert name not in collector.books_genre


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
                ["Винни-Пух"]
        ),
        (
                [("Шерлок Холмс", "Детективы"), ("Кладбище домашних животных", "Ужасы")],
                []
        ),
        (
                [("Гарри Поттер", "Фантастика"), ("Карлсон", "Мультфильмы")],
                ["Гарри Поттер", "Карлсон"]
        )
    ])
    def test_get_books_for_children(self, collector, books_data, expected_children):
        for name, genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert collector.get_books_for_children() == expected_children

        # 8a. Добавление существующей книги в избранное (с проверкой дубля)

    @pytest.mark.parametrize("call_times, expected_length", [(1, 1), (2, 1)])
    def test_add_existing_book_to_favorites(self, collector, call_times, expected_length):
        collector.add_new_book("Муха-Цокотуха")
        for _ in range(call_times):
            collector.add_book_in_favorites("Муха-Цокотуха")
        assert len(collector.favorites) == expected_length
        assert "Муха-Цокотуха" in collector.favorites

    # 8b. Добавление несуществующей книги в избранное
    def test_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites("Неизвестная")
        assert len(collector.favorites) == 0
        assert "Неизвестная" not in collector.favorites

        # 9a. Удаление книги, которая есть в избранном

    def test_delete_existing_book_from_favorites(self, collector):
        collector.add_new_book("Буратино")
        collector.add_book_in_favorites("Буратино")
        collector.delete_book_from_favorites("Буратино")
        assert "Буратино" not in collector.favorites

        # 9b. Удаление книги, которой нет в избранном

    def test_delete_nonexistent_book_from_favorites(self, collector):
        collector.add_new_book("Буратино")  # книга есть в словаре, но не в избранном
        collector.delete_book_from_favorites("Буратино")
        assert "Буратино" not in collector.favorites

    # 10. Тест метода get_list_of_favorites_books
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Сказка о царе Султане")
        collector.add_new_book("Руслан и Людмила")
        collector.add_book_in_favorites("Сказка о царе Султане")
        assert collector.get_list_of_favorites_books() == ["Сказка о царе Султане"]