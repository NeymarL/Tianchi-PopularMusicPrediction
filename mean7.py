# -*- coding:utf-8 -*-
#
# 研究均值
#

import pandas as pd
import numpy as np
import math
import matplotlib.pylab as plt

# origin data
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
'''
ua = pd.read_csv('datas/p2_mars_tianchi_user_actions.csv',
                 parse_dates='Ds', date_parser=dateparse)
so = pd.read_csv('datas/p2_mars_tianchi_songs.csv')

data = pd.merge(ua, so, on=['song_id'])
arts = data[data.action_type == 1].groupby(['artist_id',
                                            'Ds'])['action_type'].sum()
arts.to_csv('datas/arts.csv')
'''
arts = pd.read_csv('datas/arts.csv', names=['artist_id', 'Ds', 'plays'],
                   parse_dates='Ds', date_parser=dateparse, index_col='Ds')

result = pd.DataFrame(columns=['artist_id', 'plays', 'Ds'])

cnt = 0
for aid in arts['artist_id'].unique():
    print cnt, ': ', aid
    cnt += 1
    one = arts[arts.artist_id == aid]
    one.pop('artist_id')
    # log
    one_log = np.sqrt(one)
    # rolling mean
    one = one_log.rolling(window=7, center=False).mean()
    one.fillna(inplace=True, method='bfill')

    mean30 = one['20150801':'20150830'].mean().tolist()[0]
    mean15 = one['20150815':'20150830'].mean().tolist()[0]
    mean10 = one['20150820':'20150830'].mean().tolist()[0]
    last = one['20150830':'20150830'].mean().tolist()[0]
    diff30 = mean30 - last
    diff15 = mean15 - last
    diff10 = mean10 - last

    mean = mean10
    if abs(diff30) <= abs(diff10) and abs(diff30) <= abs(diff15):
        mean = mean30
    elif abs(diff15) <= abs(diff30) and abs(diff15) <= abs(diff10):
        mean = mean15
    else:
        mean = mean10

    mean = mean * mean
    n = 60
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = [mean for x in xrange(n)]
    res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                 for x in pd.date_range('20150901', '20151030')]
    result = pd.concat([result, res])
    result['plays'] = result['plays'].astype('int')
    result.to_csv('datas/p2sqrt_mean2.csv', index=False)


# c7425ea3ecbea3a51b5550c698be7e71
# ca3e42dfdb7529d540141548674bc63e
# 53dd7de874e0999634c28cdd94d21257
# 5ce35e3085934e1621766ba766437754
# 重要！！
# c026b84e8f23a7741d9b670e3d8973f0
# 300dde62b988fc83eb6dba1b702e9af3
# bc14447beab5353ef057c3ec90199576
# c5f0170f87a2fbb17bf65dc858c745e2
# maybe bad
# 5e1788cd2cce09d8780d44c81a862e19
# cd5ce8f47e50971ddb629d86a0bc34f2
#
# not equal -70
# 300dde62b988fc83eb6dba1b702e9af3
# bc14447beab5353ef057c3ec90199576
# c026b84e8f23a7741d9b670e3d8973f0
# c5f0170f87a2fbb17bf65dc858c745e2
# cd5ce8f47e50971ddb629d86a0bc34f2

# 190   7919
# 175   8226 7750
# 149   8703
