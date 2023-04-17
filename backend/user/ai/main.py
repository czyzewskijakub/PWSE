import pandas as pd

def main():
    set_pandas_options()
    load_data()

def set_pandas_options():
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

def load_data():
    data_df = pd.read_csv('data/YouTubeDataset_withChannelElapsed.csv')
    print(data_df.head())

if __name__ == "__main__":
    main()