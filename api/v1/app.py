#!/usr/bin/python3
"""The core of the api"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(exception):
    """Close the session after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors by returning a JSON-formatted response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)

    app.run(host=host, port=port, threaded=True)
