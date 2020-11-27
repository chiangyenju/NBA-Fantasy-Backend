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


df = pd.read_pickle('fantasy_df.pkl')

df['month'] = pd.to_datetime(df['GAME_DATE']).apply(lambda x: x.strftime('%Y/%m'))

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
      
      
season_df = pd.DataFrame(season_index, columns = ['Season', 'Start', 'End'])
          
game_date = df['GAME_DATE'].apply(lambda x: dt.datetime.strptime(x, "%b %d, %Y"))
    # dt.datetime.strptime(game_date, "%b %d, %Y")

                
def which_season(df):   
    for element in game_date:
    
        for i in range(0,len(season_index)):
            if i == 10:
                i = 0
            elif element >= season_index[i][1] and element <= season_index[i][2]:
                season = season_index[i][0]
                return season
            else:
                i += 1

df['season'] = df.apply(which_season, axis = 1)



for element in game_date:
        if i == len(season_index):
            i = 0
        elif element >= season_index[i][1] and element <= season_index[i][2]:
            df['season'] = season_index[i][0] 
        else:
            i += 1
