# -*- coding:utf-8 -*-
#
# 生成某一天的label
#

import numpy as np
import pandas as pd
import sys

all_data = pd.read_csv('datas/train_data.csv')
new_data = pd.read_csv('datas/preduced/data.csv')

all_data = pd.concat([new_data, all_data])

train_day = int(sys.argv[1])
label_day = train_day
b30_day = int(sys.argv[2])

train_us = all_data[
    (all_data.Ds >= b30_day) & (all_data.Ds <= train_day)]

us_pair = np.array(train_us.groupby(['user_id', 'song_id']).size().index)

print 'Make Label!!'
print 'label day : ', train_day, '\tb30 : ', b30_day, '\tlen : ', len(us_pair)

# get labels
t_plays = all_data[(all_data.Ds == label_day)
                   ].groupby(['user_id', 'song_id'])['plays'].sum()

t_plays = t_plays.reindex(us_pair, fill_value=0)
#t_plays = t_plays.fillna(0)
t_plays.to_csv('datas/labels/label' + str(label_day) + '.csv', index=False)

print 'Max : ', t_plays.max(), '\tMean : ', t_plays.mean()
