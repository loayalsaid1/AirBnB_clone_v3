#!/usr/bin/python3
"""Handles API for State objects"""

from flask import Flask, jsonify, abort, request
from flask import make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Method to retrieve the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Method to retrieve a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Method to delete a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Method to create a State object"""
    # try:
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")

    if 'name' not in json_data.keys():
        abort(400, description="Missing name")

    state = State(**json_data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)

    # except Exception:
    #     abort(500, description="Internal server error")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Method to update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
