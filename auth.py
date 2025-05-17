import bcrypt
from typing import Optional, Dict, Literal
from datetime import datetime
from models import Member
from storage import Storage

Role = Literal['librarian', 'member']

class Auth:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.current_session: Dict[str, str] = {}
        # Initialize with secure default admin account
        self._admin_username = 'admin'
        self._admin_password_hash = bcrypt.hashpw('LibAdmin@2024'.encode(), bcrypt.gensalt())

    def register_member(self, member_id: str, name: str, password: str, email: str) -> bool:
        """Register a new member with hashed password."""
        if self.storage.get_member_by_id(member_id):
            return False

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_member = Member(
            member_id=member_id,
            name=name,
            password_hash=password_hash.decode(),
            email=email,
            join_date=datetime.now()
        )
        self.storage.add_member(new_member)
        return True

    def login(self, role: Role, username: str, password: str) -> bool:
        """Login as either librarian or member."""
        if role == 'librarian':
            if username == self._admin_username and bcrypt.checkpw(
                password.encode(), self._admin_password_hash
            ):
                self.current_session['role'] = 'librarian'
                self.current_session['user_id'] = username
                return True
            return False

        member = self.storage.get_member_by_id(username)
        if member and bcrypt.checkpw(password.encode(), member.password_hash.encode()):
            self.current_session['role'] = 'member'
            self.current_session['user_id'] = username
            return True
        return False

    def logout(self) -> None:
        """Clear the current session."""
        self.current_session.clear()

    def get_current_user(self) -> Optional[Dict[str, str]]:
        """Get the current logged-in user's information."""
        return self.current_session if self.current_session else None

    def is_librarian(self) -> bool:
        """Check if the current user is a librarian."""
        return self.current_session.get('role') == 'librarian'

    def is_member(self) -> bool:
        """Check if the current user is a member."""
        return self.current_session.get('role') == 'member'