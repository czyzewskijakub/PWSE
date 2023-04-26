from flask import Blueprint
from use import load_model_and_make_prediction

ai_blueprint = Blueprint("first", __name__, url_prefix="/model")

# X array should be given in the request under /predict.
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]

@ai_blueprint.route("/predict")
def prediction():
    predicted = load_model_and_make_prediction(x, '900000.pt')
    return predicted


@ai_blueprint.route("/statistics")
def print_dataset_statistics():
    return "Dataset statistics will be here"

@ai_blueprint.route("/save")
def save():
    return "Save prediction will be here"

@ai_blueprint.route("/history")
def get_history_prediction() :
    return "Your prediction history will be here"