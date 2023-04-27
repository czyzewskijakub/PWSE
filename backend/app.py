"""Main app file"""
import json
import os

from flask import Flask, make_response, jsonify, request
from werkzeug.exceptions import HTTPException
from backend.user.jwt.request_filter import validate
from backend.extensions import db
from flask_cors import CORS

from backend import user
from backend.ai import views

def create_app(config_object="settings"):
    app = Flask(import_name=__name__)
    app.config.from_object(obj=config_object)
    register_extensions(app=app)
    register_blueprints(app=app)
    register_error_handlers(app=app)
    set_headers(app=app)
    return app


def register_extensions(app):
    db.init_app(app=app)


def register_blueprints(app):
    app.register_blueprint(blueprint=user.views.user_bp)
    app.register_blueprint(blueprint=views.ai_blueprint)


def register_error_handlers(app):
    @app.errorhandler(code_or_exception=HTTPException)
    def handle_error(error):
        return jsonify(error.description), error.code

    @app.errorhandler(code_or_exception=401)
    def unauthorized(error):
        return json.dumps({"message": "Unauthorized"}), \
            401, {'Content-Type': 'application/json; charset=utf-8'}



def set_headers(app):
    @app.after_request
    def after_request_func(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods','GET, POST, OPTIONS, PUT, PATCH, DELETE')
        response.headers.add('Access-Control-Allow-Origin', "*")

        return response


if __name__ == "__main__":
    main_app = create_app()
    cors = CORS(main_app, resource={r"/*":{"origins":"*"}})
    main_app.config["CORS_HEADERS"] = "Content-Type"
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = main_app.config["OAUTHLIB_INSECURE_TRANSPORT"]
    main_app.run(debug=True)
