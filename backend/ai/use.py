import os
import pathlib
from typing import Dict

from VideoViewsPredictor import VideoViewsPredictor
from VideoViewsPredictorTrainer import VideoViewsPredictorTrainer
from sklearn.preprocessing import StandardScaler


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


def test(data: Dict):
    """
    data = {'CVideos': 2, 'CViews': 40, 'CComments': 23, 'CElapsedTime': 888, 'CSubscribers': 1,
                  'VCategory': 1, 'VPublishedDate': "2002-12-03", 'VLikes': 12, 'VDislikes': 3,
                  'VComments': 24, 'VElapsedTime': 17520}

    """
    net = VideoViewsPredictor(11)
    trainer = VideoViewsPredictorTrainer(net, StandardScaler())
    trainer.load('30000.pt')
    return trainer.predict(data)[0]

if __name__ == '__main__':
    # data = {'CVideos': 813, 'CViews': 4009812, 'CComments': 90, 'CElapsedTime': 59736, 'CSubscribers': 40482,
    #               'VCategory': 20, 'VPublishedDate': "2012-06-05", 'VLikes': 83, 'VDislikes': 4,
    #               'VComments': 36, 'VElapsedTime': 46752}

    # data = {'CVideos': 1766, 'CViews': 399839933, 'CComments': 2541, 'CElapsedTime': 100081, 'CSubscribers': 1043486,
    #               'VCategory': 24, 'VPublishedDate': "2013-05-16", 'VLikes': 1022, 'VDislikes': 27,
    #               'VComments': 96, 'VElapsedTime': 38448}

    # data = {'CVideos': 46, 'CViews': 932034, 'CComments': 29, 'CElapsedTime': 73800, 'CSubscribers': 695,
    #               'VCategory': 20, 'VPublishedDate': "2013-07-02", 'VLikes': 556, 'VDislikes': 161,
    #               'VComments': 139, 'VElapsedTime': 37344}

    # data = {'CVideos': 39, 'CViews': 10125019, 'CComments': 29, 'CElapsedTime': 99097, 'CSubscribers': 2115,
    #               'VCategory': 10, 'VPublishedDate': "2006-08-08", 'VLikes': 2102, 'VDislikes': 271,
    #               'VComments': 410, 'VElapsedTime': 97825}

    # data = {'CVideos': 165, 'CViews': 4658668, 'CComments': 22, 'CElapsedTime': 76128, 'CSubscribers': 17095,
    #               'VCategory': 26, 'VPublishedDate': "2012-08-27", 'VLikes': 53, 'VDislikes': 5,
    #               'VComments': 3, 'VElapsedTime': 44760}

    data = {'CVideos': 21, 'CViews': 320948, 'CComments': 17, 'CElapsedTime': 61080, 'CSubscribers': 625,
                  'VCategory': 10, 'VPublishedDate': "2012-07-27", 'VLikes': 88, 'VDislikes': 3,
                  'VComments': 13, 'VElapsedTime': 45504}

    print(test(data))
