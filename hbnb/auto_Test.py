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
        print("⚠️ User already exists. Continuing...")
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

def create_review(token, place_id):
    print("💬 Creating Review...")
    url = f"{BASE_URL}/reviews/"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        "text": "Amazing experience!",
        "rating": 5,
        "place_id": place_id
    }

    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 201:
        review = res.json()
        print("✅ Review created:", review)
        return review["id"]
    else:
        try:
            print("❌ Failed to create review:", res.status_code, res.json())
        except Exception:
            print("❌ Failed to create review:", res.status_code, res.text)
        res.raise_for_status()


def create_amenity(token, name):
    print(f"\n🛠️ Creating Amenity: {name}...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    res = requests.post(f"{BASE_URL}/amenities/", json={"name": name}, headers=headers)

    if res.status_code == 201:
        print("✅ Amenity created:", res.json())
        return res.json().get("id")
    elif res.status_code == 400 and "already exists" in res.text:
        print("⚠️ Amenity already exists. Skipping creation.")
        all_res = requests.get(f"{BASE_URL}/amenities/", headers=headers)
        if all_res.status_code == 200:
            for a in all_res.json():
                if a["name"] == name:
                    print("ℹ️ Found existing amenity ID:", a["id"])
                    return a["id"]
        return None
    else:
        print("❌ Failed to create amenity:", res.status_code, res.text)
        return None

def link_amenity_to_place(token, place_id, amenity_id):
    print(f"\n🔗 Linking Amenity {amenity_id} to Place {place_id}...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    res = requests.post(f"{BASE_URL}/places/{place_id}/amenities", json={"amenity_id": amenity_id}, headers=headers)
    if res.status_code == 200:
        print("✅ Amenity linked to place.")
    else:
        print("❌ Failed to link amenity:", res.status_code, res.json())

# === RUN TEST FLOW ===

# Register and log in
email = "tester@example.com"
user_id = register_user("Test", "User", email, "testpass")
token, user_id = login_user(email, "testpass")

# Create Place
place_id = create_place(token, user_id)

# Create Amenity and link it to Place
amenity_id = create_amenity(token, "WiFi")
if amenity_id:
    link_amenity_to_place(token, place_id, amenity_id)

# Create Review for the Place by the User
# Register second user
email2 = "other@example.com"
password2 = "testpass"
print(f"\n🔐 Registering {email2}...")
try:
    user2_id = register_user("Other", "User", email2, password2)
except requests.exceptions.HTTPError as e:
    print("⚠️ User already exists. Continuing...")

# Login as second user
print(f"\n🔑 Logging in as {email2}...")
token2, is_admin2 = login_user(email2, password2)

# Review the same place as second user
review_id = create_review(token2, place_id)