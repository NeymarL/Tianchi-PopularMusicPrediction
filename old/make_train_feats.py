# -*- coding:utf-8 -*-
# 特征工程
#
# 训练集选取预测日前30天内有过交互的us对
#
# 1、2-7、7-30、31-90天内 播放／下载／收藏 该歌曲次数
# 用户历史播放该种语言歌曲占全部播放的比例
# 用户历史播放该歌手音乐占全部播放的比例
# 用户历史播放该性别歌声的音乐占全部播放的比例
# 3天内播放该语言的数量大于 10, 为了预测近期突然喜欢上某种语言歌曲的用户
# 3天内播放该歌手的数量大于10，为了预测近期突然喜欢该歌手的用户
# 听这首歌的时间－这首歌的发布时间
#


import numpy as np
import pandas as pd
import sys

all_data = pd.read_csv('datas/train_data.csv')
new_data = pd.read_csv('datas/preduced/data.csv')
song_data = pd.read_csv('datas/mars_tianchi_songs.csv')

all_data = pd.concat([new_data, all_data])
all_data['Ds'] = all_data.Ds.astype('int')

big = pd.merge(all_data, song_data, on=['song_id'])

train_day = int(sys.argv[1])
b1_day = int(sys.argv[2])
b7_day = int(sys.argv[3])
b30_day = int(sys.argv[4])
b90_day = int(sys.argv[5])

temp = 'datas/temp.csv'

# 选取预测日前30天内有过交互的us对
train_us = all_data[
    (all_data.Ds >= b30_day) & (all_data.Ds <= train_day)]

us_pair = np.array(train_us.groupby(['user_id', 'song_id']).size().index)

print 'Make Train Feats!'
print 'train day : ', train_day, '\tb30 : ', b30_day, '\tlen : ', len(us_pair)

# 1、2-7、8-30、31-90天内 播放／下载／收藏 该歌曲次数
play_1 = all_data[all_data.Ds == b1_day].groupby(
    ['user_id', 'song_id'])['plays'].sum()
play_1 = play_1.reindex(us_pair, fill_value=0)
print b1_day, ' Max : ', play_1.max(), '\tMean : ', play_1.mean()
play_1.to_csv(temp)
play_1 = pd.read_csv(temp, names=['user_id', 'song_id', 'play_1'])

down_1 = all_data[all_data.Ds == b1_day].groupby(
    ['user_id', 'song_id'])['downs'].sum()
down_1 = down_1.reindex(us_pair, fill_value=0)
down_1.to_csv(temp)
down_1 = pd.read_csv(temp, names=['user_id', 'song_id', 'down_1'])

favor_1 = all_data[all_data.Ds == b1_day].groupby(
    ['user_id', 'song_id'])['favors'].sum()
favor_1 = favor_1.reindex(us_pair, fill_value=0)
favor_1.to_csv(temp)
favor_1 = pd.read_csv(temp, names=['user_id', 'song_id', 'favor_1'])

# 2 - 7
play_2_7 = all_data[(all_data.Ds < b1_day) &
                    (all_data.Ds >= b7_day)].groupby(
    ['user_id', 'song_id'])['plays'].sum()
play_2_7 = play_2_7.reindex(us_pair, fill_value=0)
play_2_7.to_csv(temp)
play_2_7 = pd.read_csv(temp, names=['user_id', 'song_id', 'play_2_7'])

down_2_7 = all_data[(all_data.Ds < b1_day) &
                    (all_data.Ds >= b7_day)].groupby(
    ['user_id', 'song_id'])['downs'].sum()
down_2_7 = down_2_7.reindex(us_pair, fill_value=0)
down_2_7.to_csv(temp)
down_2_7 = pd.read_csv(temp, names=['user_id', 'song_id', 'down_2_7'])

favor_2_7 = all_data[(all_data.Ds < b1_day) &
                     (all_data.Ds >= b7_day)].groupby(
    ['user_id', 'song_id'])['favors'].sum()
favor_2_7 = favor_2_7.reindex(us_pair, fill_value=0)
favor_2_7.to_csv(temp)
favor_2_7 = pd.read_csv(temp, names=['user_id', 'song_id', 'favor_2_7'])

# 8 - 30
play_8_30 = all_data[(all_data.Ds < b7_day) &
                     (all_data.Ds >= b30_day)].groupby(
    ['user_id', 'song_id'])['plays'].sum()
play_8_30 = play_8_30.reindex(us_pair, fill_value=0)
play_8_30.to_csv(temp)
play_8_30 = pd.read_csv(temp, names=['user_id', 'song_id', 'play_8_30'])

down_8_30 = all_data[(all_data.Ds < b7_day) &
                     (all_data.Ds >= b30_day)].groupby(
    ['user_id', 'song_id'])['downs'].size()
down_8_30 = down_8_30.reindex(us_pair, fill_value=0)
down_8_30.to_csv(temp)
down_8_30 = pd.read_csv(temp, names=['user_id', 'song_id', 'down_8_30'])

