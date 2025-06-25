import requests

base_url = "http://localhost:5000/api/v1"
place_url = f"{base_url}/places/"
user_url = f"{base_url}/users/"
amenity_url = f"{base_url}/amenities/"

# 1. Create a user
user_data = {"first_name": "Test", "last_name": "Owner", "email": "test.owner@example.com"}
r = requests.post(user_url, json=user_data)
owner = r.json()
print("Created user:", r.status_code, owner)

# 2. Create amenities
amenities = []
for name in ["Wi-Fi", "Balcony"]:
    r = requests.post(amenity_url, json={"name": name})
    print("Created amenity:", r.status_code, r.json())
    amenities.append(r.json()["id"])

# 3. Create a place
place_data = {
    "title": "Ocean View Apartment",
    "description": "A sunny place by the beach",
    "price": 250.0,
    "latitude": 34.01,
    "longitude": -118.49,
    "owner_id": owner["id"],
    "amenities": amenities
}
r = requests.post(place_url, json=place_data)
place = r.json()
print("Created place:", r.status_code, place)

# 4. Get all places
r = requests.get(place_url)
print("All places:", r.status_code, r.json())

# 5. Update the place
updated_data = {
    "title": "Ocean View Condo",
    "description": "Even sunnier!",
    "price": 300.0,
    "latitude": 34.02,
    "longitude": -118.50,
    "owner_id": owner["id"],
    "amenities": amenities
}
r = requests.put(place_url + place["id"], json=updated_data)
print("Updated place:", r.status_code, r.json())

# 6. Get place by ID
r = requests.get(place_url + place["id"])
print("Place by ID:", r.status_code, r.json())
