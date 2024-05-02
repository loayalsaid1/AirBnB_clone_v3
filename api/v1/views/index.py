#!/usr/bin/python3
"""Views.index"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": 47,
    "cities": 36,
    "places": 154,
    "reviews": 718,
    "states": 27,
    "users": 31
}


@app_views.route("/status")
def status():
    """Status of the API"""
    return jsonify({"status": "OK"})
