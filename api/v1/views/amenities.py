#!/usr/bin/python3
"""Handles API for Amenity objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Method to retrieve the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Method to retrieve an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Method to delete an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Method to create an Amenity object"""
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")

    if 'name' not in json_data:
        abort(400, description="Missing name")

    amenity = Amenity(**json_data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Method to update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
