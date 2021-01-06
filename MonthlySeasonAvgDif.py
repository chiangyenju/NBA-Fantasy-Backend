# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 13:34:19 2020

@author: Yen Ju
"""

%reset -f
%clear

import pandas as pd
import numpy as np
import datetime as dt
from pandas import DataFrame

df = pd.read_pickle('fantasy_df.pkl')

#recent 3 years
d1 = dt.datetime(2016, 7, 31).strftime('%Y/%m')

#give month of gamedate
df['month'] = pd.to_datetime(df['GAME_DATE']).apply(lambda x: x.strftime('%Y/%m'))
df['month'] = df['month'].apply(lambda x: x if x > d1 else 0)


#add games played
df['games'] = 1

#season index
season_index = [['2010-2011',dt.datetime(2010,10,26),dt.datetime(2011,4,13)],
                ['2011-2012',dt.datetime(2011,12,25),dt.datetime(2012,6,26)],
                ['2012-2013',dt.datetime(2012,10,30),dt.datetime(2013,4,17)],
                ['2013-2014',dt.datetime(2013,10,26),dt.datetime(2014,4,13)],
                ['2014-2015',dt.datetime(2014,10,28),dt.datetime(2015,4,15)],
                ['2015-2016',dt.datetime(2015,10,28),dt.datetime(2016,4,13)],
                ['2016-2017',dt.datetime(2016,10,25),dt.datetime(2017,4,12)],
                ['2017-2018',dt.datetime(2017,10,18),dt.datetime(2018,4,12)],
                ['2018-2019',dt.datetime(2018,10,17),dt.datetime(2019,4,11)],
                ['2019-2020',dt.datetime(2019,10,26),dt.datetime(2020,8,15)]]
                # add new year index
                
df['game_date'] = df['GAME_DATE'].apply(lambda x: dt.datetime.strptime(x, "%b %d, %Y"))

#add season to each game 
def which_season(df):   
    element = df['game_date']
    for i in range(0, len(season_index)):
        if element >= season_index[i][1] and element <= season_index[i][2]:
            return season_index[i][0]
        else:
            i += 1
            
df['season'] = df.apply(which_season, axis = 1)

fp = df[['Player_ID', 'full_name', 'season', 'game_date', 'month', 'MIN', 'FGM', 'FGA', 'FG3M', 'FG3A',
         'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 
         'PTS', 'DD', 'TD', 'FP', ]]

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
monthly_avg = pd.pivot_table(fp, index = ['id', 'name', 'month', 'season'], values = stat_column, aggfunc = np.mean).sort_values('id', ascending = True)
monthly_avg = monthly_avg[stat_column]

#season average
season_avg = pd.pivot_table(fp, index = ['id', 'name', 'season'], values = stat_column, aggfunc = np.mean).sort_values('id', ascending = True)
season_avg = season_avg[stat_column]

