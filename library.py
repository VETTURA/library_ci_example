import datetime
from typing import Optional


class Book:
    """
    Представляет книгу в библиотеке.

    Атрибуты:
        title (str): Название книги.
        author (str): Автор книги.
        isbn (str): ISBN книги.
        is_borrowed (bool): Флаг, указывающий, взята ли книга.
        borrower (Member): Читатель, который взял книгу.
        return_date (date): Дата, до которой книга должна быть возвращена.
    """

    def __init__(self, title: str, author: str, isbn: str):
        """
        Инициализация книги.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            isbn (str): ISBN книги.
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
        self.borrower: Optional['Member'] = None
        self.return_date: Optional[datetime.date] = None

    def borrow(self, member: 'Member', return_date: datetime.date) -> bool:
        """
        Позволяет читателю взять книгу.

        Args:
            member (Member): Читатель, берущий книгу.
            return_date (date): Дата возврата.

        Returns:
            bool: True, если операция прошла успешно, иначе False.
        """
        if self.is_borrowed:
            print(f"Книга '{self.title}' уже взята.")
            return False
        self.is_borrowed = True
        self.borrower = member
        self.return_date = return_date
        print(f"Книга '{self.title}' успешно взята {member.name}.")
        return True

    def return_book(self) -> bool:
        """
        Позволяет вернуть книгу в библиотеку.

        Returns:
            bool: True, если книга успешно возвращена, иначе False.
        """
        if not self.is_borrowed:
            print(f"Книга '{self.title}' не была взята.")
            return False
        self.is_borrowed = False
        self.borrower = None
        self.return_date = None
        print(f"Книга '{self.title}' успешно возвращена.")
        return True


class Member:
    """
    Представляет читателя библиотеки.

    Атрибуты:
        name (str): Имя читателя.
        membership_id (int): Идентификатор читателя.
        borrowed_books (list): Список взятых книг.
    """

    def __init__(self, name: str, membership_id: int):
        """
        Инициализация читателя.

        Args:
            name (str): Имя читателя.
            membership_id (int): Идентификатор читателя.
        """
        self.name = name
        self.membership_id = membership_id
        self.borrowed_books: list[Book] = []

    def borrow_book(self, book: Book, return_date: datetime.date) -> None:
        """
        Читатель берет книгу.

        Args:
            book (Book): Книга для взятия.
            return_date (date): Дата возврата.
        """
        if book.borrow(self, return_date):
            self.borrowed_books.append(book)

    def return_book(self, book: Book, return_date: datetime.date) -> None:
        """
        Читатель возвращает книгу.

        Args:
            book (Book): Книга, которую возвращают.
            return_date (date): Фактическая дата возврата.
        """
        if book.is_borrowed:
            self.borrowed_books.remove(book)
            fine = Library.calculate_fine(book, return_date)
            if fine > 0:
                print(f"Штраф за просрочку книги '{book.title}' составляет {fine} рублей.")
            else:
                print(f"Книга '{book.title}' возвращена без штрафа.")
            book.return_book()

    def get_overdue_books(self) -> list[Book]:
        """
        Возвращает список просроченных книг.

        Returns:
            list: Список книг с истекшим сроком возврата.
        """
        overdue_books = []
        for book in self.borrowed_books:
            if book.return_date is not None and book.return_date < datetime.date.today():
                overdue_books.append(book)
        return overdue_books


class Library:
    """
    Представляет библиотеку, содержащую книги и читателей.
    """

    def __init__(self) -> None:
        """
        Инициализация библиотеки.
        """
        self.books: list[Book] = []
        self.members: list[Member] = []

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу в библиотеку.

        Args:
            book (Book): Книга для добавления.
        """
        self.books.append(book)

    def remove_book(self, isbn: str) -> None:
        """
        Удаляет книгу по ISBN.

        Args:
            isbn (str): ISBN книги.
        """
        book_to_remove = None
        for book in self.books:
            if book.isbn == isbn:
                book_to_remove = book
                break
        if book_to_remove:
            if not book_to_remove.is_borrowed:
                self.books.remove(book_to_remove)
                print(f"Книга '{book_to_remove.title}' удалена из библиотеки.")
            else:
                print("Сейчас книгу нельзя удалить, она не в библиотеке.")
        else:
            print("Книга с таким ISBN не найдена.")

    def add_member(self, member: Member) -> None:
        """
        Добавляет нового читателя.

        Args:
            member (Member): Новый читатель.
        """
        self.members.append(member)

    def remove_member(self, membership_id: int) -> None:
        """
        Удаляет читателя по ID.

        Args:
            membership_id (int): ID читателя.
        """
        member_to_remove = None
        for member in self.members:
            if member.membership_id == membership_id:
                member_to_remove = member
                break
        if member_to_remove:
            if not member_to_remove.borrowed_books:
                self.members.remove(member_to_remove)
                print(f"Читатель {member_to_remove.name} удален из библиотеки.")
            else:
                print("Читателя нельзя удалить, у него еще остались книги.")
        else:
            print("Читатель с таким ID не найден.")

    def get_book_by_isbn(self, isbn: str) -> Book | None:
        """
        Возвращает книгу по ISBN.

        Args:
            isbn (str): ISBN книги.

        Returns:
            Book | None: Найденная книга или None.
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    @staticmethod
    def calculate_fine(book: Book, return_date: datetime.date) -> int:
        """
        Рассчитывает штраф за просрочку книги.

        Args:
            book (Book): Книга.
            return_date (date): Дата возврата.

        Returns:
            int: Сумма штрафа в рублях.
        """
        if book.return_date is not None:
            if return_date <= book.return_date:
                return 0
            overdue_days = (return_date - book.return_date).days
            fine = overdue_days * 10
            return fine
        else:
            return 0


# Пример работы
if __name__ == "__main__":
    library = Library()

    book1 = Book("Война и мир", "Лев Толстой", "978-5-0001-0000-1")
    book2 = Book("1984", "Джордж Оруэлл", "978-0-452-28423-4")
    library.add_book(book1)
    library.add_book(book2)

    member1 = Member("Иван Иванов", 1)
    member2 = Member("Мария Петрова", 2)
    library.add_member(member1)
    library.add_member(member2)

    member1.borrow_book(book1, datetime.date(2025, 4, 15))

    print("\n--- Читатель возвращает книгу ---")
    return_date = datetime.date(2025, 4, 20)
    member1.return_book(book1, return_date)

    print("\n--- Читатель возвращает книгу без просрочки ---")
    return_date = datetime.date(2025, 4, 10)
    member1.return_book(book1, return_date)

    library.remove_book("978-0-452-28423-4")
    library.remove_member(2)
