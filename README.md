# Library Management System

A comprehensive library management system implemented in Python, featuring user authentication, book management, and loan tracking functionality.

## Features

- **User Authentication**
  - Separate login for librarians and members
  - Member registration system
  - Secure password handling

- **Book Management**
  - Add new books to the library
  - Track multiple copies of books
  - Search catalogue by title or author

- **Loan System**
  - Issue books to members
  - Track due dates
  - Monitor overdue books
  - View loan history

## Technical Implementation

### Data Structures
- **Hash Tables**: Used for efficient member and book lookup operations
- **Lists**: Implemented for managing book collections and loan records
- **CSV File Storage**: Persistent data storage using CSV format

### Algorithms
- **Search Algorithm**: Implemented case-insensitive search for book catalogue
- **UUID Generation**: Unique identifier generation for loans
- **Date Handling**: Automated due date calculation and overdue checking

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Default librarian credentials:
   - Username: admin
   - Password: admin

3. Members can:
   - Sign up for a new account
   - Search the catalogue
   - Borrow books
   - View their loan history

4. Librarians can:
   - Add new books
   - Register members
   - Issue books
   - Process returns
   - View overdue list

## Testing

Run the test suite:
```bash
pytest -q test_library.py
```

## Project Structure

```
.
├── main.py          # Main application entry point
├── models.py        # Data models
├── auth.py          # Authentication system
├── storage.py       # Data persistence
├── test_library.py  # Test suite
├── requirements.txt # Dependencies
└── data/           # Data storage directory
    ├── books.csv
    ├── members.csv
    └── loans.csv
```

## Error Handling

- Input validation for all user inputs
- Proper error messages for:
  - Invalid credentials
  - Duplicate member IDs
  - Non-existent books
  - Insufficient book copies
  - Invalid loan operations

## Future Enhancements

- GUI interface
- Email notifications for due dates
- Fine calculation system
- Book reservation system
- Report generation