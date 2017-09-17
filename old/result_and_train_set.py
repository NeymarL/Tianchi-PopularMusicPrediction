# -*- coding:utf-8 -*-
#
# 把训练好的结果加入训练集，作为训练下一天的数据集
#

import numpy as np
import pandas as pd
import sys

day = int(sys.argv[1])

new = pd.read_csv('datas/preduced/data' + str(day) + '.csv')
old = pd.read_csv('datas/preduced/data.csv')

new = pd.concat([new, old])
new.to_csv('datas/preduced/data.csv', index=False)
