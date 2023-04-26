from flask import Blueprint, jsonify, request, redirect
from .jwt import user_manager
from .google import google_user_manager
from flask_cors import cross_origin

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/login", methods=["POST"])
def login():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]

    res = user_manager.authorize(email=email, password=password)
    return jsonify_response(res)


@user_bp.route("/login/google")
def login_via_facebook():
    authorization_url: str = google_user_manager.google_login()
    return redirect(authorization_url)


@user_bp.route("/callback")
def callback():
    res = google_user_manager.callback_from_google_login()
    return jsonify_response(res)


@user_bp.route("/register", methods=["POST"])
def register():
    req_body = request.get_json()
    name: str = ""
    email: str = req_body["email"]
    password: str = req_body["password"]
    profile_picture_url: str = ""

    if "name" in req_body:
        name = req_body["name"]
    if "profile_picture_url" in req_body:
        profile_picture_url = req_body["profile_picture_url"]

    res = user_manager.register(name=name, email=email, password=password, profile_picture_url=profile_picture_url)

    return jsonify_response(res)


def jsonify_response(response):
    res = jsonify({key: value for key, value in list(response.items())[:-1]}), response["status_code"]
    return res
