from .BaseModel import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        super().__init__()
        if not isinstance(name, str) or len(name) > 50 or not name:
            raise ValueError("Name must be a non-empty string, max 50 characters")
        self.name = name