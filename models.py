from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    isbn: str
    title: str
    author: str
    copies_total: int
    copies_available: int

@dataclass
class Member:
    member_id: str
    name: str
    password_hash: str
    email: str
    join_date: datetime

@dataclass
class Loan:
    loan_id: str
    member_id: str
    isbn: str
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None