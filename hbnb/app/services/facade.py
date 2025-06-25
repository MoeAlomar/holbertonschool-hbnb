from app.models.amenity import Amenity
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        allowed_fields = ['name']
        filtered_data = {k: v for k, v in amenity_data.items() if k in allowed_fields}
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in filtered_data:
            existing_amenity = self.amenity_repo.get_by_attribute('name', filtered_data['name'])
            if existing_amenity and existing_amenity.id != amenity_id:
                return {'error': 'An amenity with this name already exists'}
        amenity.update(filtered_data)
        return amenity

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"User with id {owner_id} not found")

        # Remove 'owner_id' from place_data to avoid passing it to Place's __init__
        place_data = dict(place_data)  # Create a copy to avoid mutating original
        del place_data['owner_id']

        # Pass the owner object to the Place constructor
        place = Place(owner=owner, **place_data)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def get_place_by_title(self, title):
        self.place_repo.get_by_attribute('title', title)

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'amenities']
        filtered_data = {k: v for k, v in place_data.items() if k in allowed_fields}
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if 'title' in filtered_data:
            existing_place = self.place_repo.get_by_attribute('title', filtered_data['title'])
            if existing_place and existing_place.id != place_id:
                return {'error': 'A place with this title already exists'}
            place.update(filtered_data)

