# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 10:38:31 2020

@author: Yen Ju
"""

# At least 33000 to win.

# Pick 12 players.

# Lowest cost.

# 500 dollar budget

%reset -f
%clear

import pandas as pd
import numpy as np
import datetime as dt
from pandas import DataFrame

from collections import Counter
from itertools import chain


merge = pd.read_csv('merge.csv')

current_season = '2020-2021'
minimum_fp = 2000

merge = merge[merge.season == current_season]

merge['rank'] = merge['fp'].rank(ascending = False)
merge = merge[merge.fp >= minimum_fp]


# merge['fp'] = merge['fp'].apply(lambda x: x if x >= 2000 else 0)

# column_names = ['name', 'fp', 'price']

budget = 500
winp = 38000
draftc = 12


team = merge.sample(draftc)

team_list = []
i = 0
while i < 100:
    while (team['price'].sum() >= budget) | (team['fp'].sum() <= winp):
        team = merge.sample(draftc)
    team['team_cnt'] = i
    team_list.append(team)
    team = merge.sample(draftc)
    i = i+1

# print(team_list)

df = pd.concat(team_list)

df['freq'] = df.groupby('name')['name'].transform("count")
df = df.drop_duplicates(subset = ["name"])

team
team.fp.sum()
team.price.sum()




