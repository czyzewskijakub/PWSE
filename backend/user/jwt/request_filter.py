import jwt
from flask import request, abort


def validate(config):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        abort(403, {"error": "Authentication required"})

    token = auth_header.split()[1]
    try:
        jwt.decode(token, config["SECRET_KEY"], algorithms=config["ALGORITHM"])
    except jwt.DecodeError:
        abort(403, {"error": "Token is invalid"})
    except jwt.ExpiredSignatureError:
        abort(401, {"error": "Token has expired"})
