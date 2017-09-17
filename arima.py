# -*- coding:utf-8 -*-
#
# ARIMA model
#

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA


# data preprocess
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
ua = pd.read_csv('datas/mars_tianchi_user_actions.csv',
                 parse_dates='Ds', date_parser=dateparse)
so = pd.read_csv('datas/mars_tianchi_songs.csv')

data = pd.merge(ua, so, on=['song_id'])
arts = data[data.action_type == 1].groupby(['artist_id',
                                            'Ds'])['action_type'].sum()
arts.to_csv('datas/arts.csv')
arts = pd.read_csv('datas/arts.csv', names=['artist_id', 'Ds', 'plays'],
                   parse_dates='Ds', date_parser=dateparse, index_col='Ds')

result = pd.DataFrame(columns=['artist_id', 'plays', 'Ds'])

# fit data
for aid in arts['artist_id']:
    one = arts[arts.artist_id == aid]
    one.pop('artist_id')
    ts = pd.Series(data=one['plays'], index=one.index)
    # log
    ts_log = np.log(ts)
    # difference
    ts_log_diff = ts_log - ts_log.shift(7)
    ts_log_diff.dropna(inplace=True)
    # arima
    model = ARIMA(ts_log_diff, order=(7, 0, 0))
    results_ARIMA = model.fit(maxiter=1000000)
    # fit
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(
        predictions_ARIMA_diff_cumsum, fill_value=0)
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    # predict
    pred = results_ARIMA.predict(start='20150831', end='20151030')
    pred_ARIMA_diff_cumsum = pred.cumsum()
    pred_ARIMA_log = pd.Series(ts_log.ix[len(ts_log) - 1], index=pred.index)
    pred_ARIMA_log = pred_ARIMA_log.add(pred_ARIMA_diff_cumsum, fill_value=0)
    pred_ARIMA = np.exp(pred_ARIMA_log)
    # plot
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(ts)
    ax.plot(predictions_ARIMA)
    ax.plot(pred_ARIMA)
    fig.savefig('images/' + aid + '.png')
    plt.close(fig)
    # save result
    n = len(pred_ARIMA)
    res = pd.DataFrame()
    res['artist_id'] = [aid for x in xrange(n)]
    res['plays'] = pred_ARIMA.values
    res['Ds'] = pred_ARIMA.index
    result = pd.concat([res, result])
    result.to_csv('datas/arima.csv', idnex=False)
