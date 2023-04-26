from flask import Blueprint, jsonify, request, redirect
from .jwt import user_manager
from .google import google_user_manager
from flask_cors import cross_origin

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login", methods=["POST"])
def login():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.authorize(email=email, password=password)
    return jsonify_response(res)


@blueprint.route("/login/google")
def login_via_facebook():
    authorization_url: str = google_user_manager.google_login()
    return redirect(authorization_url)


@blueprint.route("/callback")
def callback():
    res = google_user_manager.callback_from_google_login()
    return jsonify_response(res)


@blueprint.route("/register", methods=["POST"])
def register():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.register(email=email, password=password)

    return jsonify_response(res)


def jsonify_response(response):
    res = jsonify({key: value for key, value in list(response.items())[:-1]}), response["status_code"]
    return res
