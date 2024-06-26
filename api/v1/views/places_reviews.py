#!/usr/bin/python3
"""Handles API for Review objects"""

from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in json_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in json_data:
        abort(400, description="Missing text")

    review = Review(place_id=place_id, **json_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")

    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
