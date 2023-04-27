import json
import os

import pandas as pd


def main():
    set_pandas_options()
    load_data()


def set_pandas_options():
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


def load_data():
    # Change to your Path
    path = os.getcwd()+"/ai/data.csv"
    data_df = pd.read_csv(path)
    a = data_df.groupby('videoCategoryId')['videoLikeCount'].sum()
    x = a.keys().tolist()
    y = a.tolist()

    return prepare_json_results_from_array(x, y)


def prepare_json_results_from_array(x, y):
    lista = []
    for i in range(len(x)):
        object = {"Category": x[i], "Average Likes": y[i]}
        lista.append(object)
    print(lista)
    return json.dumps(lista)