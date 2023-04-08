"""Main app file"""
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from backend import user
from backend.user.jwt.request_filter import validate
from backend.extensions import db


def create_app(config_object="settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_request_filter(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user.views.blueprint)


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_error(error):
        return jsonify(error.description), error.code


def register_request_filter(app):
    @app.before_request
    def filter_specific_routes():
        if request.path == "/users/all":
            validate(app.config)


if __name__ == "__main__":
    main_app = create_app()
    main_app.run(debug=True)
