import pandas as pd


class StatCalculator:

    def __init__(self, data='../ai/data/data.csv', **kwargs) -> None:
        super().__init__()
        self.data = None
        self.data_path = data
        self.reload()
        self.filter_data(**kwargs)

    def describe_all_features(self):
        return self.data.drop('index', axis=1).describe().to_dict()

    def describe_feature(self, column):
        return self.data.drop('index', axis=1)[column].describe().to_dict()

    def filter_data(self, **kwargs):
        if kwargs:
            conditions = ' & '.join(
                [self.__build_condition(k, v) for k, v in kwargs.items()])
            self.data = eval(f'self.data[{conditions}]')

    def __build_condition(self, k: str, v):
        return f'(self.data[\'{self.__remove_prefix(self.__remove_prefix(k, "min"), "max")}\'] ' \
               f'{self.__get_comparator_sign(k)} {v})'

    @staticmethod
    def __get_comparator_sign(column):
        return ">=" if column.startswith("min") else ("<=" if column.startswith("max") else "==")

    @staticmethod
    def __remove_prefix(text, prefix):
        return text[text.startswith(prefix) and len(prefix):]

    def reload(self):
        self.data = pd.read_csv(self.data_path)


calc = StatCalculator(CComments=21, minCVideos=8, maxCVideos=12)
print()
