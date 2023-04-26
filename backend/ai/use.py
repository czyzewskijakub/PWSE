from VideoViewsPredictor import VideoViewsPredictor
from VideoViewsPredictorTrainer import VideoViewsPredictorTrainer

def load_model_and_make_prediction(x, path):
    """
    Loads the model saved in .pt format saved under given paramter 'path' and uses it to make prediction using 'x'
    values.

    Arguments:
    - x: Array of values about given youtube channel and video in the order: channelViewCount, channelelapsedtime,
    channelvideoCount, channelsubscriberCount, channelCommentCount, videoCategoryId, likes, dislikes, comments,
    elapsedtime, videoPublished.
    """
    model: VideoViewsPredictor = VideoViewsPredictor(20)
    trainer = VideoViewsPredictorTrainer(model)
    trainer.load(path)
    new_x = [x[0]/x[1], x[0], x[6]/x[3], x[0]/x[2]/x[3], x[2], x[3], x[7]/x[0]/x[2], x[8]/x[3], x[6]/x[0]/x[2], x[4],
             x[6]/x[7], x[8]/x[0]/x[2], x[0]/x[2], x[9], x[6], x[7], x[7]/x[3], x[0]/x[3], x[0]/x[2]/x[9], x[8]]
    y = trainer.predict(new_x)
    return y

