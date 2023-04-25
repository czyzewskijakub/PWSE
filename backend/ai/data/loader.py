import json

import pandas as pd
import matplotlib.pyplot as plt


def main():
    set_pandas_options()
    load_data()


def set_pandas_options():
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


def load_data():
    # Change to your Path
    data_df = pd.read_csv("C:\Studia\Semy\Sem 6\PWSE\\PWSE\\backend\\ai\data\YouTubeDataset_withChannelElapsed.csv")
    a = data_df.groupby('videoCategoryId')['videoLikeCount'].sum()
    x = a.keys().tolist()
    y = a.tolist()

    return prepare_json_results_from_array(x, y)


def prepare_json_results_from_array(x, y):
    lista = []
    for i in range(len(x)):
        object = {"x": x[i], "y": y[i]}
        lista.append(object)
    print(lista)
    return json.dumps(lista)

# coding=utf-8
from PrepareData import PrepareData
from VideoViewsPredictor import VideoViewsPredictor
from VideoViewsPredictorTrainer import VideoViewsPredictorTrainer

if __name__ == "__main__":
    epochs = 900000
    path = f'{epochs}.pt'
    data = PrepareData('data/data.csv')
    print(data.DfFinal.columns)
    net = VideoViewsPredictor(data.Columns)

    trainer = VideoViewsPredictorTrainer(net)
    # trainer.train(data.X_train, data.Y_train, epochs)
    # trainer.evaluate(data.X_test, data.Y_test)
    # trainer.save(path)
    trainer.load(path)
    # trainer.quick_predict(data.X_test, data.Y_test, 10)
    # print(data.X_test[0])
    # print(data.Y_test[0])
    print(trainer.compute_accuracy(data.X_test, data.Y_test, 10))
