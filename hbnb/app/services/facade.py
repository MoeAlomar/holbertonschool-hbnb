# from app.models import place, review, amenity
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.user_repository import UserRepository



class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_user_by_email(email)

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



    # Amenity area #


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



    # Place area #

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=owner.id  # ✅ CORRECT: use owner_id, not `owner`
            )

        except ValueError as e:
            raise ValueError(str(e))

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        for field in allowed_fields:
            if field in place_data:
                try:
                    setattr(place, field, place_data[field])
                except ValueError as e:
                    raise ValueError(str(e))

        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner

        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                amenities.append(amenity)
            place.amenities = amenities

        place.save()
        return place


    # Review area #

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=text,
            rating=rating,
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        place.reviews.append(review)
        self.place_repo.update_obj(place)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None  # So your API can return 404

        print(f"Fetching reviews for place: {place_id}")
        return [
            review for review in self.review_repo.get_all()
            if review.place.id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        review.place.reviews.remove(review)
        self.review_repo.delete(review_id)
        return True
