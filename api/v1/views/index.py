#!/usr/bin/python3
"""Views.index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Status of the API"""
    return jsonify({"status": "OK"})
