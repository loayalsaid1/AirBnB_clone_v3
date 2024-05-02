#!/usr/bin/python3
"""Endpoints for the states view"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort


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
        return jsonify(state)


