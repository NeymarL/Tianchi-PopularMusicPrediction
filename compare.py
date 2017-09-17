# -*- coding:utf-8 -*-
#
# 可视化不同分数的结果
#

import pandas as pd
import numpy as np
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

# some predict score
dslog = pd.read_csv('datas/song_log.csv',
                    names=['artist_id', 'plays', 'Ds'],
                    parse_dates='Ds', date_parser=dateparse,
                    index_col='Ds')
dlog = pd.read_csv('datas/p2log_mean.csv', names=['artist_id', 'plays', 'Ds'],
                   parse_dates='Ds', date_parser=dateparse, index_col='Ds')
dsqrt = pd.read_csv('datas/sqrt15186.csv',
                    names=['artist_id', 'plays', 'Ds'],
                    parse_dates='Ds', date_parser=dateparse, index_col='Ds')
dsqrt10 = pd.read_csv('datas/p2sqrt_mean10.csv',
                      names=['artist_id', 'plays', 'Ds'], parse_dates='Ds',
                      date_parser=dateparse, index_col='Ds')

dlog10 = pd.read_csv('datas/p2log_mean10.csv',
                     names=['artist_id', 'plays', 'Ds'],
                     parse_dates='Ds', date_parser=dateparse, index_col='Ds')

dsong = pd.read_csv('datas/song_new2.csv',
                    names=['artist_id', 'plays', 'Ds'],
                    parse_dates='Ds', date_parser=dateparse, index_col='Ds')
dstlrf = pd.read_csv('datas/p2_new_stl_rf.csv',
                     names=['artist_id', 'plays', 'Ds'],
                     parse_dates='Ds', date_parser=dateparse, index_col='Ds')

cnt = 0
for aid in arts['artist_id'].unique():
    print cnt, ': ', aid
    cnt += 1
    # if arts[arts.artist_id == aid]['plays'].max() < 1000:
    #    continue
    merge = pd.concat([arts, dstlrf])
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(merge[merge.artist_id == aid]['plays'], label='Origin')
    #ax.plot(dlog[dlog.artist_id == aid]['plays'], label='Mlog 15171')
    ax.plot(dsqrt[dsqrt.artist_id == aid]['plays'],
            label='Msqrt 15186')
    ax.plot(dsong[dsong.artist_id == aid]['plays'],
            label='Song new')
    ax.plot(dsqrt10[dsqrt10.artist_id == aid]['plays'], label='Sqrt 10')
    ax.plot(dslog[dslog.artist_id == aid]['plays'],
            label='Song log')
    #ax.plot(dstlrf[dstlrf.artist_id == aid]['plays'], label='STL RF')
    ax.legend(loc='best')
    fig.savefig('images/p2_all/' + aid + '.png')
    plt.close(fig)

# c5f0170f87a2fbb17bf65dc858c745e2
# c7425ea3ecbea3a51b5550c698be7e71
#
