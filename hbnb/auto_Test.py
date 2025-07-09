import requests
import jwt

BASE_URL = "http://127.0.0.1:5000/api/v1"

def register_user(first_name, last_name, email, password, ad=False):
    print(f"\n🔐 Registering {email}...")
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "is_admin": ad
    }
    res = requests.post(f"{BASE_URL}/users/", json=user_data)
    if res.status_code == 400:
        print("User already exists. Continuing...")
    else:
        res.raise_for_status()
        print("User created:", res.json())
    return res.json().get("id")

def login(email, password):
    print(f"\n🔑 Logging in as {email}...")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    res.raise_for_status()
    token = res.json()["access_token"]
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("Logged in. is_admin:", decoded.get("is_admin", False))
    return token, decoded["sub"]

def create_place(title, description, price, latitude, longitude, owner_id, headers):
    print(f"\n🏠 Creating place: {title}...")
    place_data = {
        "title": title,
        "description": description,
        "price": price,
        "latitude": latitude,
        "longitude": longitude,
        "owner_id": owner_id
    }
    res = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers)
    if res.status_code == 201:
        print("Place created:", res.json())
        return res.json().get("id")
    else:
        print(f"Failed to create place. Status: {res.status_code}, Response: {res.json()}")
        return None

# Register users
admin_email = "admin@example.com"
user1_email = "alice@example.com"
user2_email = "bob@example.com"

admin_id = register_user("Admin", "User", admin_email, "adminpass", True)
user1_id = register_user("Alice", "Smith", user1_email, "alicepass")
user2_id = register_user("Bob", "Jones", user2_email, "bobpass")

# Log in
admin_token, admin_id = login(admin_email, "adminpass")
user1_token, user1_id = login(user1_email, "alicepass")
user2_token, user2_id = login(user2_email, "bobpass")

admin_headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}
user1_headers = {"Authorization": f"Bearer {user1_token}", "Content-Type": "application/json"}
user2_headers = {"Authorization": f"Bearer {user2_token}", "Content-Type": "application/json"}

# Create places owned by different users
user1_place_id = create_place("Alice's Cozy Apartment", "A lovely place in downtown", 100.0, 40.7128, -74.0060, user1_id, user1_headers)
user2_place_id = create_place("Bob's Beach House", "Relaxing beachfront property", 200.0, 25.7617, -80.1918, user2_id, user2_headers)

if user1_place_id and user2_place_id:
    # 🚫 User1 tries to update User2's profile (should fail)
    print("\n🚫 User1 tries to update User2's profile (should fail)...")
    res = requests.put(f"{BASE_URL}/users/{user2_id}", json={
        "first_name": "Hacked",
        "last_name": "User",
        "email": "hacked@example.com",
        "password": "newpass"
    }, headers=user1_headers)
    print("Status:", res.status_code, "Response:", res.json())

    # ✅ User1 updates their own profile
    print("\n✅ User1 updates their own profile...")
    res = requests.put(f"{BASE_URL}/users/{user1_id}", json={
        "first_name": "AliceUpdated",
        "last_name": "SmithUpdated",
        "email": "alice.updated@example.com",
        "password": "alicepass"
    }, headers=user1_headers)
    print("Status:", res.status_code, "Response:", res.json())

    # 🛠️ Admin updates User2's profile
    print("\n🛠️ Admin updates User2's profile...")
    res = requests.put(f"{BASE_URL}/users/{user2_id}", json={
        "first_name": "BobUpdated",
        "last_name": "JonesUpdated",
        "email": "bob.updated@example.com",
        "password": "bobpass"
    }, headers=admin_headers)
    print("Status:", res.status_code, "Response:", res.json())
