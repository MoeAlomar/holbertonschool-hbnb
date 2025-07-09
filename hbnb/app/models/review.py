from .BaseModel import BaseModel
from .place import Place
from .user import User
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    #Relationship
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    def __init__(self, text, rating, place, user):
        super().__init__()

        self.validate_Review(text, rating, place, user)

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def validate_Review(self, text, rating, place, user):
        if not text or not rating or not place or not user: # case of an empty field.
            raise ValueError("All field are Required!")
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        if not isinstance(place, Place): # check from the database it self (Repo)
            raise ValueError("Place must be a valid Place instance")
        if not isinstance(user, User): # check from the database it self (Repo)
            raise ValueError("User must be a valid User instance")