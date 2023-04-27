from flask import Blueprint, request, jsonify

from .data import stats
from ..ai.use import test

ai_blueprint = Blueprint("ai", __name__, url_prefix="/ai")


@ai_blueprint.route("/predict", methods=['POST'])
def prediction():
    req_body = request.get_json()
    response = test(req_body)
    if "error" in response:
        return jsonify({"error": response["error"]}), response["status_code"]
    return jsonify({"views": response["views"]}), response["status_code"]


@ai_blueprint.route("/statistics/likes")
def get_average_likes():
    return stats.load_data('videoLikeCount', "Average Likes")

@ai_blueprint.route("/statistics/dislikes")
def get_average_dislikes():
    return stats.load_data('videoDislikeCount', "Average Dislikes")

@ai_blueprint.route("/statistics/comments")
def get_average_comments():
    return stats.load_data('VideoCommentCount', "Average Comments")

@ai_blueprint.route("/statistics/views")
def get_average_views():
    return stats.load_data('videoViewCount', "Average Views")


