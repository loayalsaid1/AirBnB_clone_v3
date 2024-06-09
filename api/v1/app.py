#!/usr/bin/python3
"""The core of the api"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close(exception):
	"""Close the session after each request"""
	storage.close()


if __name__ == "__main__":
	from os import getenv
	host = getenv("HBNB_API_HOST", "0.0.0.0")
	port = getenv("HBNB_API_PORT", "5000")

	app.run(host=host, port=port, threaded=True)
