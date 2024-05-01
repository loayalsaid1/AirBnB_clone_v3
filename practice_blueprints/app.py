from flask import Flask
from branch.b import b


app = Flask(__name__)
app.register_blueprint(b, url_prefix='/api')

@app.route("/")
@app.route("/home")
def home():
    return "<h1>home</h1>"


if __name__ == "__main__":
    app.run()
