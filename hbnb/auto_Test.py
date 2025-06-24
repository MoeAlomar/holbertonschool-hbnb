import requests

base_url = "http://127.0.0.1:5000/api/v1/users/"
amenity_url = "http://127.0.0.1:5000/api/v1/amenities/"

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

