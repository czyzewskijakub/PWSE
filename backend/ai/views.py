from flask import Blueprint

ai_blueprint = Blueprint("first", __name__, url_prefix="/model")

@ai_blueprint.route("/predict")
def prediction():
    return "Prediction will be here"


@ai_blueprint.route("/statistics")
def print_dataset_statistics():
    return "Dataset statistics will be here"

@ai_blueprint.route("/save")
def save():
    return "Save prediction will be here"

@ai_blueprint.route("/history")
def get_history_prediction() :
    return "Your prediction history will be here"