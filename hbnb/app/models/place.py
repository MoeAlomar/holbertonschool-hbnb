from .BaseModel import BaseModel
from .user import User
from .amenity import  Amenity
from app.extensions import db, bcrypt
from app.models.place_amenity import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='places', lazy=True)

    # Relationships
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                backref=db.backref('places', lazy=True), lazy='subquery')


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