import requests

base_url = "http://127.0.0.1:5000/api/v1/users/"
amenity_url = "http://127.0.0.1:5000/api/v1/amenities/"
places_url = "http://127.0.0.1:5000/api/v1/places/"
"""
# Add two users
users = [
    {"first_name": "Alice", "last_name": "Smith", "email": "alice.smith@example.com"},
    {"first_name": "Bob", "last_name": "Jones", "email": "alice.smith@exmample.com"}
]

for user in users:
    r = requests.post(base_url, json=user)
    print("POST:", r.status_code, r.json())

# Get all users
r = requests.get(base_url)
print("\nGET All Users:", r.status_code)
users = r.json()
print(users)

# Update the second user
if len(users) > 1:
    user_id = users[1]["id"]
    update = {"first_name": "Bobby", "last_name": "Johnson", "email": "bobby.j@example.com"}
    r = requests.put(base_url + user_id, json=update)
    print("\nPUT:", r.status_code, r.json())

amenities = [ {'name': "Wi-fi"},
            {'name': "Chair"},
            {'name': "TV"}
            ]
for amenity in amenities:
    e = requests.post(amenity_url, json=amenity)
    print("Post: ", e.status_code, e.json())
r = requests.get(amenity_url)
print("Get all amenities: ", r.status_code, r.json())
amenities = r.json()
amenity_id = amenities[0]["id"]
r = requests.put(amenity_url + amenity_id, json={"name": "Bed"})
"""


# Add two users
users = [
    {"first_name": "Alice", "last_name": "Smith", "email": "alice.smith@example.com"},
    {"first_name": "Bob", "last_name": "Jones", "email": "alice.smith@exmample.com"}
]

for user in users:
    r = requests.post(base_url, json=user)
    print("POST:", r.status_code, r.json())

# Get all users
r = requests.get(base_url)
print("\nGET All Users:", r.status_code)
users = r.json()
print(users)
user_id = users[0]["id"]


# Create amenities
r = requests.post(amenity_url, json={"name": "Wi-Fi"})
print("POST:", r.status_code, r.json())

r = requests.post(amenity_url, json={"name": "Couch"})
print("POST:", r.status_code, r.json())

# Get all amenities and store the response
amenities_response = requests.get(amenity_url)
amenities_data = amenities_response.json()
print("GET amenities:", amenities_response.status_code, amenities_data)
place = {
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": user_id,
  "amenities": []
}
# Now use the stored amenities data
e = requests.post(places_url, json=place)
print("Response status:", e.status_code)
print("Response text:", e.text)
print("POST place:", e.json())