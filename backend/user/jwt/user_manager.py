import bcrypt as bcrypt

import backend.settings as config
import datetime
import jwt

from flask import jsonify

from backend.user.models import User


def authorize(email, password):

    if password == "password":
        token = jwt.encode({'user': email,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config.EXP_TIME_MIN)},
                           config.SECRET_KEY, algorithm=config.ALGORITHM)
        res = {
            "message": "Successfully logged in",
            "token": token
        }
        return jsonify(res), 200

    res = {"message": "Could not log in"}
    return jsonify(res), 401


def register(email, password):
    if User.query.filter_by(email=email).first() is not None:
        return "TAKEN"

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = User(email, password_hash)
    user.save()
    return "success"
