#!/usr/bin/python3
"""Endpoints to manipulate amenities or places"""

from flask import jsonify, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_place_amentities(place_id):
    """
        Get place amnenities info....

        For db engine return json representation of the object

        For File Storage list the amenties IDs
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage_t == "db":
        amenities = place.amenities

        return jsonify([amenity.to_dict() for amenity in amenities])
    else:
        return jsonify(place.amenity_ids)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """
        Unlink an amenity to a place....
        Using the right approach considering storage engine and
        how each link an amenity to a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)

    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def add_place_amenity(place_id, amenity_id):
    """Add an aminiyt to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
