import os
import pathlib

from ..ai.VideoViewsPredictor import VideoViewsPredictor
from ..ai.VideoViewsPredictorTrainer import VideoViewsPredictorTrainer


def load_model_and_make_prediction(req_body, path):
    """
    Loads the model saved in .pt format saved under given paramter 'path' and uses it to make prediction using 'x'
    values.

    Arguments:
    - x: Array of values about given youtube channel and video in the order: channelViewCount, channelelapsedtime,
    channelvideoCount, channelsubscriberCount, channelCommentCount, videoCategoryId, likes, dislikes, comments,
    elapsedtime, videoPublished.
    """
    keys = ["channel_view_count", "channel_elapsed_time", "channel_video_count", "channel_subscriber_count",
            "channel_comment_count", "likes", "dislikes", "comments", "elapsed_time"]

    for key in keys:
        if key not in req_body:
            print(key)
            return {"error": "Not acceptable prediction parameters where provided", "status_code": 406}

    file = os.path.join(pathlib.Path(__file__).parent, path)

    model: VideoViewsPredictor = VideoViewsPredictor(20)
    trainer = VideoViewsPredictorTrainer(model)
    trainer.load(file)

    data = [req_body["channel_view_count"] / req_body["channel_elapsed_time"], req_body["channel_view_count"],
            req_body["likes"] / req_body["channel_subscriber_count"],
            req_body["channel_view_count"]  / req_body["channel_video_count"] / req_body["channel_subscriber_count"],
            req_body["channel_video_count"], req_body["channel_subscriber_count"],
            req_body["dislikes"] / req_body["channel_view_count"] / req_body["channel_video_count"],
            req_body["comments"] / req_body["channel_subscriber_count"],
            req_body["likes"] / req_body["channel_view_count"]  / req_body["channel_video_count"],
            req_body["channel_comment_count"], req_body["likes"] / req_body["dislikes"],
            req_body["comments"] / req_body["channel_view_count"]  / req_body["channel_video_count"],
            req_body["channel_view_count"]  / req_body["channel_video_count"], req_body["elapsed_time"],
            req_body["likes"], req_body["dislikes"], req_body["dislikes"] / req_body["channel_subscriber_count"],
            req_body["channel_view_count"]  / req_body["channel_subscriber_count"],
            req_body["channel_view_count"]  / req_body["channel_video_count"]  / req_body["elapsed_time"],
            req_body["comments"]]


    result = trainer.predict(data)
    return {"result": result, "status_code": 200}


