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
    # 2,72,48265,5,72240,338,27,2009-08-07T06:51:10.000Z,8,1,2,71544,3478                       22641.5	650%
    # 5,53,211649,1,93121,232,26,2009-02-24T02:06:10.000Z,4,0,0,75480,12998                     12242.0322265625 94%
    # 3,172,2116722,74,82512,22051,26,2011-08-04T01:07:38.000Z,161,6,10,54096,19497             17340.095703125 88%
    # 240911,165,4658668,22,76128,17095,26,2012-08-27T14:25:00.000Z,53,5,3,44760,16325          12566.4453125 77%
    # 240937,21,320948,17,61080,625,10,2012-07-27T12:05:08.000Z,88,3,13,45504,23017             23190.123046875	100.7%
    # 151,1766,399839933,2541,100081,1043486,24,2013-05-16T19:37:43.000Z,1022,27,96,38448,50028 73149.9296875 146%
    # 240668,46,932034,29,73800,695,20,2013-07-02T11:42:38.000Z,556,161,139,37344,160002        367913.21875 230%
    # 240833,39,10125019,29,99097,2115,10,2006-08-08T13:31:44.000Z,2102,271,410,97825,4530340	2652579.0 58%

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
