import pandas as pd
import time
import datetime

data = pd.read_csv('data/data.csv')

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data2 = data[["videoCount", "channelViewCount", "channelCommentCount", "channelelapsedtime", "subscriberCount", "videoCategoryId",  "videoPublished", "videoLikeCount",  "videoDislikeCount", "VideoCommentCount",  "elapsedtime", "videoViewCount",]]
data2.columns = ['CVideos', 'CViews', 'CComments', 'CElapsedTime', 'CSubscribers', 'VCategory', 'VPublishedDate', 'VLikes', 'VDislikes', 'VComments', 'VElapsedTime', 'VViews']

data2['VPublishedDate'] = data2['VPublishedDate'].apply(lambda x: time.mktime(datetime.datetime.strptime(x[:10], "%Y-%m-%d").timetuple()))

data2.to_csv('data\data1.csv')