from flask import Blueprint, request, jsonify

from .data import stats
from ..ai.use import load_model_and_make_prediction

ai_blueprint = Blueprint("ai", __name__, url_prefix="/ai")


@ai_blueprint.route("/predict", methods=['POST'])
def prediction():
    req_body = request.get_json()
    response = load_model_and_make_prediction(req_body, '900000.pt')

    if "error" in response:
        return jsonify({"error": response["error"]}), response["status_code"]
    return jsonify({"result": response["result"][0]}), response["status_code"]


@ai_blueprint.route("/statistics")
def print_dataset_statistics():
    return stats.load_data()


@ai_blueprint.route("/save")
def save():
    return "Save prediction will be here"


@ai_blueprint.route("/history")
def get_history_prediction():
    return "Your prediction history will be here"

