import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from typing import Optional, Dict
import re
import os

from auth import Auth
from storage import Storage
from models import Book, Member, Loan

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Modern Library Management System")
        self.geometry("1200x800")
        self.configure(bg='#f0f0f0')

        # Initialize backend components
        self.storage = Storage()
        self.auth = Auth(self.storage)
        
        # Setup styles
        # Setup modern styles
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 12), background='#f0f0f0')
        self.style.configure('TButton', font=('Helvetica', 11), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 11), padding=5)
        self.style.configure('Accent.TButton', font=('Helvetica', 11, 'bold'), padding=10, background='#007bff')
        self.style.configure('TNotebook.Tab', padding=(10, 5))
        self.style.configure('TNotebook', background='#ffffff')
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'))

        # Create and set custom colors
        self.colors = {
            'primary': '#007bff',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }

        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Start with login screen
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_main_container()
        
        # Create a card-like frame for login
        login_card = ttk.Frame(self.main_container, style='Card.TFrame')
        login_card.pack(expand=True, padx=20, pady=20)

        # Add decorative header
        header_frame = ttk.Frame(login_card, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=2, pady=2)
        header_frame.configure(style='Header.TFrame')

        # Title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(title_frame, 
                               text="📚 Library Management System",
                               font=('Helvetica', 24, 'bold'),
                               foreground=self.colors['primary'])
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="Welcome back! Please login to continue",
                                  font=('Helvetica', 12),
                                  foreground=self.colors['dark'])
        subtitle_label.pack(pady=(5, 0))

        # Main content frame
        content_frame = ttk.Frame(login_card)
        content_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)

        # Role selection with modern styling
        role_frame = ttk.Frame(content_frame)
        role_frame.pack(pady=(0, 20))
        self.role_var = tk.StringVar(value='member')
        
        # Style the radio buttons
        for text, value in [('Member', 'member'), ('Librarian', 'librarian')]:
            rb = ttk.Radiobutton(role_frame, text=text, value=value,
                                variable=self.role_var,
                                style='TRadiobutton')
            rb.pack(side=tk.LEFT, padx=15)

        # Username field with icon
        username_frame = ttk.Frame(content_frame)
        username_frame.pack(fill=tk.X, pady=5)
        ttk.Label(username_frame, text="👤").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(username_frame, text="Username/ID:").pack(side=tk.LEFT)
        
        self.username_entry = ttk.Entry(content_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))

        # Password field with icon
        password_frame = ttk.Frame(content_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="🔒").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
        
        self.password_entry = ttk.Entry(content_frame, show='•', width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))

        # Modern login button
        login_button = ttk.Button(content_frame, text="Login",
                                command=self.handle_login,
                                style='Accent.TButton')
        login_button.pack(fill=tk.X, pady=10)

        # Separator
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=20)

        # Register link with modern styling
        register_frame = ttk.Frame(content_frame)
        register_frame.pack(pady=10)
        
        ttk.Label(register_frame,
                  text="New to our library?",
                  foreground=self.colors['dark']).pack(side=tk.LEFT)
        
        register_link = ttk.Label(register_frame,
                                 text="Create an account",
                                 cursor="hand2",
                                 foreground=self.colors['primary'])
        register_link.pack(side=tk.LEFT, padx=5)
        register_link.bind('<Button-1>', lambda e: self.show_register_screen())

        # Add keyboard bindings
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        role = self.role_var.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if self.auth.login(role, username, password):
            self.show_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_register_screen(self):
        self.clear_main_container()

        # Create a card-like frame for registration
        register_card = ttk.Frame(self.main_container, style='Card.TFrame')
        register_card.pack(expand=True, padx=20, pady=20)

        # Header section
        header_frame = ttk.Frame(register_card, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=2, pady=2)

        # Title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(title_frame,
                               text="📝 New Member Registration",
                               font=('Helvetica', 24, 'bold'),
                               foreground=self.colors['primary'])
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="Join our library community today!",
                                  font=('Helvetica', 12),
                                  foreground=self.colors['dark'])
        subtitle_label.pack(pady=(5, 0))

        # Main content frame
        content_frame = ttk.Frame(register_card)
        content_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)

        # Member ID field with icon
        id_frame = ttk.Frame(content_frame)
        id_frame.pack(fill=tk.X, pady=5)
        ttk.Label(id_frame, text="🆔").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(id_frame, text="Member ID:").pack(side=tk.LEFT)
        
        member_id_entry = ttk.Entry(content_frame, width=30)
        member_id_entry.pack(fill=tk.X, pady=(0, 15))

        # Name field with icon
        name_frame = ttk.Frame(content_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="👤").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(name_frame, text="Full Name:").pack(side=tk.LEFT)
        
        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.pack(fill=tk.X, pady=(0, 15))

        # Email field with icon
        email_frame = ttk.Frame(content_frame)
        email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(email_frame, text="📧").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(email_frame, text="Email:").pack(side=tk.LEFT)
        
        email_entry = ttk.Entry(content_frame, width=30)
        email_entry.pack(fill=tk.X, pady=(0, 15))

        # Password field with icon
        password_frame = ttk.Frame(content_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="🔒").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
        
        password_entry = ttk.Entry(content_frame, show='•', width=30)
        password_entry.pack(fill=tk.X, pady=(0, 20))

        def handle_register():
            member_id = member_id_entry.get().strip()
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()

            if not all([member_id, name, email, password]):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Invalid email format")
                return

            if self.auth.register_member(member_id, name, password, email):
                messagebox.showinfo("Success", "Registration successful! Please login.")
                self.show_login_screen()
            else:
                messagebox.showerror("Error", "Member ID already exists")

        # Register button with modern styling
        register_button = ttk.Button(content_frame,
                                   text="Create Account",
                                   command=handle_register,
                                   style='Accent.TButton')
        register_button.pack(fill=tk.X, pady=10)

        # Separator
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=20)

        # Back to login with modern styling
        login_frame = ttk.Frame(content_frame)
        login_frame.pack(pady=10)
        
        ttk.Label(login_frame,
                  text="Already have an account?",
                  foreground=self.colors['dark']).pack(side=tk.LEFT)
        
        back_link = ttk.Label(login_frame,
                             text="Login here",
                             cursor="hand2",
                             foreground=self.colors['primary'])
        back_link.pack(side=tk.LEFT, padx=5)
        back_link.bind('<Button-1>', lambda e: self.show_login_screen())

        # Add keyboard bindings for better UX
        member_id_entry.bind('<Return>', lambda e: name_entry.focus())
        name_entry.bind('<Return>', lambda e: email_entry.focus())
        email_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: handle_register())

    def show_main_screen(self):
        self.clear_main_container()
        
        # Create and show the dashboard screen
        from gui.dashboard import DashboardScreen
        dashboard = DashboardScreen(self.main_container, self)
        dashboard.pack(fill=tk.BOTH, expand=True)

        # Create menu bar
        menu_frame = ttk.Frame(self.main_container)
        menu_frame.pack(fill=tk.X, pady=(0, 20))

        user = self.auth.get_current_user()
        welcome_text = f"Welcome, {'Librarian' if self.auth.is_librarian() else 'Member'}: {user['user_id']}"
        ttk.Label(menu_frame, text=welcome_text, 
                 font=('Helvetica', 14)).pack(side=tk.LEFT, padx=10)

        ttk.Button(menu_frame, text="Logout", 
                  command=self.handle_logout).pack(side=tk.RIGHT, padx=10)

        # Create notebook for different sections
        notebook = ttk.Notebook(self.main_container)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Books tab
        books_frame = ttk.Frame(notebook)
        self.setup_books_tab(books_frame)
        notebook.add(books_frame, text='Books')

        # Loans tab
        loans_frame = ttk.Frame(notebook)
        self.setup_loans_tab(loans_frame)
        notebook.add(loans_frame, text='Loans')

        if self.auth.is_librarian():
            # Members tab (librarian only)
            members_frame = ttk.Frame(notebook)
            self.setup_members_tab(members_frame)
            notebook.add(members_frame, text='Members')

    def setup_books_tab(self, parent):
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Books table
        columns = ('ISBN', 'Title', 'Author', 'Available', 'Total')
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate books
        for book in self.storage.get_all_books():
            tree.insert('', tk.END, values=(book.isbn, book.title, book.author, 
                                          book.copies_available, book.copies_total))

        if self.auth.is_librarian():
            # Add book button (librarian only)
            add_button = ttk.Button(parent, text="Add New Book", 
                                  command=lambda: self.show_add_book_dialog())
            add_button.pack(pady=10)

    def setup_loans_tab(self, parent):
        # Loans table
        columns = ('Loan ID', 'Member ID', 'ISBN', 'Issue Date', 'Due Date', 'Return Date')
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate loans based on role
        if self.auth.is_librarian():
            loans = self.storage.get_all_loans()
        else:
            user = self.auth.get_current_user()
            loans = self.storage.get_member_loans(user['user_id'])

        for loan in loans:
            tree.insert('', tk.END, values=(
                loan.loan_id, loan.member_id, loan.isbn,
                loan.issue_date.strftime('%Y-%m-%d'),
                loan.due_date.strftime('%Y-%m-%d'),
                loan.return_date.strftime('%Y-%m-%d') if loan.return_date else 'Not Returned'
            ))

    def setup_members_tab(self, parent):
        # Members table
        columns = ('Member ID', 'Name', 'Email', 'Join Date')
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate members
        for member in self.storage.get_all_members():
            tree.insert('', tk.END, values=(
                member.member_id, member.name, member.email,
                member.join_date.strftime('%Y-%m-%d')
            ))

    def show_add_book_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Book")
        dialog.geometry("400x300")

        ttk.Label(dialog, text="ISBN:").pack(pady=5)
        isbn_entry = ttk.Entry(dialog, width=30)
        isbn_entry.pack(pady=5)

        ttk.Label(dialog, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=30)
        title_entry.pack(pady=5)

        ttk.Label(dialog, text="Author:").pack(pady=5)
        author_entry = ttk.Entry(dialog, width=30)
        author_entry.pack(pady=5)

        ttk.Label(dialog, text="Number of Copies:").pack(pady=5)
        copies_entry = ttk.Entry(dialog, width=30)
        copies_entry.pack(pady=5)

        def handle_add_book():
            isbn = isbn_entry.get().strip()
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            try:
                copies = int(copies_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Copies must be a number")
                return

            if not all([isbn, title, author]):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            new_book = Book(isbn=isbn, title=title, author=author,
                          copies_total=copies, copies_available=copies)
            self.storage.add_book(new_book)
            messagebox.showinfo("Success", "Book added successfully")
            dialog.destroy()
            self.show_main_screen()

        ttk.Button(dialog, text="Add Book", 
                  command=handle_add_book).pack(pady=20)

    def handle_logout(self):
        self.auth.logout()
        self.show_login_screen()

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()