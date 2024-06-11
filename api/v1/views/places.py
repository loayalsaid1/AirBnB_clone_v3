#!/usr/bin/python3
"""Check the routes of /users and /users/place

    Accept all of { get, post, put, and delete} on them
"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """This method retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(
    '/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """This method retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """This method deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object using HTTP POST"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_data = request.get_json(silent=True)
    if not place_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in place_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, place_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in place_data:
        abort(400, description="Missing name")

    place = Place(**place_data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route(
    '/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object using HTTP PUT"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_data = request.get_json(silent=True)
    if not place_data:
        abort(400, description="Not a JSON")

    for key, value in place_data.items():
        if key not in [
                'id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
