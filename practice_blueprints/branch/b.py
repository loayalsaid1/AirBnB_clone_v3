from flask import Blueprint


b = Blueprint("b", __name__)

@b.route('/')
def b_home():
    return "branch"

