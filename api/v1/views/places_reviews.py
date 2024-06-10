#!/usr/bin/python3
"""Handles all API default routes for Review objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route(
    '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object from"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object using HTTP POST"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review_data = request.get_json(silent=True)
    if not review_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, review_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in review_data:
        abort(400, description="Missing text")

    review = Review(**review_data)
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object using HTTP PUT"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_data = request.get_json(silent=True)
    if not review_data:
        abort(400, description="Not a JSON")

    for key, value in review_data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
