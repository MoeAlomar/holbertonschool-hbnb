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
    "email": "test.user@example.com",
    "password": "1234"
}
user_res = requests.post(user_url, json=user_data)
print("Create user:", user_res.status_code, user_res.json())
user_id = user_res.json()["id"]
user_get = requests.get(f"{user_url}{user_id}")
print("Get user:", user_get.status_code, user_get.json())

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

# --- Get all reviews ---
all_reviews = requests.get(review_url)
print("All reviews:", all_reviews.status_code, all_reviews.json())

# --- Update review ---
update_data = {
    "text": "Very pleasant stay.",
    "rating": 4,
    "user_id": user_id,
    "place_id": place_id
}
update_res = requests.put(f"{review_url}{review_id}", json=update_data)
print("Update review:", update_res.status_code, update_res.json())

# --- Get review by ID ---
get_res = requests.get(f"{review_url}{review_id}")
print("Get review by ID:", get_res.status_code, get_res.json())

# --- Get reviews for a place ---
place_reviews = requests.get(place_reviews_url(place_id))
print("Reviews for place:", place_reviews.status_code)


# Check that the place is reachable
place_detail = requests.get(f"http://localhost:5000/api/v1/places/{place_id}")
print("Place status:", place_detail.status_code)
print("Place data:", place_detail.text)


# All reviews
all_reviews = requests.get("http://localhost:5000/api/v1/reviews/")
print("All reviews status:", all_reviews.status_code)
print("All reviews:", all_reviews.text)

# Get place full details (should include reviews)
place_info = requests.get(f"http://localhost:5000/api/v1/places/{place_id}")
print("Place info (with reviews):", place_info.text)

# Get reviews by place (should match the above)
place_reviews = requests.get(f"http://localhost:5000/api/v1/places/{place_id}/reviews")
print("Place reviews status:", place_reviews.status_code)
print("Place reviews response:", place_reviews.text)  # Again, use repr to avoid surprises


