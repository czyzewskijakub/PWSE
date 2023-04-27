import pandas as pd
import time
import datetime

data = pd.read_csv('data/data.csv')

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data2 = data[["videoCount", "channelViewCount", "channelCommentCount", "channelelapsedtime", "subscriberCount", "videoCategoryId",  "videoPublished", "videoLikeCount",  "videoDislikeCount", "VideoCommentCount",  "elapsedtime", "videoViewCount",]]
data2.columns = ['CVideos', 'CViews', 'CComments', 'CElapsedTime', 'CSubscribers', 'VCategory', 'VPublishedDate', 'VLikes', 'VDislikes', 'VComments', 'VElapsedTime', 'VViews']

data2['VPublishedDate'] = data2['VPublishedDate'].apply(lambda x: time.mktime(datetime.datetime.strptime(x[:10], "%Y-%m-%d").timetuple()))

# max_value = data2.max().to_dict()
# min_value = data2.min().to_dict()
# print(max_value)
# print(min_value)
# data2 = data2.div(max_value)

print(data2.head())

data2.to_csv('data\data1.csv')