import unittest
from app import create_app

class TestHBnBEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_create_user_valid(self):
        """Test creating a valid user"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "Jane")

    def test_create_user_invalid(self):
        """Test creating a user with invalid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_place_valid(self):
        """Test creating a valid place"""
        # First create a user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        user_id = user_response.get_json()['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cabin",
            "description": "Nice cabin",
            "price": 99.99,
            "latitude": 37.77,
            "longitude": -122.41,
            "owner_id": user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], "Cozy Cabin")

    def test_create_place_invalid(self):
        """Test creating a place with invalid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "Invalid",
            "price": -10,
            "latitude": 100,
            "longitude": -200,
            "owner_id": "invalid-id",
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_review_valid(self):
        """Test creating a valid review"""
        # Create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        user_id = user_response.get_json()['id']

        # Create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cabin",
            "description": "Nice cabin",
            "price": 99.99,
            "latitude": 37.77,
            "longitude": -122.41,
            "owner_id": user_id,
            "amenities": []
        })
        place_id = place_response.get_json()['id']

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], "Great stay!")

    def test_create_review_invalid(self):
        """Test creating a review with invalid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,
            "user_id": "invalid-id",
            "place_id": "invalid-id"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_place_reviews(self):
        """Test retrieving reviews for a place"""
        # Create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        user_id = user_response.get_json()['id']

        # Create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cabin",
            "description": "Nice cabin",
            "price": 99.99,
            "latitude": 37.77,
            "longitude": -122.41,
            "owner_id": user_id,
            "amenities": []
        })
        place_id = place_response.get_json()['id']

        # Create review
        self.client.post('/api/v1/reviews/', json={
            "text": "Great stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })

        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['text'], "Great stay!")

    def test_get_non_existent_place_reviews(self):
        """Test retrieving reviews for a non-existent place"""
        response = self.client.get('/api/v1/places/invalid-id/reviews')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
