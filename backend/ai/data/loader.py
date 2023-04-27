# coding=utf-8
import pandas as pd

from PrepareData import PrepareData
from VideoViewsPredictor import VideoViewsPredictor
from VideoViewsPredictorTrainer import VideoViewsPredictorTrainer
from use import load_model_and_make_prediction

if __name__ == "__main__":
    epochs = 10000
    path = f'{30000}.pt'
    path2 = f'{epochs}2.pt'
    data = PrepareData('data/data1.csv')
    net = VideoViewsPredictor(data.Columns)
    trainer = VideoViewsPredictorTrainer(net, data.Scaler)
    trainer.load(path)
    trainer.train(data.X_train, data.Y_train, epochs)
    trainer.evaluate(data.X_test, data.Y_test)
    trainer.save(path2)

    # trainer.load(path)


    # to_test_data = data.Df.drop(data.Exclude_cols, axis=1)
    to_test = [data.X.iloc[x].to_dict() for x in range(10)]

    trainer.quick_predict(to_test, data.Y, 10)

    # trainer.quick_predict2(data.X_test, data.Y_test, 10)

    # print(trainer.compute_accuracy(data.X_test, data.Y_test, 30))

    # x = {
    # "channel_view_count": 123,
    # "channel_elapsed_time": 1,
    # "channel_video_count": 2,
    # "channel_subscriber_count": 3,
    # "channel_comment_count": 5,
    # "video_categoryId": 4,
    # "likes": 6,
    # "dislikes": 7999999,
    # "comments": 823234234,
    # "elapsed_time": 9,
    # "video_published": 11
    # }
    #
    # print(load_model_and_make_prediction(x, '900000.pt'))
