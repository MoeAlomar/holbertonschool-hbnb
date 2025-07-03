import requests
import jwt

BASE_URL = "http://127.0.0.1:5000/api/v1"

# Step 1: Register a user
print("🔐 Registering user...")
user_data = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "password": "securepassword"
}
res = requests.post(f"{BASE_URL}/users/", json=user_data)
if res.status_code == 400 and "already registered" in res.text:
    print("User already exists. Continuing...")
else:
    res.raise_for_status()
    print("User created:", res.json())

user_id = res.json().get("id")

# Step 2: Log in and get token
print("\n🔐 Logging in to get token...")
login_data = {
    "email": user_data["email"],
    "password": user_data["password"]
}
res = requests.post(f"{BASE_URL}/auth/login", json=login_data)
res.raise_for_status()
token = res.json()["access_token"]
print("Token:", token)

# Optional: Decode token to confirm structure (not required)
decoded = jwt.decode(token, options={"verify_signature": False})
print("Decoded Token:", decoded)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Step 3: Create a place
print("\n🏠 Creating a place...")
place_data = {
    "title": "Test Apartment",
    "description": "A great test place",
    "price": 120.0,
    "latitude": 12.34,
    "longitude": 56.78,
    "owner_id": user_id,  # normally injected in backend, but needed here due to the input model
    "amenities": []
}
res = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers)
res.raise_for_status()
place = res.json()
print("Place created:", place)
place_id = place["id"]

# Step 4: List places (public endpoint)
print("\n🌍 Getting list of places (public)...")
res = requests.get(f"{BASE_URL}/places/")
res.raise_for_status()
print("Places:", res.json())

# Step 5: Create a review (user can't review own place → expect failure)
print("\n💬 Trying to review own place (should fail)...")
review_data = {
    "text": "Awesome place!",
    "rating": 5,
    "user_id": user_id,
    "place_id": place_id
}
res = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers)
if res.status_code == 400:
    print("✅ Expected failure:", res.json())
else:
    print("⚠️ Unexpected result:", res.status_code, res.text)

# Step 6: Simulate a second user to review the place properly
print("\n👥 Registering second user to review the place...")
second_user = {
    "first_name": "Reviewer",
    "last_name": "Two",
    "email": "reviewer2@example.com",
    "password": "anotherpassword"
}
res = requests.post(f"{BASE_URL}/users/", json=second_user)
if res.status_code == 400:
    print("Second user already exists.")
res = requests.post(f"{BASE_URL}/auth/login", json={
    "email": second_user["email"],
    "password": second_user["password"]
})
res.raise_for_status()
second_token = res.json()["access_token"]
second_headers = {
    "Authorization": f"Bearer {second_token}",
    "Content-Type": "application/json"
}

# Step 7: Second user creates review
print("\n💬 Second user creating review...")
res = requests.post(f"{BASE_URL}/reviews/", json={
    "text": "Lovely place!",
    "rating": 4,
    "user_id": jwt.decode(second_token, options={"verify_signature": False})["sub"],
    "place_id": place_id
}, headers=second_headers)
res.raise_for_status()
print("Review created:", res.json())
review_id = res.json()["id"]

# Step 8: Try updating the review as second user
print("\n✏️ Updating review as second user...")
res = requests.put(f"{BASE_URL}/reviews/{review_id}", json={
    "text": "Actually, not bad",
    "rating": 4,
    "user_id": jwt.decode(second_token, options={"verify_signature": False})["sub"],
    "place_id": place_id
}, headers=second_headers)
res.raise_for_status()
print(res.json())

# Step 9: Try deleting the review as second user
print("\n🗑️ Deleting review as second user...")
res = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=second_headers)
res.raise_for_status()
print(res.json())

# Step 10: Try unauthorized access (no token)
print("\n🚫 Trying protected endpoint without token...")
res = requests.get(f"{BASE_URL}/users/{user_id}")
if res.status_code == 401:
    print("✅ Unauthorized access correctly blocked:", res.json())
else:
    print("⚠️ Unexpected behavior:", res.status_code, res.text)
