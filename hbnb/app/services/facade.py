from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user information with email uniqueness check"""
        allowed_fields = ['first_name', 'last_name', 'email']
        filtered_data = {k: v for k, v in user_data.items() if k in allowed_fields}
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if 'email' in filtered_data:
            existing_user = self.user_repo.get_by_attribute('email', filtered_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}
        user.update(filtered_data)
        return user


