#!/usr/bin/python3
"""Cities views"""
from flask import request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET", "POST"])
def state_cities(state_id):
    """Get or add a cities of a specific state"""
    if not (state := storage.get(State, state_id)):
        abort(404)

    print(state.to_dict())
    if request.method == "GET":
        cities = state.cities
        dict_cities = [city.to_dict() for city in cities]

        return jsonify(dict_cities)
    else:
        if not (json_payload := request.get_json()):
            abort(400, description="Not a JSON")

        if "name" not in json_payload:
            abort(400, description="Missing name")

        city = City(**json_payload)
        setattr(city, 'state_id', state_id)
        city.save()

        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def cities(city_id):
    """Get, Delete, Modify a city object"""
    if not (city := storage.get(City, city_id)):
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict()), 200
    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()

        return jsonify({}), 200
    else:
        if not (json_payload := request.get_json()):
            abort(400, description="Not a JSON")

        if "name" not in json_payload:
            abort(400, description="Missing name")

        for key in ["id", "state_id", "created_at", "updated_at"]:
            if key in json_payload:
                del json_payload[key]

        for key, value in json_payload.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
