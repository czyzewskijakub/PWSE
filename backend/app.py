"""Main app file"""
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from backend import user
from backend.user.jwt.request_filter import validate
from backend.extensions import db


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
    app.register_blueprint(blueprint=user.views.blueprint)


def register_error_handlers(app):
    @app.errorhandler(code_or_exception=HTTPException)
    def handle_error(error):
        return jsonify(error.description), error.code


def register_request_filter(app):
    """All routes that require authorization should be placed in here"""
    request_paths = []

    @app.before_request
    def filter_specific_routes():
        if request.path in request_paths:
            validate(config=app.config)


if __name__ == "__main__":
    main_app = create_app()
    main_app.run(debug=True)
