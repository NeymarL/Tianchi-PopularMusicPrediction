# -*- coding:utf-8 -*-
#
# ARIMA model
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

# fit data
cnt = 0
for aid in arts['artist_id'].unique():
    one = arts[arts.artist_id == aid]
    print cnt, ' : ', aid
    cnt += 1
    one.pop('artist_id')
    ts = pd.Series(data=one['plays'], index=one.index)
    # log
    ts_log = np.log(ts)
    # difference
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)
    # fit model
    rdf = pandas2ri.py2ri(ts_log_diff)
    ro.globalenv['r_timeseries'] = rdf
    pred = ro.r(
        'as.data.frame(forecast(auto.arima(r_timeseries, stationary=TRUE),\
        h=61))')

    # trans back
    pred_ARIMA_diff_cumsum = pred['Point Forecast'].cumsum()
    pred_ARIMA_log = pd.Series(ts_log.ix[len(ts_log) - 1], index=pred.index)
    pred_ARIMA_log = pred_ARIMA_log.add(pred_ARIMA_diff_cumsum, fill_value=0)
    pred_ARIMA = np.exp(pred_ARIMA_log)
    # correct
    difference = pred_ARIMA.mean() - \
        mean[mean.artist_id == aid]['plays'].mean()
    pred_ARIMA -= difference
    pred_ARIMA.index = pd.date_range('20150831', '20151030')
    pred_ARIMA = pred_ARIMA['20150901':'20151030']
    # save
    n = len(pred_ARIMA)
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = pred_ARIMA.values
    res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                 for x in pred_ARIMA.index]
    result = pd.concat([result, res])
    result['plays'] = result['plays'].astype('int')
    result.to_csv('datas/p2_arima.csv', index=False)
