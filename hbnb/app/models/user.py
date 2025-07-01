from .BaseModel import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        self.validate_User(first_name, last_name, email) # validate password later

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # Should be hashed in a real app
        self.is_admin = bool(is_admin)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)

    def validate_User(self, first_name, last_name, email):
        if not first_name or not last_name or not email:
            raise ValueError("All user fields are required.")
        if not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("First name must be string, max 50 characters")
        if not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Last name must be string, max 50 characters")
        if first_name.isalpha() == False or last_name.isalpha() == False:
            raise ValueError("first name and last name must be characters")
        if not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")