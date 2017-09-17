# -*- coding:utf-8 -*-
#
# STL decomposition & Random Forest
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
from sklearn.ensemble.forest import RandomForestRegressor
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
so = pd.read_csv('datas/p2_mars_tianchi_songs.csv')
mean = pd.read_csv('datas/p2_mean.csv', names=['artist_id', 'plays', 'Ds'])

result = pd.DataFrame(columns=['artist_id', 'plays', 'Ds'])

cnt = 0
for aid in arts['artist_id'].unique():
    print cnt, ': ', aid
    cnt += 1
    if aid == '2b7fedeea967becd9408b896de8ff903'\
            or aid == 'aeae35529086c0b12777b314222d7930'\
            or aid == 'cbc53d8b2da2e34974c29b7fc6534444':
        res = pd.DataFrame()
        res['artist_id'] = [aid for x in xrange(n)]
        res['plays'] = mean[mean.artist_id == aid]['plays'].tolist()
        res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                     for x in pd.date_range('20150901', '20151030')]
        result = pd.concat([result, res])
        result['plays'] = result['plays'].astype('int')
        result.to_csv('datas/p2_stl_rf.csv', index=False)
        continue
    one = arts[arts.artist_id == aid]
    one.pop('artist_id')
    ts = pd.Series(data=one['plays'], index=one.index)
    ts_log = np.log(ts)

    # STL decomposition
    # weekly
    decomposition = seasonal_decompose(ts_log, freq=7)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # use r's default forecast method fit trend
    rdf = pandas2ri.py2ri(trend)
    ro.globalenv['r_timeseries'] = rdf
    pred_tre = ro.r('as.data.frame(forecast(r_timeseries, h=61))')
    pred_tre.dropna(inplace=True)
    pred_trend = pd.Series(index=pd.date_range('20150901', '20151030'),
                           data=pred_tre['Point Forecast'].tolist()[1:])

    # fit residuals
    # track features
    tset = pd.DataFrame(index=pd.date_range('20150301', '20151030'))
    tset['dayofweek'] = tset.index.dayofweek.tolist()
    tset['dayofmonth'] = [int(x[-2:]) for x in tset.index.to_native_types()]
    tset['isworkday'] = [1 if x >= 0 and x <= 4 else 0
                         for x in tset['dayofweek']]
    tset['isweekend'] = [1 if x >= 5 and x <= 6 else 0
                         for x in tset['dayofweek']]
    tset['monthend'] = [1 if x >= 25 else 0 for x in tset['dayofmonth']]
    tset['feast'] = [1 if x >= '2015-03-04' and x <= '2015-03-06' or
                     x >= '2015-04-05' and x <= '2015-04-06' or
                     x >= '2015-05-01' and x <= '2015-05-03' or
                     x >= '2015-06-20' and x <= '2015-06-22' or
                     x >= '2015-09-26' and x <= '2015-09-28' or
                     x >= '2015-10-01' and x <= '2015-10-07' else 0
                     for x in tset.index.to_native_types()]
    pub = so[so.artist_id == aid]
    pub = pub[pub.publish_time >= 20150301]
    pub = pub['publish_time'].unique()
    pub = [pd.datetime.strptime(str(x), '%Y%m%d') for x in pub]
    tset['new_song'] = [1 if x in pub else 0 for x in tset.index]
    pub_week = []
    [pub_week.extend(pd.date_range(start=x, periods=7).tolist()) for x in pub]
    tset['new_song_a_week'] = [1 if x in pub_week else 0 for x in tset.index]
    pub_month = []
    [pub_week.extend(pd.date_range(start=x, periods=30).tolist()) for x in pub]
    tset['new_song_a_month'] = [1 if x in pub_month else 0 for x in tset.index]

    label = np.array(residual.fillna(residual.mean()))
    train_data = tset['20150301':'20150830']
    train_data = np.array(
        [np.array(train_data.ix[i].tolist())
         for i in train_data.index])
    pred_data = tset['20150831':'20151030']
    pred_data = np.array(
        [np.array(pred_data.ix[i].tolist())
         for i in pred_data.index])

    # model
    rfr = RandomForestRegressor(n_estimators=100)
    # train
    rfr.fit(train_data, label)
    # predict
    pred_resi = rfr.predict(pred_data)
    pred_resi = pd.Series(index=pd.date_range('20150901', '20151030'),
                          data=pred_resi[1:])
    print rfr.feature_importances_

    # seasonal
    pred_sea = seasonal['20150601':'20150731']
    pred_sea.index = pd.date_range('20150831', '20151030')

    # combine and plot
    pred_all_log = pred_resi + pred_trend + pred_sea
    pred_all = np.exp(pred_all_log)
    # correct
    m = mean[mean.artist_id == aid]['plays'].mean()
    pred_mean = pred_all.mean()
    diff = m - pred_mean
    pred_all += diff

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(ts)
    ax.plot(pred_all)
    fig.savefig('images/stl_with_rf/' + aid + '.png')
    plt.close(fig)

    # save result
    pred_all = pred_all[pd.date_range('20150901', '20151030')]
    n = len(pred_all)
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = pred_all.values
    res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                 for x in pred_all.index]
    result = pd.concat([result, res])
    result['plays'] = result['plays'].astype('int')
    result.to_csv('datas/p2_stl_rf.csv', index=False)
