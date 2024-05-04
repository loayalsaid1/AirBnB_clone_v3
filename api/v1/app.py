#!/usr/bin/python3
"""Main app file for the api"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found_handler(error):
    """Handle 404 error"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_session(error):
    """Close session after each request"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")

    app.run(debug=True, host=host, port=port, threaded=True)
