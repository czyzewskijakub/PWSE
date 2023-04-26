from flask import Blueprint, json, request

from use import load_model_and_make_prediction

ai_blueprint = Blueprint("first", __name__, url_prefix="/model")


@ai_blueprint.route("/predict", methods=['POST'])
def prediction():
    x = json.loads(request.data).values()
    if len(x) != 11:
        raise ValueError(f'Input array should contain 11 elements. Provided ${len(x)}')
    predicted = load_model_and_make_prediction(x, '900000.pt')
    return predicted


@ai_blueprint.route("/statistics")
def print_dataset_statistics():
    return "Dataset statistics will be here"


@ai_blueprint.route("/save")
def save():
    return "Save prediction will be here"


@ai_blueprint.route("/history")
def get_history_prediction():
    return "Your prediction history will be here"
