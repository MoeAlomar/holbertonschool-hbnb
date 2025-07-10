from app.extensions import db, bcrypt
from .BaseModel import BaseModel
import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships



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