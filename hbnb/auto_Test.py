import requests
import jwt

BASE_URL = "http://127.0.0.1:5000/api/v1"

def register_user(first_name, last_name, email, password, is_admin=False):
    print(f"\n🔐 Registering {email}...")
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "is_admin": is_admin
    }
    res = requests.post(f"{BASE_URL}/users/", json=data)
    if res.status_code == 400:
        print("User already exists. Continuing...")
    else:
        res.raise_for_status()
        print("✅ User created:", res.json())
    return res.json().get("id")

def login_user(email, password):
    print(f"\n🔑 Logging in as {email}...")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    res.raise_for_status()
    token = res.json()["access_token"]
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("✅ Logged in. is_admin:", decoded.get("is_admin", False))
    return token, decoded["sub"]

def create_place(token, user_id):
    print("\n🏠 Creating Place...")
    headers = {"Authorization": f"Bearer {token}"}
    place_data = {
        "title": "Test Place",
        "description": "A nice test place",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": user_id
    }
    res = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers)
    res.raise_for_status()
    print("✅ Place created:", res.json())
    return res.json().get("id")

def create_review(token, user_id, place_id):
    print("\n💬 Creating Review...")
    headers = {"Authorization": f"Bearer {token}"}
    review_data = {
        "text": "This place is awesome!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    res = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers)
    res.raise_for_status()
    print("✅ Review created:", res.json())
    return res.json().get("id")

def create_amenity(token, name):
    print("\n🛠️ Creating Amenity...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name}
    res = requests.post(f"{BASE_URL}/amenities/", json=data, headers=headers)
    res.raise_for_status()
    print("✅ Amenity created:", res.json())
    return res.json().get("id")

# === RUN TEST FLOW ===

# Create user
user_email = "tester@example.com"
user_id = register_user("Test", "User", user_email, "testpass")

# Log in
token, user_id = login_user(user_email, "testpass")

# Create Amenity
amenity_id = create_amenity(token, "WiFi")
