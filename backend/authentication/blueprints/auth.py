from flask import Blueprint, request, make_response, jsonify
import jwt
import datetime

from ..config import Config

auth_bp = Blueprint("authentication", __name__)


@auth_bp.route("/login", methods=['POST'])
def login():
    req_body = request.get_json()
    username = req_body["username"]
    password = req_body["password"]

    if password == "password":
        token = jwt.encode({'user': username,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.EXP_TIME_MIN)},
                           Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        res = {
            "message": "Successfully logged in",
            "token": token
        }
        return make_response(jsonify(res), 200)

    res = {"message": "Could not log in"}
    return make_response(jsonify(res), 401)


@auth_bp.route('/register', methods=["POST"])
def register():
    return "registration"
