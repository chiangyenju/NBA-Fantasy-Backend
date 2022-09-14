# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 11:26:07 2020

@author: Yen Ju
"""

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

#import data
df = pd.read_pickle('fantasy_df.pkl')

#add game month
df['month'] = pd.to_datetime(df['GAME_DATE']).apply(lambda x: x.strftime('%Y/%m'))

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
                ['2018-2019',dt.datetime(2018,10,16),dt.datetime(2019,4,10)],
                ['2019-2020',dt.datetime(2019,10,22),dt.datetime(2020,8,14)],
                ['2020-2021',dt.datetime(2020,12,22),dt.datetime(2021,5,16)]]
                # add new year index
      
#season index to dataframe      
# season_df = pd.DataFrame(season_index, columns = ['Season', 'Start', 'End'])
          
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

# rename collumns
df = df.rename(columns = {'Player_ID': 'id', 'full_name': 'name', 'FP':'fp'})

#sum fantasy points and games played by season
season_fp = pd.pivot_table(df, index = ['name', 'season'], values = ['fp', 'games'], aggfunc = np.sum).sort_values('name', ascending = True)


#per game fp
season_fp['pergfp'] = season_fp.fp / season_fp.games
season_fp['pergfp'] = season_fp['pergfp'].round(1)

#import yearly auction player price
price_csv_y1 = pd.read_csv('draft_2020_2021_1.csv')
price_csv_y2 = pd.read_csv('draft_2019_2020.csv')
price_csv_y3 = pd.read_csv('draft_2018_2019.csv')

#merge vlookup price with season fp
season_y1 = '2020-2021'
season_y2 = '2019-2020'
season_y3 = '2018-2019'

price_csv_y1['season'] = season_y1
price_csv_y2['season'] = season_y2
price_csv_y3['season'] = season_y3

price_csv_y1 = price_csv_y1.rename(columns = {'Player': 'name', 'Price': 'price'})
price_csv_y2 = price_csv_y2.rename(columns = {'Player': 'name', 'Price': 'price'})
price_csv_y3 = price_csv_y3.rename(columns = {'Player': 'name', 'Price': 'price'})

price_csv = pd.concat([price_csv_y1,price_csv_y2,price_csv_y3])

season_fp = season_fp.merge(price_csv, how='left', on=['name', 'season'])


#fantasy points per dollar
season_fp['fppd'] = season_fp.fp / season_fp.price
season_fp['fppd'] = season_fp['fppd'].round(1)

season_fp.to_csv('season_fp.csv', index = False)

df.to_csv('fantasy_raw.csv', index = False)


