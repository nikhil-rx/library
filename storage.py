import csv
import os
from datetime import datetime
from typing import List, Optional
from models import Book, Member, Loan

class Storage:
    def __init__(self, data_dir: str = './data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.books_file = os.path.join(data_dir, 'books.csv')
        self.members_file = os.path.join(data_dir, 'members.csv')
        self.loans_file = os.path.join(data_dir, 'loans.csv')
        self._initialize_files()

    def _initialize_files(self):
        # Initialize books.csv
        if not os.path.exists(self.books_file):
            with open(self.books_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ISBN', 'Title', 'Author', 'CopiesTotal', 'CopiesAvailable'])

        # Initialize members.csv
        if not os.path.exists(self.members_file):
            with open(self.members_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['MemberID', 'Name', 'PasswordHash', 'Email', 'JoinDate'])

        # Initialize loans.csv
        if not os.path.exists(self.loans_file):
            with open(self.loans_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['LoanID', 'MemberID', 'ISBN', 'IssueDate', 'DueDate', 'ReturnDate'])

    def get_all_books(self) -> List[Book]:
        books = []
        with open(self.books_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(Book(
                    isbn=row['ISBN'],
                    title=row['Title'],
                    author=row['Author'],
                    copies_total=int(row['CopiesTotal']),
                    copies_available=int(row['CopiesAvailable'])
                ))
        return books

    def add_book(self, book: Book) -> None:
        books = self.get_all_books()
        books.append(book)
        self._save_books(books)

    def _save_books(self, books: List[Book]) -> None:
        with open(self.books_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ISBN', 'Title', 'Author', 'CopiesTotal', 'CopiesAvailable'])
            for book in books:
                writer.writerow([book.isbn, book.title, book.author, book.copies_total, book.copies_available])

    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        with open(self.members_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['MemberID'] == member_id:
                    return Member(
                        member_id=row['MemberID'],
                        name=row['Name'],
                        password_hash=row['PasswordHash'],
                        email=row['Email'],
                        join_date=datetime.strptime(row['JoinDate'], '%Y-%m-%d')
                    )
        return None

    def add_member(self, member: Member) -> None:
        with open(self.members_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                member.member_id,
                member.name,
                member.password_hash,
                member.email,
                member.join_date.strftime('%Y-%m-%d')
            ])

    def add_loan(self, loan: Loan) -> None:
        with open(self.loans_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                loan.loan_id,
                loan.member_id,
                loan.isbn,
                loan.issue_date.strftime('%Y-%m-%d'),
                loan.due_date.strftime('%Y-%m-%d'),
                loan.return_date.strftime('%Y-%m-%d') if loan.return_date else ''
            ])

    def get_member_loans(self, member_id: str) -> List[Loan]:
        loans = []
        with open(self.loans_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['MemberID'] == member_id:
                    return_date = None
                    if row['ReturnDate']:
                        return_date = datetime.strptime(row['ReturnDate'], '%Y-%m-%d')
                    loans.append(Loan(
                        loan_id=row['LoanID'],
                        member_id=row['MemberID'],
                        isbn=row['ISBN'],
                        issue_date=datetime.strptime(row['IssueDate'], '%Y-%m-%d'),
                        due_date=datetime.strptime(row['DueDate'], '%Y-%m-%d'),
                        return_date=return_date
                    ))
        return loans

    def get_overdue_loans(self) -> List[Loan]:
        today = datetime.now()
        overdue_loans = []
        with open(self.loans_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['ReturnDate']:
                    due_date = datetime.strptime(row['DueDate'], '%Y-%m-%d')
                    if due_date < today:
                        overdue_loans.append(Loan(
                            loan_id=row['LoanID'],
                            member_id=row['MemberID'],
                            isbn=row['ISBN'],
                            issue_date=datetime.strptime(row['IssueDate'], '%Y-%m-%d'),
                            due_date=due_date
                        ))
        return overdue_loans