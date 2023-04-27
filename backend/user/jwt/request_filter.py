import jwt

from flask import request, abort


def validate(config):
    auth_header = request.headers.get("Authorization")

    token = ""
    if auth_header is not None:
        token = auth_header.split()[1]
    try:
        payload = jwt.decode(jwt=token, key=config["SECRET_KEY"], algorithms=config["ALGORITHM"])
        return payload
    except jwt.ExpiredSignatureError:
        abort(code=401)
    except jwt.InvalidTokenError:
        abort(code=401)
