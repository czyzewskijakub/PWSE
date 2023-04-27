"""Main app file"""
import json
import os

from flask import Flask, make_response, jsonify, request
from werkzeug.exceptions import HTTPException
from backend.user.jwt.request_filter import validate
from backend.extensions import db
from flask_cors import CORS

from backend import user
from backend import ai

def create_app(config_object="settings"):
    app = Flask(import_name=__name__)
    app.config.from_object(obj=config_object)
    register_extensions(app=app)
    register_blueprints(app=app)
    register_error_handlers(app=app)
    register_request_filter(app=app)
    return app


def register_extensions(app):
    db.init_app(app=app)


def register_blueprints(app):
    app.register_blueprint(blueprint=user.views.user_bp)
    app.register_blueprint(blueprint=ai.views.ai_blueprint)


def register_error_handlers(app):
    @app.errorhandler(code_or_exception=HTTPException)
    def handle_error(error):
        return jsonify(error.description), error.code

    @app.errorhandler(code_or_exception=401)
    def unauthorized(error):
        return json.dumps({"message": "Unauthorized"}), \
            401, {'Content-Type': 'application/json; charset=utf-8'}



def register_request_filter(app):
    """All routes that require authorization should be placed in here"""
    request_paths = ["/ai/predict"]
    @app.before_request
    def filter_specific_routes():
        if request.path in request_paths:
            validate(config=app.config)

    @app.after_request
    def after_request_func(response):
        origin = request.headers.get('Origin')
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
            response.headers.add('Access-Control-Allow-Methods',
                                'GET, POST, OPTIONS, PUT, PATCH, DELETE')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)

        return response


if __name__ == "__main__":
    main_app = create_app()
    cors = CORS(main_app, resource={r"/*":{"origins":"*"}})
    main_app.config["CORS_HEADERS"] = "Content-Type"
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = main_app.config["OAUTHLIB_INSECURE_TRANSPORT"]
    main_app.run(debug=True)
