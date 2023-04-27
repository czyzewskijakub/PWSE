# coding=utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class PrepareData:
    def __init__(self, path: str = 'data/data.csv', exclude_cols=None, tested_col_name: str = 'channelViewCount',
                 test_size: float = 0.2, random_state: int = 42):
        if exclude_cols is None:
            exclude_cols = ['index', 'channelId', 'videoCategoryId', 'videoId', 'videoPublished', 'channelelapsedtime']

        self.Path: str = path
        self.Exclude_cols = exclude_cols
        self.TestedColName: str = tested_col_name
        self.TestSize: float = test_size
        self.RandomState: float = random_state

        self.Df = pd.read_csv(self.Path)
        self.DfFinal = self.Df.drop(self.Exclude_cols, axis=1)
        self.DfFinal = self.DfFinal.fillna(0)

        # Convert categorical variables to numerical variables
        self.DfFinal['totvideos/videocount'] = pd.factorize(self.DfFinal['totvideos/videocount'])[0]
        self.DfFinal['elapsedtime'] = pd.factorize(self.DfFinal['elapsedtime'])[0]

        X = self.DfFinal.drop([self.TestedColName], axis=1)
        y = self.DfFinal[self.TestedColName].values.reshape(-1,
                                                            1)  # Reshape target tensor to match predicted output tensor
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, y, test_size=self.TestSize,
                                                                                random_state=self.RandomState)

        # Scale the data
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

        self.Columns: int = self.DfFinal.shape[1] - 1
