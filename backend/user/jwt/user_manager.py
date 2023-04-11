import backend.settings as config
import datetime
import jwt
import re

from backend.user.models import User


def authorize(email, password):
    user = User.find_by_email(email=email)

    if user is not None and user.check_password(password=password):
        token = jwt.encode(payload={"user": email,
                                    "exp": datetime.datetime.utcnow() + datetime.timedelta(
                                        config.EXP_TIME_MIN)},
                           key=config.SECRET_KEY, algorithm=config.ALGORITHM)
        return {
            "message": "Successfully logged in",
            "token": token,
            "status_code": 202
        }

    return {"error": "Could not log in", "status_code": 401}


def register(email, password):
    if User.find_by_email(email=email) is not None:
        return {"error": "Email is taken", "status_code": 409}

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Incorrect email", "status_code": 409}

    user = User(email=email, password=password)
    user.save()
    return {"message": "Successfully created user", "status_code": 201}
