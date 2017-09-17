# -*- coding:utf-8 -*-
#
# 预处理数据集
#
# 目标格式：
# user_id   song_id    Ds    plays    downs    favors
#


import numpy as np
import pandas as pd

all_data = pd.read_csv('datas/mars_tianchi_user_actions.csv')

plays = all_data[all_data.action_type == 1].groupby(
    ['user_id', 'song_id', 'Ds'])
plays = plays['action_type'].sum()
plays.to_csv('temp.csv')
plays = pd.read_csv('temp.csv', names=['user_id', 'song_id', 'Ds', 'plays'])

downs = all_data[all_data.action_type == 2].groupby(
    ['user_id', 'song_id', 'Ds'])
downs = downs['action_type'].size()
downs.to_csv('temp.csv')
downs = pd.read_csv('temp.csv', names=['user_id', 'song_id', 'Ds', 'downs'])

favors = all_data[all_data.action_type == 3].groupby(
    ['user_id', 'song_id', 'Ds'])
favors = favors['action_type'].size()
favors.to_csv('temp.csv')
favors = pd.read_csv(
    'temp.csv', names=['user_id', 'song_id', 'Ds', 'favors'])

data = pd.merge(plays, downs, how='outer', on=['user_id', 'song_id', 'Ds'])
data = pd.merge(data, favors, how='outer', on=['user_id', 'song_id', 'Ds'])
data = data.fillna(0)
data.to_csv('datas/train_data.csv', index=False)
