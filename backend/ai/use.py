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
            "channel_comment_count", "video_categoryId", "likes", "dislikes", "comments", "elapsed_time",
            "video_published"]

    for key in keys:
        if key not in req_body:
            print(key)
            return {"error": "Not acceptable prediction parameters where provided", "status_code": 406}

    params = list(req_body.values())
    file = os.path.join(pathlib.Path(__file__).parent, path)

    model: VideoViewsPredictor = VideoViewsPredictor(20)
    trainer = VideoViewsPredictorTrainer(model)
    trainer.load(file)

    data = [params[0] / params[1], params[0], params[6] / params[3], params[0] / params[2] / params[3], params[2],
            params[3], params[7] / params[0] / params[2], params[8] / params[3], params[6] / params[0] / params[2],
            params[4], params[6] / params[7], params[8] / params[0] / params[2], params[0] / params[2], params[9],
            params[6], params[7], params[7] / params[3], params[0] / params[3], params[0] / params[2] / params[9],
            params[8]]

    result = trainer.predict(data)
    return {"result": result, "status_code": 200}


