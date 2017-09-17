# -*- coding:utf-8 -*-
#
# 研究song's均值
#

import pandas as pd
import numpy as np
import math
import matplotlib.pylab as plt

dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
songs = pd.read_csv('datas/songs.csv',
                    names=['artist_id', 'song_id', 'Ds', 'plays'],
                    parse_dates='Ds', date_parser=dateparse, index_col='Ds')

result = pd.DataFrame(columns=['artist_id', 'plays', 'Ds'])

cnt = 0
for aid in songs['artist_id'].unique():
    print cnt, ': ', aid
    cnt += 1
    ts = songs[songs.artist_id == aid]
    ts.pop('artist_id')
    asum = 0

    for sid in ts['song_id'].unique():
        onets = ts[ts.song_id == sid]
        onets.pop('song_id')
        # log
        one_log = np.log(onets)
        # rolling mean
        one = one_log.rolling(window=7, center=False).mean()
        one.fillna(inplace=True, method='bfill')

        mean60 = one['20150701':'20150830'].mean().tolist()[0]
        mean30 = one['20150801':'20150830'].mean().tolist()[0]
        mean15 = one['20150815':'20150830'].mean().tolist()[0]
        mean10 = one['20150820':'20150830'].mean().tolist()[0]
        last = one['20150830':'20150830'].mean().tolist()[0]
        diff60 = mean60 - last
        diff30 = mean30 - last
        diff15 = mean15 - last
        diff10 = mean10 - last

        mean = mean10
        minium = min(abs(diff10), abs(diff15), abs(diff30), abs(diff60))
        if minium == abs(diff30):
            mean = mean30
        elif minium == abs(diff15):
            mean = mean15
        elif minium == abs(diff60):
            mean = mean60
        else:
            mean = mean10

        mean = math.exp(mean)

        if not np.isnan(mean):
            asum += mean

    n = 60
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = [asum for x in xrange(n)]
    res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                 for x in pd.date_range('20150901', '20151030')]
    result = pd.concat([result, res])
    result['plays'] = result['plays'].astype('int')
    result.to_csv('datas/song_log.csv', index=False)

# 2e14d32266ee6b4678595f8f50c369ac
# 4b8eb68442432c242e9242be040bacf9
# c5f0170f87a2fbb17bf65dc858c745e2
# c7425ea3ecbea3a51b5550c698be7e71
# 6bb4c3bbdb6f5a96d643320c6b6005f5 merge
#
