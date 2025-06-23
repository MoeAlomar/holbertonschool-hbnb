from .BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not isinstance(name, str) or len(name) > 50 or not name:
            raise ValueError("Name must be a non-empty string, max 50 characters")
        self.name = name