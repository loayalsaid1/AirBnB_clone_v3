#!/usr/bin/python3
"""Handles all API default routes for User objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def get_users():
    """Handles GET and POST requests for User objects"""
    if request.method == "GET":
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])
    else:
        json_payload = request.get_json(silent=True)
        if not json_payload:
            abort(400, description="Not a JSON")

        if "email" not in json_payload:
            abort(400, description="Missing email")

        if "password" not in json_payload:
            abort(400, description="Missing password")

        user = User(**json_payload)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=[
    "GET", "DELETE", "PUT"])
def user_id(user_id):
    """Handles GET, DELETE, and PUT requests for a specific User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:  # PUT request
        json_payload = request.get_json(silent=True)
        if not json_payload:
            abort(400, description="Not a JSON")

        for key in ["id", "email", "created_at", "updated_at"]:
            if key in json_payload:
                del json_payload[key]

        for key, value in json_payload.items():
            setattr(user, key, value)

        user.save()
        return jsonify(user.to_dict()), 200
