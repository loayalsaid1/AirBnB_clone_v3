#!/usr/bin/python3

from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Create some objects
amenity = Amenity(name="Pool")
city = City(name="San Francisco", state_id="state_1")
place = Place(city_id=city.id, user_id="user_1", name="House")
review = Review(place_id=place.id, user_id="user_1", text="Great place!")
state = State(name="California")
user = User(email="test@example.com", password="password")

# Add objects to storage
storage.new(amenity)
storage.new(city)
storage.new(place)
storage.new(review)
storage.new(state)
storage.new(user)

# Save objects to file
storage.save()

# Print counts before reload
print("Counts before reload:")
print(f"Amenity count: {storage.count(Amenity)}")
print(f"City count: {storage.count(City)}")
print(f"Place count: {storage.count(Place)}")
print(f"Review count: {storage.count(Review)}")
print(f"State count: {storage.count(State)}")
print(f"User count: {storage.count(User)}")
print(f"Total count: {storage.count()}")

# Reload storage from file
storage.reload()

# Print all objects to verify they are loaded correctly
print("\nAll objects after reload:")
for key, obj in storage.all().items():
    print(f"{key}: {obj}")

# Print counts after reload
print("\nCounts after reload:")
print(f"Amenity count: {storage.count(Amenity)}")
print(f"City count: {storage.count(City)}")
print(f"Place count: {storage.count(Place)}")
print(f"Review count: {storage.count(Review)}")
print(f"State count: {storage.count(State)}")
print(f"User count: {storage.count(User)}")
print(f"Total count: {storage.count()}")

