# -*- coding:utf-8 -*-
#
# 用 lstm 分析时间序列
#


import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
import datetime

import tensorflow.contrib.learn as skflow
from sklearn.metrics import mean_squared_error

from lstm import lstm_model

LOG_DIR = './lstm.log'
TIMESTEPS = 30
RNN_LAYERS = [{'steps': TIMESTEPS}, {'steps': 30, 'keep_prob': 0.5}]
DENSE_LAYERS = [2]
TRAINING_STEPS = 10000
BATCH_SIZE = 100
PRINT_STEPS = TRAINING_STEPS / 100

data = pd.read_csv('datas/artist_every_day_plays.csv')

apts = data.groupby(['artist_id', 'diff'])['plays'].sum()
arts = data.groupby(['artist_id'])['plays'].sum()
artist_set = arts.index

result = pd.DataFrame(columns=['artist_id', 'plays', 'Ds'])

for a1 in artist_set:
    # prepare train data
    X = apts.ix[a1].index.tolist()
    y = apts.ix[a1].tolist()
    X = np.array(X)
    y = np.array(y)

    realX = []
    for i in range(len(X) - TIMESTEPS):
        realX.append([[x] for x in X[i:i+TIMESTEPS]])

    realX = np.array(realX)
    realY = np.array(y[TIMESTEPS-1:-1])

    realX = realX.astype('float32')
    realY = realY.astype('float32')

    # test data
    tX = range(0, 243)
    testX = []
    for i in range(152, 182 + 61 - TIMESTEPS):
        testX.append([[x] for x in tX[i:i+TIMESTEPS]])

    testX = np.array(testX)
    testX = testX.astype('float32')

    # model
    regressor = skflow.TensorFlowEstimator(
        model_fn=lstm_model(TIMESTEPS, RNN_LAYERS, DENSE_LAYERS), n_classes=0,
        verbose=1,  steps=TRAINING_STEPS,
        optimizer='Adagrad',
        learning_rate=0.03,
        batch_size=BATCH_SIZE)

    regressor.fit(realX, realY, logdir=LOG_DIR)

    predict = regressor.predict(testX)

    day = [(datetime.date(2015, 9, 1) +
            datetime.timedelta(x)).strftime("%Y%m%d") for x in range(60)]

    res = pd.DataFrame()
    res['artist_id'] = [a1 for x in range(60)]
    res['plays'] = predict[1:]
    res['plays'] = res['plays'].astype('int')
    res['Ds'] = day

    result = pd.concat([result, res])
    result.to_csv('datas/lstm_predict.csv', index=False)
