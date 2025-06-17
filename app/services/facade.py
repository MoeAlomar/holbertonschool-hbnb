from app.persistance.repository import InMemoryRepository

class HBnBFacade():
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # This method will be implemented later
        pass

    # Placeholder method to get places by ID
    def get_place(self, place_id):
        # This method will be implemented later
        pass
