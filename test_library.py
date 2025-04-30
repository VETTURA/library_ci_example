import datetime
import pytest
from library import Book, Member, Library


@pytest.fixture
def setup_library():
    library = Library()
    book = Book("Преступление и наказание", "Ф. Достоевский", "123-456")
    member = Member("Анна Каренина", 1001)
    library.add_book(book)
    library.add_member(member)
    return library, book, member


def test_borrow_book_success(setup_library):
    library, book, member = setup_library
    return_date = datetime.date.today() + datetime.timedelta(days=7)
    member.borrow_book(book, return_date)

    assert book.is_borrowed is True
    assert book.borrower == member
    assert book.return_date == return_date
    assert book in member.borrowed_books


def test_borrow_book_already_taken(setup_library):
    library, book, member = setup_library
    return_date = datetime.date.today() + datetime.timedelta(days=7)

    member.borrow_book(book, return_date)
    result = book.borrow(member, return_date)

    assert result is False


def test_return_book_no_fine(setup_library):
    library, book, member = setup_library
    return_date = datetime.date.today() + datetime.timedelta(days=7)
    member.borrow_book(book, return_date)

    return_date = return_date
    member.return_book(book, return_date)

    assert book.is_borrowed is False
    assert book.borrower is None
    assert book.return_date is None
    assert book not in member.borrowed_books


def test_return_book_with_fine(setup_library):
    library, book, member = setup_library
    return_date = datetime.date.today() - datetime.timedelta(days=5)
    member.borrow_book(book, return_date)

    return_date = datetime.date.today()
    fine = Library.calculate_fine(book, return_date)

    assert fine == 5 * 10  # 10 рублей за день


def test_return_unborrowed_book(setup_library):
    _, book, _ = setup_library
    result = book.return_book()

    assert result is False


def test_get_overdue_books(setup_library):
    _, book, member = setup_library
    past_due = datetime.date.today() - datetime.timedelta(days=3)
    member.borrow_book(book, past_due)

    overdue_books = member.get_overdue_books()

    assert book in overdue_books


def test_add_and_remove_book(setup_library):
    library, book, _ = setup_library
    isbn = book.isbn

    library.remove_book(isbn)
    assert library.get_book_by_isbn(isbn) is None


def test_add_and_remove_member(setup_library):
    library, _, member = setup_library
    member_id = member.membership_id

    library.remove_member(member_id)
    ids = [m.membership_id for m in library.members]
    assert member_id not in ids
