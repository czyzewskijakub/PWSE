import pandas as pd
data = pd.read_csv('data/dataCleaned.csv')

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# data2 = data[["videoCount", "channelViewCount", "channelCommentCount", "channelelapsedtime", "subscriberCount", "videoCategoryId",  "videoPublished", "videoLikeCount",  "videoDislikeCount", "VideoCommentCount",  "elapsedtime", "videoViewCount",]]
# data2.columns = ['CVideos', 'CViews', 'CComments', 'CElapsedTime', 'CSubscribers', 'VCategory', 'VPublishedDate', 'VLikes', 'VDislikes', 'VComments', 'VElapsedTime', 'VViews']
# print(data2.head())

# data2['CViews\CVideos'] = data2['CViews'].div(data2['CVideos'])
# data2['CSubscribers\CVideos'] = data2['CSubscribers'].div(data2['CVideos'])
# print(data2.head())

# data2.to_csv('data/dataCleaned.csv')

# print(data2.drop('VPublishedDate', axis=1).corr())