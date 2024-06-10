#!/usr/bin/python3
"""Initiate the views"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
<<<<<<< HEAD
=======
from api.v1.views.amenities import *
>>>>>>> 6fe33a8 (Created aemnities.py to handle routes for the Amenity objects)
