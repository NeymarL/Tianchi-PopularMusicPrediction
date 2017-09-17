# -*- coding:utf-8 -*-
#
# Random Forest
#

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.ensemble.forest import RandomForestRegressor
import random
import math

# data preprocess
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')

arts = pd.read_csv('datas/arts.csv', names=['artist_id', 'Ds', 'plays'],
                   parse_dates='Ds', date_parser=dateparse, index_col='Ds')

mean = pd.read_csv('datas/p2sqrt_mean.csv', names=['artist_id', 'plays', 'Ds'])

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
        result.to_csv('datas/p2_rf_not.csv', index=False)
        continue
    one = arts[arts.artist_id == aid]
    one.pop('artist_id')
    ts = pd.Series(data=one['plays'], index=one.index)
    ts_log = np.log(ts)

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

    label = np.array(ts_log.values)
    train_data = tset['20150301':'20150830']
    train_data = np.array(
        [np.array(train_data.ix[i].tolist())
         for i in train_data.index])
    pred_data = tset['20150831':'20151030']
    pred_data = np.array(
        [np.array(pred_data.ix[i].tolist())
         for i in pred_data.index])

    # model
    rfr = RandomForestRegressor(n_estimators=200)
    # train
    rfr.fit(train_data, label)
    # predict
    pred = rfr.predict(pred_data)
    pred = pd.Series(index=pd.date_range('20150901', '20151030'),
                     data=pred[1:])
    pred = np.exp(pred)
    pred_mean = pred.rolling(window=7, center=False).mean()
    pred_mean.fillna(method='bfill', inplace=True)
    pred_mean.fillna(method='ffill', inplace=True)

    n = len(pred_mean)
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = pred_mean.values
    res['Ds'] = [pd.datetime.strftime(x, format='%Y%m%d')
                 for x in pred.index]
    result = pd.concat([result, res])
    result['plays'] = result['plays'].astype('int')
    result.to_csv('datas/p2_rf_not.csv', index=False)
