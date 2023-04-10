from flask import Blueprint, jsonify, request

from .jwt import user_manager

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login", methods=["POST"])
def login():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.authorize(email=email, password=password)

    return jsonify_response(res)


@blueprint.route("/register", methods=["POST"])
def register():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.register(email=email, password=password)

    return jsonify_response(res)


def jsonify_response(response):
    return jsonify({key: value for key, value in list(response.items())[:-1]}), response["status_code"]
