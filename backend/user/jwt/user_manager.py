import backend.settings as config
import datetime
import jwt
import re

from backend.database.user import User


def authorize(email, password):
    user = User.find_by_email(email=email)

    if user is not None and user.check_password(password=password):
        token = generate_token(email=email)
        return {
            "message": "Successfully logged in",
            "token": token,
            "status_code": 202
        }

    return {"error": "Could not log in", "status_code": 401}


def register(name: str, email, password, profile_picture_url):
    if User.find_by_email(email=email) is not None:
        return {"error": "Email is taken", "status_code": 409}
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Incorrect email", "status_code": 409}
    elif name is None or len(name) == 0:
        return {"error": "User name has to be provided", "status_code": 409}
    elif password is None or not sufficient_password(password=password):
        return {"error": "Password is not sufficient", "status_code": 403}

    user = User(name=name, email=email, profile_picture_url=profile_picture_url, account_source="FlickTrendz")
    user.set_password(password)

    user.save()
    return {"message": "Successfully created user", "status_code": 201}


def register_google_account(name, email, profile_picture_url):
    if User.find_by_email(email=email) is None:
        user = User(name=name, email=email, profile_picture_url=profile_picture_url, account_source="Google")
        user.save()
    token = generate_token(email=email)
    return {
            "message": "Successfully logged in",
            "token": token,
            "status_code": 202
        }


def generate_token(email):
    return jwt.encode(payload={"user": email,
                               "exp": datetime.datetime.utcnow() + datetime.timedelta(
                                   config.EXP_TIME_MIN)},
                      key=config.SECRET_KEY, algorithm=config.ALGORITHM)

def get_user_data(email):
    user = User.find_by_email(email=email)
    if user is None:
        return {"error": "User was no found", "status_code": 404}
    return {"user": user.to_dict(), "status_code": 200}


def sufficient_password(password: str):
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password)\
            or not re.search(r'[!@#$%^&*()\-=_+[\]{};:\'"<>?,./|\\]', password):
        return False
    return True
