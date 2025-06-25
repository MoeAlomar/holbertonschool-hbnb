from .BaseModel import BaseModel
from .user import User
from .amenity import  Amenity
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.validate_Place(title, description, price, latitude, longitude, owner)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities


    def validate_Place(self, title, description, price, latitude, longitude, owner):
        if not title or not price or not latitude or not longitude or not owner:
            raise ValueError("All fields are required")
        if not isinstance(title, str) or len(title) > 100 or not title:
            raise ValueError("Title must be a non-empty string, max 100 characters")
        if not isinstance(price, float) or price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(latitude, float) or latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(longitude, float) or longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        if not isinstance(owner, User): # might need to check all user.
            raise ValueError("Owner must be a valid User instance")

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be a valid Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)