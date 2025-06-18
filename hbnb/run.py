from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity

# User test
user = User("ff", "Doe", "janeexample.com","12346")
print("✅ User created:", user.__dict__)

user = User("john", "D1e", "jane@example.com","12346")
print("✅ User created:", user.__dict__)

# Place test
place = Place("Nice Apartment", "Near downtown", 150.0, 40.7, 32, user)
print("✅ Place created:", place.__dict__)

# Review test
review = Review("Amazing stay!", 5, place, user)
place.add_review(review)
print("✅ Review added to place:", place.reviews[0].__dict__)

# Amenity test
wifi = Amenity("Wi-Fi")
place.add_amenity(wifi)
print("✅ Amenity added to place:", place.amenities[0].__dict__)
