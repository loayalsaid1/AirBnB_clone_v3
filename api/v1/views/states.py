#!/usr/bin/python3
"""Endpoints for the states view"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states")
def get_states():
    """Gets states objects"""
    objects = storage.all(State).values()
    objects = [obj.to_dict() for obj in objects]

    return jsonify(objects)


@app_views.route("/states/<id>")
def get_state(id):
    """Get specific state object"""
    state = storage.get(State, id)

    if not object:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states/<id>")
def delete_state(id):
    """deletes a state object"""
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        return {}, 200
    else:
        abort(404)


@app_views.route("/states/<id>", methods=["POST"])
def create_state(id):
    """create a state"""
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if not data['name']:
        abort(400, description="Missing name")

    state = State(name=data['name'])
    state.save()

    return jsonify(state.to_dict()), 201
