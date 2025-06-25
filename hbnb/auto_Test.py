import requests

BASE_URL = "http://localhost:5000/api/v1"
user_url = f"{BASE_URL}/users/"
place_url = f"{BASE_URL}/places/"
review_url = f"{BASE_URL}/reviews/"
place_reviews_url = lambda pid: f"{BASE_URL}/places/{pid}/reviews/"

# --- Create a test user ---
user_data = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test.user@example.com"
}
user_res = requests.post(user_url, json=user_data)
print("Create user:", user_res.status_code, user_res.json())
user_id = user_res.json()["id"]

# --- Create a test place ---
place_data = {
    "title": "Test House",
    "description": "Nice for testing",
    "price": 99.99,
    "latitude": 37.77,
    "longitude": -122.41,
    "owner_id": user_id,
    "amenities": []
}
place_res = requests.post(place_url, json=place_data)
print("Create place:", place_res.status_code, place_res.json())
place_id = place_res.json()["id"]

# --- Create a review ---
review_data = {
    "text": "Lovely stay!",
    "rating": 5,
    "user_id": user_id,
    "place_id": place_id
}
review_res = requests.post(review_url, json=review_data)
print("Create review:", review_res.status_code, review_res.json())
review_id = review_res.json()["id"]

