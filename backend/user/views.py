from flask import Blueprint, jsonify, request

from .jwt import user_manager

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login", methods=["POST"])
def login():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.authorize(email, password)

    return jsonify({key: value for key, value in list(res.items())[:-1]}), res["status_code"]


@blueprint.route("/register", methods=["POST"])
def register():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.register(email, password)

    return jsonify({key: value for key, value in list(res.items())[:-1]}), res["status_code"]

