# -*- coding:utf-8 -*-
#
# 把训练好的每首歌的播放量汇总
# 生成可以提交的格式
#

import numpy as np
import pandas as pd
import sys

day = int(sys.argv[1])

data = pd.read_csv(
    'datas/raw_train_result/plays' + str(day) + '.csv',
    names=['song_id', 'plays'])
artists = pd.read_csv('datas/mars_tianchi_songs.csv')

n = len(artists)
plays = np.zeros(n)

data = data.groupby(['song_id'])['plays'].sum()

for i in xrange(0, n):
    sid = artists.ix[i]['song_id']
    sid = int(sid, 16)
    sid = str(sid)
    if sid in data.index:
        plays = data.ix[sid]

artists['plays'] = plays

result = artists.groupby(['artist_id'])['plays'].sum()
result = result.astype('int')
result.to_csv('datas/temp.csv')

# 调整格式
result = pd.read_csv('datas/temp.csv', names=['song_id', 'plays'])
n = len(result)
result['day'] = [str(day) for x in xrange(n)]


# 最终输出, 需要手动把第一行去掉
result.to_csv('datas/final/' + str(day) + '.csv', index=False)
