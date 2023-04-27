# coding=utf-8
import datetime
import time

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class PrepareData:
    max_values = {'CVideos': 415500.0, 'CViews': 23798172642.0, 'CComments': 3953563.0, 'CElapsedTime': 108913.0,
                  'CSubscribers': 25253114.0, 'VCategory': 44.0, 'VPublishedDate': 1443996000.0, 'VLikes': 1240473.0,
                  'VDislikes': 244280.0, 'VComments': 191498.0, 'VElapsedTime': 106609.0}
    min_values = {'CVideos': 0.0, 'CViews': 0.0, 'CComments': 0.0, 'CElapsedTime': 888.0, 'CSubscribers': 0.0,
                  'VCategory': 1.0, 'VPublishedDate': 1123279200.0, 'VLikes': -1.0, 'VDislikes': -1.0,
                  'VComments': -1.0, 'VElapsedTime': 17520.0}

    columns = ['CVideos', 'CViews', 'CComments', 'CElapsedTime', 'CSubscribers', 'VCategory', 'VPublishedDate',
               'VLikes', 'VDislikes', 'VComments', 'VElapsedTime']

    def __init__(self, path: str = 'data/dataCleaned.csv', exclude_cols=None, tested_col_name: str = 'VViews',
                 test_size: float = 0.2, random_state: int = 42):
        if exclude_cols is None:
            exclude_cols = ['index']

        self.Path: str = path
        self.Exclude_cols = exclude_cols
        self.TestedColName: str = tested_col_name
        self.TestSize: float = test_size
        self.RandomState: float = random_state

        self.Df = pd.read_csv(self.Path)
        self.DfFinal = self.Df.drop(self.Exclude_cols, axis=1)

        self.DfFinal['VPublishedDate'] = self.DfFinal['VPublishedDate'].apply(lambda x: time.mktime(datetime.datetime.strptime(x[:10], "%Y-%m-%d").timetuple()))

        self.DfFinal = self.DfFinal.fillna(0)

        self.X = self.DfFinal.drop([self.TestedColName], axis=1)
        self.Y = self.DfFinal[self.TestedColName].values.reshape(-1, 1)  # Reshape target tensor to match predicted output tensor
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=self.TestSize,
                                                                                random_state=self.RandomState)
        self.X_train = self.X.copy()
        self.Y_train = self.Y.copy()

        # for column in self.columns:
        #     self.X_train[column] = self.X_train[column].apply(lambda x: (x-self.min_values[column])/(self.max_values[column]-self.min_values[column]))
        #
        # for column in self.columns:
        #     self.X_test[column] = self.X_test[column].apply(lambda x: (x-self.min_values[column])/(self.max_values[column]-self.min_values[column]))

        self.Scaler = StandardScaler()
        self.Scaler.fit(self.X)
        self.X_train = self.Scaler.transform(self.X_train)
        self.X_test = self.Scaler.transform(self.X_test)

        # self.X_train = self.X_train.to_numpy()
        # self.X_test = self.X_test.to_numpy()

        self.Columns: int = self.X.shape[1]

    @staticmethod
    def normalize(inputs):
        if isinstance(inputs[6], str):
            inputs[6] = time.mktime(datetime.datetime.strptime(inputs[6][:10], "%Y-%m-%d").timetuple())
        for i in range(len(inputs)):
            inputs[i] = (inputs[i]-PrepareData.min_values[PrepareData.columns[i]])/(PrepareData.max_values[PrepareData.columns[i]]-PrepareData.min_values[PrepareData.columns[i]])
        return inputs

if __name__=="__main__":
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    data = PrepareData('data/data1.csv')
    df = data.DfFinal.copy()
    df['VPublishedDate'].apply(lambda x: x-1123279200)
    print(df.corr())

