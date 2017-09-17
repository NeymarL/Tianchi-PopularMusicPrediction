# -*- coding:utf-8 -*-
#
# STL decomposition & ARIMA
#

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
from rpy2.robjects import r
import rpy2.robjects as ro
from statsmodels.tsa.seasonal import seasonal_decompose
import random
import math


forecats = rpackages.importr('forecast')
pandas2ri.activate()

# data preprocess
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
'''
ua = pd.read_csv('datas/mars_tianchi_user_actions.csv',
                 parse_dates='Ds', date_parser=dateparse)
so = pd.read_csv('datas/mars_tianchi_songs.csv')

data = pd.merge(ua, so, on=['song_id'])
arts = data[data.action_type == 1].groupby(['artist_id',
                                            'Ds'])['action_type'].sum()
arts.to_csv('datas/arts.csv')
'''
arts = pd.read_csv('datas/arts.csv', names=['artist_id', 'Ds', 'plays'],
                   parse_dates='Ds', date_parser=dateparse, index_col='Ds')
mean = pd.read_csv('datas/p2sqrt_mean.csv', names=['artist_id', 'plays', 'Ds'])
result = pd.DataFrame(columns=['artist_id', 'plays', 'Ds'])


def fit(ts, sqrt=True):
    if sqrt:
        ts_sqrt = np.sqrt(ts)
        # rolling mean
        ts_log_diff = ts_sqrt.rolling(window=7, center=False).mean()
    else:
        ts_log_diff = ts
    mean30 = ts_log_diff['20150801':'20150830'].mean()
    mean15 = ts_log_diff['20150815':'20150830'].mean()
    mean10 = ts_log_diff['20150820':'20150830'].mean()
    last = ts_log_diff['20150830':'20150830'].mean()
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

    if sqrt:
        mean = mean * mean

    return mean

cnt = 0
for aid in arts['artist_id'].unique():
    print cnt, ': ', aid
    cnt += 1
    if aid == '2b7fedeea967becd9408b896de8ff903'\
            or aid == 'aeae35529086c0b12777b314222d7930'\
            or aid == 'cbc53d8b2da2e34974c29b7fc6534444':
        es = pd.DataFrame()
        res['artist_id'] = [aid for x in xrange(n)]
        res['plays'] = mean[mean.artist_id == aid]['plays'].tolist()
        res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                     for x in pd.date_range('20150901', '20151030')]
        result = pd.concat([result, res])
        result['plays'] = result['plays'].astype('int')
        result.to_csv('datas/p2_stlmean.csv', index=False)
        continue
    one = arts[arts.artist_id == aid]
    one.pop('artist_id')
    ts = pd.Series(data=one['plays'], index=one.index)
    #ts_sqrt = np.sqrt(ts)

    # STL decomposition
    decomposition = seasonal_decompose(ts, freq=7)
    trend = decomposition.trend.dropna()
    seasonal = decomposition.seasonal.dropna()
    residual = decomposition.resid.dropna()

    '''
    rdf = pandas2ri.py2ri(trend)
    ro.globalenv['r_timeseries'] = rdf
    pred_tre = ro.r('as.data.frame(forecast(r_timeseries, h=61))')
    pred_tre.dropna(inplace=True)
    pred_trend = pd.Series(index=pd.date_range('20150901', '20151030'),
                           data=pred_tre['Point Forecast'].tolist()[1:])
    '''

    mean_trend = fit(trend)
    pred_trend = pd.Series(index=pd.date_range('20150831', '20151030'),
                           data=[mean_trend for x in range(61)])

    # fit residuals
    mean_resi = fit(residual, False)

    pred_resi = pd.Series(index=pd.date_range('20150831', '20151030'),
                          data=[mean_resi for x in range(61)])

    # seasonal
    pred_sea = seasonal['20150601':'20150731']
    pred_sea.index = pd.date_range('20150831', '20151030')

    # combine and plot
    pred_all = pred_resi + pred_trend + pred_sea
    # correct
    '''
    m = mean[mean.artist_id == aid]['plays'].mean()
    pred_mean = pred_all.mean()
    if pred_all.min >= m or pred_all.max <= m:
        diff = m - pred_mean
        pred_all += diff
    '''
    pred_mean = pred_all.rolling(window=7, center=False).mean()
    pred_mean.fillna(method='bfill', inplace=True)
    pred_mean.fillna(method='ffill', inplace=True)
    pred_mean = pred_mean[1:]

    # save result
    pred_all = pred_all[pd.date_range('20150901', '20151030')]
    n = len(pred_all)
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = pred_mean.values
    res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                 for x in pred_all.index]
    result = pd.concat([result, res])
    result['plays'] = result['plays'].astype('int')
    result.to_csv('datas/p2_stlmean.csv', index=False)
