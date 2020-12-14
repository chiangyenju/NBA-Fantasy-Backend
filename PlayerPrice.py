# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 23:23:18 2020

@author: Yen Ju
"""

%reset -f
%clear

import pandas as pd
import numpy as np
import datetime as dt

df = pd.read_csv('draft_2019_2020.csv')
yearly_fp = pd.read_csv('season_fp.csv')

current_season = '2019-2020'

df['season'] = current_season
df = df.rename(columns = {'Player':'name'})

merge = df.merge(yearly_fp, how='left', on=['name', 'season'])

merge['fppd'] = merge.fp/merge.Price

merge.to_csv('merge.csv', index = False)



# df_fp_columns = ['Player','Price']
# player1_fpoints = df.loc[df['Player'] == yearly_fp['name']][df_fp_columns]
# player1_fpoints.columns = ['date','fp']

