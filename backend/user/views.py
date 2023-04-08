from flask import Blueprint, jsonify, request

from .jwt import user_manager
from backend.user.models import User

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login", methods=["POST"])
def login():
    req_body = request.get_json()
    email = req_body["email"]
    password = req_body["password"]
    return user_manager.authorize(email, password)


@blueprint.route("/register", methods=["POST"])
def register():
    req_body = request.get_json()
    email = req_body["email"]
    password = req_body["password"]

    return jsonify(user_manager.register(email, password))


@blueprint.route("/<int:user_id>", methods=["GET"])
def get_by_id(user_id):
    user: User = User.get_by_id(user_id)
    return jsonify({"id": user.id, "email": user.email})


@blueprint.route("/all")
def get_all():
    users: list = User.find_all()
    return jsonify([{"id": user.id, "email": user.email} for user in users])
