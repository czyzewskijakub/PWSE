import jwt
from flask import request, abort


def validate(config):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        abort(code=401, args={"error": "Authentication required"})

    token = auth_header.split()[1]
    try:
        jwt.decode(jwt=token, key=config["SECRET_KEY"], algorithms=config["ALGORITHM"])
    except jwt.InvalidTokenError:
        abort(code=401, args={"error": "Token is invalid"})
