from flask import Blueprint, jsonify, request, redirect
from .jwt import user_manager, request_filter
from .google import google_user_manager
from backend import settings
from .user_history import history_manager

user_bp = Blueprint("user", __name__, url_prefix="/users")
config = {
        "ALGORITHM": settings.ALGORITHM,
        "SECRET_KEY": settings.SECRET_KEY
    }

@user_bp.route("/login", methods=["POST"])
def login():
    req_body = request.get_json()
    email: str = req_body["email"]
    password: str = req_body["password"]
    res = user_manager.authorize(email=email, password=password)
    return jsonify_response(res)

@user_bp.route("/authorize", methods=["POST"])
def authorize():
    response = request_filter.validate(config)
    return jsonify(response)


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


@user_bp.route("/history/save", methods=["POST"])
def save():
    req_body = request.get_json()
    response = history_manager.save_history(req_body=req_body)
    return jsonify_response(response)

@user_bp.route("/history/get", methods=["GET"])
def get_history_prediction():
    user_id = request.args.get('user_id')
    response = history_manager.read_history(user_id)
    return jsonify_response(response)

@user_bp.route("/profile", methods=["POST"])
def get_user_data():
    response = request_filter.validate(config)
    email = response["user"]
    user = user_manager.get_user_data(email)
    return jsonify_response(user)


def jsonify_response(response):
    res = jsonify({key: value for key, value in list(response.items())[:-1]}), response["status_code"]
    return res
