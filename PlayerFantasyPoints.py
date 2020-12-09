# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:41:13 2020

@author: Yen Ju
"""

# all players recent 3 years monthly average


%reset -f
%clear

import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
from pandas import DataFrame

# from nba_api.stats.static import players

# player_dict = players.get_active_players()
# player_df = DataFrame(player_dict, columns = ['id', 'full_name'])
# player_df = player_df.rename(columns = {"full_name": "name"})


df = pd.read_pickle('fantasy_df.pkl')

d1 = dt.datetime(2016, 7, 31).strftime('%Y/%m')

df['month'] = pd.to_datetime(df['GAME_DATE']).apply(lambda x: x.strftime('%Y/%m'))
df['month'] = df['month'].apply(lambda x: x if x > d1 else 0)

fp = df[['Player_ID', 'full_name', 'month', 'MIN', 'FGM', 'FGA', 'FG3M', 'FG3A',
         'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 
         'PTS', 'DD', 'TD', 'FP']]

#filter recent 3 years
fp = fp[fp['month'] != 0]

#rename and lower case columns
fp = fp.rename(columns = {'Player_ID': 'id', 'full_name': 'name'})
fp.columns = fp.columns.str.lower()

#change data type to float / int
fp['min'] = pd.to_numeric(fp['min'], errors = 'coerce')
fp['fgm'] = pd.to_numeric(fp['fgm'], errors = 'coerce')
fp['fga'] = pd.to_numeric(fp['fga'], errors = 'coerce')
fp['fg3m'] = pd.to_numeric(fp['fg3m'], errors = 'coerce')
fp['fg3a'] = pd.to_numeric(fp['fg3a'], errors = 'coerce')
fp['ftm'] = pd.to_numeric(fp['ftm'], errors = 'coerce')
fp['fta'] = pd.to_numeric(fp['fta'], errors = 'coerce')
fp['oreb'] = pd.to_numeric(fp['oreb'], errors = 'coerce')
fp['dreb'] = pd.to_numeric(fp['dreb'], errors = 'coerce')
fp['ast'] = pd.to_numeric(fp['ast'], errors = 'coerce')
fp['stl'] = pd.to_numeric(fp['stl'], errors = 'coerce')
fp['blk'] = pd.to_numeric(fp['blk'], errors = 'coerce')
fp['tov'] = pd.to_numeric(fp['tov'], errors = 'coerce')
fp['pts'] = pd.to_numeric(fp['pts'], errors = 'coerce')
fp['dd'] = pd.to_numeric(fp['dd'], errors = 'coerce')
fp['td'] = pd.to_numeric(fp['td'], errors = 'coerce')
fp['fp'] = pd.to_numeric(fp['fp'], errors = 'coerce')
fp['games'] = 1

#get column for pivot table
stat_column = ['min', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb', 'ast', 'stl', 'blk', 'tov', 'pts', 'dd', 'td', 'fp']


print(fp.dtypes)

#get each month average stats
avg_pivot = pd.pivot_table(fp, index = ['id', 'name', 'month'], values = stat_column, aggfunc = np.mean).sort_values('id', ascending = True)

#sort pivot order
avg_pivot = avg_pivot.reindex(stat_column, axis=1)

#add total games played that month
avg_pivot['games'] = pd.pivot_table(fp, index = ['id', 'name', 'month'], values = 'games', aggfunc = np.sum).sort_values('id', ascending = True)

avg_pivot.to_csv('fp_3y_monthly.csv')
