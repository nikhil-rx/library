import pytest
from datetime import datetime, timedelta
from models import Book, Member, Loan
from storage import Storage
from auth import Auth
from main import LibrarySystem
import os
import shutil

@pytest.fixture
def test_data_dir():
    test_dir = './test_data'
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    shutil.rmtree(test_dir)

@pytest.fixture
def library_system(test_data_dir):
    return LibrarySystem(test_data_dir)

@pytest.fixture
def sample_book():
    return Book(
        isbn='1234567890',
        title='Test Book',
        author='Test Author',
        copies_total=3,
        copies_available=3
    )

@pytest.fixture
def sample_member():
    return {
        'member_id': 'TEST001',
        'name': 'Test User',
        'password': 'testpass123',
        'email': 'test@example.com'
    }

def test_add_book(library_system, sample_book):
    library_system.storage.add_book(sample_book)
    books = library_system.storage.get_all_books()
    assert any(b.isbn == sample_book.isbn for b in books)

def test_register_member(library_system, sample_member):
    result = library_system.auth.register_member(
        sample_member['member_id'],
        sample_member['name'],
        sample_member['password'],
        sample_member['email']
    )
    assert result == True

def test_member_login(library_system, sample_member):
    library_system.auth.register_member(
        sample_member['member_id'],
        sample_member['name'],
        sample_member['password'],
        sample_member['email']
    )
    result = library_system.auth.login('member', sample_member['member_id'], sample_member['password'])
    assert result == True

def test_issue_book(library_system, sample_book, sample_member):
    # Setup
    library_system.storage.add_book(sample_book)
    library_system.auth.register_member(
        sample_member['member_id'],
        sample_member['name'],
        sample_member['password'],
        sample_member['email']
    )
    
    # Issue book
    library_system.auth.login('librarian', 'admin', 'admin')
    initial_copies = sample_book.copies_available
    
    # Create loan
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=14)
    loan = Loan(
        loan_id='TEST_LOAN_001',
        member_id=sample_member['member_id'],
        isbn=sample_book.isbn,
        issue_date=issue_date,
        due_date=due_date
    )
    library_system.storage.add_loan(loan)
    
    # Verify
    books = library_system.storage.get_all_books()
    updated_book = next(b for b in books if b.isbn == sample_book.isbn)
    assert updated_book.copies_available == initial_copies - 1

def test_search_catalogue(library_system, sample_book):
    library_system.storage.add_book(sample_book)
    books = library_system.storage.get_all_books()
    matches = [book for book in books
              if sample_book.title.lower() in book.title.lower() or 
              sample_book.author.lower() in book.author.lower()]
    assert len(matches) > 0
    assert matches[0].isbn == sample_book.isbn