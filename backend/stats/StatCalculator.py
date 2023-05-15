import pandas as pd


class StatCalculator:

    def __init__(self, data='../ai/data/data.csv', **kwargs) -> None:
        f"""
        Class used to calculate statistics of dataset used for neural network model training.
        Args:
            data: data path to csv dataset (default: '../ai/data/data.csv')
            **kwargs: data filters (See: filter_data())
        """
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
        """
        Method used to filter dataset used to calculate statistics.
        Args:
            **kwargs: Features with conditions to filter (See examples)
        Examples:
            - `filter_data(minCVideos=8, maxCVideos=12)` - records having CVideos number from 8 to 12 (inclusive)
            - `filter_data(maxCVideos=12)` - records having less or equal CVideos number
            - `filter_data(CComments=21, minCVideos=8, maxCVideos=12)` - records having CComments value equal to 21
        Notes:
            You can also pass this filter parameters into StatCalculator constructor to have data filtered on init.
        """
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
