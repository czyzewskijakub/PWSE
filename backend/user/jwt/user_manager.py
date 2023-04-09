import re

import backend.settings as config
import datetime
import jwt

from backend.user.models import User


def authorize(email, password):
    user = User.find_by_email(email)
    if user.check_password(password):
        token = jwt.encode({"user": email,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=config.EXP_TIME_MIN)},
                           config.SECRET_KEY, algorithm=config.ALGORITHM)
        return {
            "message": "Successfully logged in",
            "token": token,
            "status_code": 202
        }

    return {"error": "Could not log in", "status_code": 401}


def register(email, password):
    if User.find_by_email(email) is not None:
        return {"error": "Email is taken", "status_code": 409}

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Incorrect email", "status_code": 409}

    user = User(email, password)
    user.save()
    return {"message": "Successfully created user", "status_code": 201}


