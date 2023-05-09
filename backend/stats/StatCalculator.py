import pandas as pd


class StatCalculator:

    def __init__(self, data='../ai/data/data.csv') -> None:
        super().__init__()
        self.data = pd.read_csv(data)

    def describe_all_features(self):
        return self.data.drop('index', axis=1).describe().to_dict()

    def describe_feature(self, column):
        return self.data.drop('index', axis=1)[column].describe()
