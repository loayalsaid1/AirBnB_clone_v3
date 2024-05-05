#!/usr/bin/python3
"""Endpoints for the states view"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False)
def get_states():
    """Gets states objects"""
    objects = storage.all(State).values()
    objects = [obj.to_dict() for obj in objects]

    return jsonify(objects)


@app_views.route("/states/<id>")
def get_state(id):
    """Get specific state object"""
    state = storage.get(State, id)

    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states/<id>", methods=["DELETE"])
def delete_state(id):
    """deletes a state object"""
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        storage.save()

        return {}, 200
    else:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """create a state"""
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if not data.get('name'):
        abort(400, description="Missing name")

    state = State(name=data['name'])
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<id>", methods=["PUT"])
def modify_state(id):
    """Modify a state object"""
    # Get the object
    state = storage.get(State, id)
    if not state:
        abort(404)
    # Get the items to change
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    attributes = request.get_json()
    # Filter it first
    ignored_attrs = ["id", "created_at", "updated_at"]
    for attr in ignored_attrs:
        attributes.pop(attr, None)
    # Apply changes
    for key, value in attributes.items():
        setattr(state, key, value)
    state.save()
    # Return
    return state.to_dict(), 200
