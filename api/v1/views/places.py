#!/usr/bin/python3
"""Handles all API default routes for Place objects"""

from flask import Flask, jsonify, abort, request
from flask import make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """This method retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """This method retrieves a Place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """This method deletes a Place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    my_place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object using HTTP POST"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)

    city_json = request.get_json(silent=True)
    if not city_json:
        abort(400, description="Not a JSON")
    if 'user_id' not in city_json.keys():
        abort(400, description="Missing user_id")
    my_user = storage.get(User, city_json['user_id'])
    if my_user is None:
        abort(404)
    if 'name' not in city_json.keys():
        abort(400, description="Missing name")
    new_place = Place(**city_json)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object using HTTP PUT"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    place_json = request.get_json(silent=True)
    if not place_json:
        abort(400, description="Not a JSON")
    for key, value in place_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(my_place, key, value)
    storage.save()
    return jsonify(my_place.to_dict())
