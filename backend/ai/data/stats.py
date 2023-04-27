import json
import os

import pandas as pd


def load_data(parameter, values_desc):
    path = os.getcwd()+"/ai/data.csv"
    data_df = pd.read_csv(path)
    a = data_df.groupby('videoCategoryId')[parameter].mean()

    x = a.keys().tolist()
    path2 = os.getcwd()+"/ai/categoryID.csv"
    data_df2 = pd.read_csv(path2)
    category_title = data_df2[["categoryID", "Title"]].to_numpy()
    y = a.tolist()

    return prepare_json_results_from_array(x, y, category_title, values_desc)


def prepare_json_results_from_array(x, y, category_title, values_desc):
    lista = []
    for j in range(len(x)):
        category = ""
        for i in range(len(category_title)):
            if x[j] == category_title[i][0]:
                category = category_title[i][1]
                break
        if category == "":
            category = "Uncategorized"
        object = {"Category": category, values_desc: round(y[j])}
        lista.append(object)
    return json.dumps(lista)