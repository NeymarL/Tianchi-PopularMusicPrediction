# -*- coding:utf-8 -*-
# 训练数据
#
# Decision Tree Regression


import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import sys

train_day = int(sys.argv[1])
label_day = train_day
predict_day = int(sys.argv[2])

new_data_set_filename = 'datas/preduced/data' + str(predict_day) + '.csv'
predict_result_filename = 'datas/raw_train_result/plays' + \
    str(predict_day) + '.csv'


# train data
feats = pd.read_csv('datas/feats/feats' + str(train_day) + '.csv')
#feats['user_id'] = [int(x, 16) for x in feats['user_id']]
feats['song_id'] = [int(x, 16) for x in feats['song_id']]

#umin = feats['user_id'].min()
smin = feats['song_id'].min()

#feats['user_id'] = feats['user_id'] * 1.0 / umin
feats['song_id'] = feats['song_id'] * 1.0 / smin
feats.pop('user_id')

X = []
n = len(feats)
for i in xrange(n):
    X.append(feats.ix[i].tolist())
X = np.array(X)

# labels
labels = pd.read_csv('datas/labels/label' + str(label_day) + '.csv')

Y = [0]
index = labels.columns[0]
Y.extend(labels[index].tolist())

# predict data
predict_feats = pd.read_csv('datas/feats/feats' + str(predict_day) + '.csv')
bak = predict_feats.copy()
#predict_feats['user_id'] = [int(x, 16) for x in predict_feats['user_id']]
predict_feats['song_id'] = [int(x, 16) for x in predict_feats['song_id']]

#predict_feats['user_id'] = predict_feats['user_id'] * 1.0 / umin
predict_feats['song_id'] = predict_feats['song_id'] * 1.0 / smin

predict_feats.pop('user_id')

pX = []
n = len(predict_feats)
for i in xrange(n):
    pX.append(predict_feats.ix[i].tolist())

pX = np.array(pX)

# model
regr = DecisionTreeRegressor(max_depth=15)
# train
regr.fit(X, Y)

# predict
predy = regr.predict(pX)

bak['pred'] = predy

# make song_id and predict result together
pred_plays = bak.groupby(['song_id'])['pred'].sum()

print 'Predict ', predict_day, ' Max : ',\
    bak['pred'].max(), '\tMean : ', bak['pred'].mean()

pred_plays.to_csv(predict_result_filename)

# 生成新的训练数据
new_train_set = pd.DataFrame()
new_train_set['user_id'] = bak['user_id']
new_train_set['song_id'] = bak['song_id']
new_train_set['Ds'] = [str(predict_day) for x in range(n)]
#new_train_set['gmt_create'] = np.zeros(n, dtype='int')
new_train_set['plays'] = predy
new_train_set['downs'] = np.zeros(n, dtype='int')    # 可以改进，模拟一个随机分布
new_train_set['favors'] = np.zeros(n, dtype='int')
new_train_set = new_train_set[new_train_set.plays > 0.1]
new_train_set.to_csv(new_data_set_filename, index=False)
