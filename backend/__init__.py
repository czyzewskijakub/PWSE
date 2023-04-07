from flask import Flask, jsonify, request
from backend.authentication.blueprints.auth import auth_bp
from backend.authentication.filters.request_filter import validate
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


def create_app():
    app.register_blueprint(auth_bp)
    return app


# Request filter
# @app.before_request
# def filter_specific_requests():
#     if request.path == "/register":
#         validate()


@app.errorhandler(HTTPException)
def auth_required(error):
    return jsonify(error.description), error.code
