from flask import Blueprint, request, jsonify

from .data import stats
from ..ai.use import test
from ..stats.StatCalculator import StatCalculator

ai_blueprint = Blueprint("ai", __name__, url_prefix="/ai")
stat_calc = StatCalculator()


@ai_blueprint.route("/predict", methods=['POST'])
def prediction():
    req_body = request.get_json()
    response = test(req_body)
    if "error" in response:
        return jsonify({"error": response["error"]}), response["status_code"]
    return jsonify({"views": response["views"]}), response["status_code"]


@ai_blueprint.route("/statistics/likes", methods=['GET'])
def get_average_likes():
    return stats.load_data('videoLikeCount', "Average Likes")


@ai_blueprint.route("/statistics/dislikes", methods=['GET'])
def get_average_dislikes():
    return stats.load_data('videoDislikeCount', "Average Dislikes")


@ai_blueprint.route("/statistics/comments", methods=['GET'])
def get_average_comments():
    return stats.load_data('VideoCommentCount', "Average Comments")


@ai_blueprint.route("/statistics/views", methods=['GET'])
def get_average_views():
    return stats.load_data('videoViewCount', "Average Views")


@ai_blueprint.route("/statistics/describe", methods=['GET'])
def get_description():
    stat_calc.reload()
    stat_calc.filter_data(**request.args)
    return stat_calc.describe_all_features()