favor_8_30 = all_data[(all_data.Ds < b7_day) &
                      (all_data.Ds >= b30_day)].groupby(
    ['user_id', 'song_id'])['favors'].size()
favor_8_30 = favor_8_30.reindex(us_pair, fill_value=0)
favor_8_30.to_csv(temp)
favor_8_30 = pd.read_csv(temp, names=['user_id', 'song_id', 'favor_8_30'])

# 31 - 90
play_31_90 = all_data[(all_data.Ds < b30_day) &
                      (all_data.Ds >= b90_day)].groupby(
    ['user_id', 'song_id'])['plays'].sum()
play_31_90 = play_31_90.reindex(us_pair, fill_value=0)

play_31_90.to_csv(temp)
play_31_90 = pd.read_csv(temp, names=['user_id', 'song_id', 'play_31_90'])

down_31_90 = all_data[(all_data.Ds < b30_day) &
                      (all_data.Ds >= b90_day)].groupby(
    ['user_id', 'song_id'])['downs'].size()
down_31_90 = down_31_90.reindex(us_pair, fill_value=0)
down_31_90.to_csv(temp)
down_31_90 = pd.read_csv(temp, names=['user_id', 'song_id', 'down_31_90'])

favor_31_90 = all_data[(all_data.Ds < b30_day) &
                       (all_data.Ds >= b90_day)].groupby(
    ['user_id', 'song_id'])['favors'].size()
favor_31_90 = favor_31_90.reindex(us_pair, fill_value=0)
favor_31_90.to_csv(temp)
favor_31_90 = pd.read_csv(temp, names=['user_id', 'song_id', 'favor_31_90'])


# 用户历史播放该种语言歌曲占全部播放的比例

lang_ev = big.groupby(['user_id', 'language'])['plays'].sum()
lang_al = big.groupby(['user_id'])['plays'].sum()
lang_ev.to_csv(temp)
lang_ev = pd.read_csv(temp, names=['user_id', 'language', 'lplays'])
lang_al.to_csv(temp)
lang_al = pd.read_csv(temp, names=['user_id', 'aplays'])

lang = pd.merge(lang_al, lang_ev, on=['user_id'])
lang['lang'] = lang['lplays'] / lang['aplays']
lang = lang.fillna(0)

lang = pd.merge(big, lang, on=['user_id', 'language'])

lang_feats = pd.DataFrame()
lang_feats['user_id'] = lang['user_id']
lang_feats['song_id'] = lang['song_id']
lang_feats['lang'] = lang['lang']


# 用户历史播放该歌手音乐占全部播放的比例

art = big.groupby(['user_id', 'artist_id'])['plays'].sum()
art.to_csv(temp)
art = pd.read_csv(temp, names=['user_id', 'artist_id', 'plays'])

artist = pd.merge(art, lang_al, on=['user_id'])
artist['art'] = artist['plays'] / artist['aplays']
artist = artist.fillna(0)

artist = pd.merge(big, artist, on=['user_id', 'artist_id'])

art_feats = pd.DataFrame()
art_feats['user_id'] = artist['user_id']
art_feats['song_id'] = artist['song_id']
art_feats['art'] = artist['art']


# 用户历史播放该性别歌声的音乐占全部播放的比例


# 融合特征

feats_1 = pd.merge(play_1, down_1, how='outer', on=['user_id', 'song_id'])
feats_1 = pd.merge(favor_1, feats_1, how='outer', on=['user_id', 'song_id'])

feats_2_7 = pd.merge(
    play_2_7, down_2_7, how='outer', on=['user_id', 'song_id'])
feats_2_7 = pd.merge(
    favor_2_7, feats_2_7, how='outer', on=['user_id', 'song_id'])

feats_8_30 = pd.merge(
    play_8_30, down_8_30, how='outer', on=['user_id', 'song_id'])
feats_8_30 = pd.merge(
    favor_8_30, feats_8_30, how='outer', on=['user_id', 'song_id'])

feats_31_90 = pd.merge(
    play_31_90, down_31_90, how='outer', on=['user_id', 'song_id'])
feats_31_90 = pd.merge(
    favor_31_90, feats_31_90, how='outer', on=['user_id', 'song_id'])

feats1 = pd.merge(feats_1, feats_2_7, how='outer', on=['user_id', 'song_id'])
feats2 = pd.merge(
    feats_8_30, feats_31_90, how='outer', on=['user_id', 'song_id'])

feats = pd.merge(feats1, feats2, how='outer', on=['user_id', 'song_id'])

feats3 = pd.merge(art_feats, lang_feats, on=['user_id', 'song_id'])

feats = pd.merge(feats, feats3, on=['user_id', 'song_id'])
feats = feats.fillna(0)


feats.to_csv('datas/feats/feats' + str(train_day) + '.csv', index=False)
