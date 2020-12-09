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

merge = pd.read_csv('merge.csv')



#minimum to reach 33000, then add best value players

merge.fp.sum()

# column_names = ['name', 'fp', 'price']

budget = 500
winp = 38000
draftc = 12

team = merge.sample(draftc)

 
while (team['Price'].sum() >= budget) | (team['fp'].sum() <= winp):
    team = merge.sample(draftc)

team
team.fp.sum()
team.Price.sum()




