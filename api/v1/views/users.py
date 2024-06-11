#!/usr/bin/python3
"""Check the routes of /users and /users/<user_id>

    Accept all of { get, post, put, and delete} on them    
"""
from flask import request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify


@app_views.route("/users", strict_slashes=False,
                 methods=["GET", "POST"])
def get_users():
    """Get users"""
    if request.method == "GET":
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])
    else:
        if not (json_payload := request.get_json()):
            abort(400, description="Not a JSON")

        if "email" not in json_payload:
            abort(400, description="Missing email")

        if "password" not in json_payload:
            abort(400, description="Missing password")

        user = User(**json_payload)
        user.save()

        return jsonify(user.to_dict()), 202


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def user_id(user_id):
    """Affect specific user"""
    if not (user := storage.get(User, user_id)):
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        if not (json_payload := request.get_json()):
            abort(400, description="Not a JSON")
        for key in ["id", "email", "created_at", "updated_at"]:
            if key in json_payload:
                del json_payload[key]

        for key, value in json_payload.items():
            setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict())
