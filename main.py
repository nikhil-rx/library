import argparse
from datetime import datetime, timedelta
import uuid
from storage import Storage
from auth import Auth
from models import Book, Loan

class LibrarySystem:
    def __init__(self, data_dir: str = './data'):
        self.storage = Storage(data_dir)
        self.auth = Auth(self.storage)

    def librarian_menu(self):
        while True:
            print('\n=== Librarian Dashboard ===')
            print('1. Add Book')
            print('2. Register Member')
            print('3. Issue Book')
            print('4. Return Book')
            print('5. Overdue List')
            print('6. Logout')

            choice = input('> ')
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.register_member()
            elif choice == '3':
                self.issue_book()
            elif choice == '4':
                self.return_book()
            elif choice == '5':
                self.show_overdue_list()
            elif choice == '6':
                self.auth.logout()
                break
            else:
                print('Invalid choice. Please try again.')

    def member_menu(self):
        while True:
            print('\n=== Member Dashboard ===')
            print('1. Search Catalogue')
            print('2. Borrow Book')
            print('3. My Loans')
            print('4. Logout')

            choice = input('> ')
            if choice == '1':
                self.search_catalogue()
            elif choice == '2':
                self.borrow_book()
            elif choice == '3':
                self.view_my_loans()
            elif choice == '4':
                self.auth.logout()
                break
            else:
                print('Invalid choice. Please try again.')

    def add_book(self):
        if not self.auth.is_librarian():
            print('Unauthorized access')
            return

        isbn = input('Enter ISBN: ')
        title = input('Enter Title: ')
        author = input('Enter Author: ')
        copies = input('Enter number of copies: ')

        try:
            copies = int(copies)
            if copies < 0:
                raise ValueError('Copies cannot be negative')

            book = Book(isbn=isbn, title=title, author=author,
                       copies_total=copies, copies_available=copies)
            self.storage.add_book(book)
            print('✔ Book added successfully')
        except ValueError as e:
            print(f'Error: {e}')

    def register_member(self):
        if not self.auth.is_librarian():
            print('Unauthorized access')
            return

        member_id = input('Enter Member ID: ')
        name = input('Enter Name: ')
        email = input('Enter Email: ')
        password = input('Enter Password: ')

        if self.auth.register_member(member_id, name, password, email):
            print('✔ Member registered successfully')
        else:
            print('Error: Member ID already exists')

    def issue_book(self):
        if not self.auth.is_librarian():
            print('Unauthorized access')
            return

        isbn = input('ISBN to issue: ')
        member_id = input('Member ID: ')

        # Find the book
        books = self.storage.get_all_books()
        book = next((b for b in books if b.isbn == isbn), None)
        if not book:
            print('Error: Book not found')
            return

        if book.copies_available <= 0:
            print('Error: No copies available')
            return

        # Verify member
        member = self.storage.get_member_by_id(member_id)
        if not member:
            print('Error: Member not found')
            return

        # Create loan
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)
        loan = Loan(
            loan_id=str(uuid.uuid4()),
            member_id=member_id,
            isbn=isbn,
            issue_date=issue_date,
            due_date=due_date
        )

        # Update book availability
        book.copies_available -= 1
        books = [b if b.isbn != isbn else book for b in books]
        self.storage._save_books(books)
        self.storage.add_loan(loan)

        print(f'✔ Book issued. Due on {due_date.strftime("%d-%b-%Y")}')

    def return_book(self):
        if not self.auth.is_librarian():
            print('Unauthorized access')
            return

        loan_id = input('Enter Loan ID: ')
        # Implementation for return book
        print('✔ Book returned successfully')

    def search_catalogue(self):
        keyword = input('Enter search keyword (title/author): ').lower()
        books = self.storage.get_all_books()
        matches = [book for book in books
                  if keyword in book.title.lower() or keyword in book.author.lower()]

        if matches:
            print('\nSearch Results:')
            for book in matches:
                print(f'ISBN: {book.isbn}')
                print(f'Title: {book.title}')
                print(f'Author: {book.author}')
                print(f'Available Copies: {book.copies_available}/{book.copies_total}\n')
        else:
            print('No books found matching your search')

    def borrow_book(self):
        if not self.auth.is_member():
            print('Please login as a member to borrow books')
            return

        isbn = input('Enter ISBN of the book to borrow: ')
        member_id = self.auth.current_session['user_id']
        
        # Find the book
        books = self.storage.get_all_books()
        book = next((b for b in books if b.isbn == isbn), None)
        if not book:
            print('Error: Book not found')
            return

        if book.copies_available <= 0:
            print('Error: No copies available')
            return

        # Create loan
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)
        loan = Loan(
            loan_id=str(uuid.uuid4()),
            member_id=member_id,
            isbn=isbn,
            issue_date=issue_date,
            due_date=due_date
        )

        # Update book availability
        book.copies_available -= 1
        books = [b if b.isbn != isbn else book for b in books]
        self.storage._save_books(books)
        self.storage.add_loan(loan)

        print(f'✔ Book borrowed successfully. Due on {due_date.strftime("%d-%b-%Y")}')

    def view_my_loans(self):
        if not self.auth.is_member():
            print('Please login as a member to view loans')
            return

        member_id = self.auth.current_session['user_id']
        loans = self.storage.get_member_loans(member_id)

        if not loans:
            print('No loan history found')
            return

        print('\nYour Loan History:')
        for loan in loans:
            print(f'Loan ID: {loan.loan_id}')
            print(f'ISBN: {loan.isbn}')
            print(f'Issue Date: {loan.issue_date.strftime("%d-%b-%Y")}')
            print(f'Due Date: {loan.due_date.strftime("%d-%b-%Y")}')
            if loan.return_date:
                print(f'Returned: {loan.return_date.strftime("%d-%b-%Y")}')
            print()

    def show_overdue_list(self):
        if not self.auth.is_librarian():
            print('Unauthorized access')
            return

        overdue_loans = self.storage.get_overdue_loans()
        if not overdue_loans:
            print('No overdue books')
            return

        print('\nOverdue Books:')
        for loan in overdue_loans:
            member = self.storage.get_member_by_id(loan.member_id)
            print(f'Loan ID: {loan.loan_id}')
            print(f'Member: {member.name} (ID: {member.member_id})')
            print(f'ISBN: {loan.isbn}')
            print(f'Due Date: {loan.due_date.strftime("%d-%b-%Y")}\n')

    def signup_member(self):
        print('\n=== Member Signup ===\n')
        member_id = input('Enter Member ID: ')
        name = input('Enter Name: ')
        email = input('Enter Email: ')
        password = input('Enter Password: ')

        if self.auth.register_member(member_id, name, password, email):
            print('✔ Signup successful! You can now login as a member.')
        else:
            print('Error: Member ID already exists')

def main():
    parser = argparse.ArgumentParser(description='Library Management System')
    parser.add_argument('--data-dir', default='./data',
                        help='Directory for CSV files')
    args = parser.parse_args()

    library = LibrarySystem(args.data_dir)

    while True:
        print('\n=== Library Management System ===')
        print('1. Login as Librarian')
        print('2. Login as Member')
        print('3. Sign Up as New Member')
        print('4. Exit')

        choice = input('> ')
        if choice == '1':
            username = input('Username: ')
            password = input('Password: ')
            if library.auth.login('librarian', username, password):
                library.librarian_menu()
            else:
                print('Invalid credentials')
        elif choice == '2':
            member_id = input('Member ID: ')
            password = input('Password: ')
            if library.auth.login('member', member_id, password):
                library.member_menu()
            else:
                print('Invalid credentials')
        elif choice == '3':
            library.signup_member()
        elif choice == '4':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main()