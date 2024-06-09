#!/usr/bin/python3
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Endpoint that retrieves the number of each objects by type"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    stats = {key: storage.count(cls) for key, cls in classes.items()}
    return jsonify(stats)
