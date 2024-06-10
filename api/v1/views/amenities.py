#!/usr/bin/python3
"""Module that defines API routes for Amenities objects"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
