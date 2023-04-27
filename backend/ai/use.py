import os
import pathlib
from typing import Dict

from  ..ai.VideoViewsPredictor import VideoViewsPredictor
from ..ai.VideoViewsPredictorTrainer import VideoViewsPredictorTrainer
from sklearn.preprocessing import StandardScaler


def test(data: Dict):
    keys = ["channel_view_count", "channel_elapsed_time", "channel_video_count", "channel_subscriber_count",
            "channel_comment_count", "video_categoryId", "likes", "dislikes", "comments", "elapsed_time",
            "video_published"]

    for key in keys:
        if key not in data:
            return {"error": "Not acceptable prediction parameters where provided", "status_code": 406}

    parsed_data = {'CVideos': data['channel_video_count'], 'CViews': data['channel_view_count'],
                   'CComments': data['channel_comment_count'], 'CElapsedTime': data['channel_elapsed_time'],
                   'CSubscribers': data['channel_subscriber_count'], 'VCategory': data['video_categoryId'],
                   'VPublishedDate': data['video_published'], 'VLikes': data['likes'], 'VDislikes': data['dislikes'],
                   'VComments': data['comments'], 'VElapsedTime': data['elapsed_time']}

    net = VideoViewsPredictor(11)
    trainer = VideoViewsPredictorTrainer(net, StandardScaler())
    file = os.path.join(pathlib.Path(__file__).parent, "30000.pt")

    trainer.load(file)

    views = int(trainer.predict(parsed_data)[0])

    return {"views": views, "status_code": 200}


