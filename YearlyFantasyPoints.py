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

season_index = [['2010-2011',dt.datetime(2010,10,26),dt.datetime(2011,4,13)],
                ['2011-2012',dt.datetime(2010,12,25),dt.datetime(2011,6,26)],
                ['2012-2013',dt.datetime(2010,10,30),dt.datetime(2011,4,17)],
                ['2013-2014',dt.datetime(2010,10,26),dt.datetime(2011,4,13)],
                ['2014-2015',dt.datetime(2010,10,28),dt.datetime(2011,4,15)],
                ['2015-2016',dt.datetime(2010,10,28),dt.datetime(2011,4,13)],
                ['2016-2017',dt.datetime(2010,10,25),dt.datetime(2011,4,12)],
                ['2017-2018',dt.datetime(2010,10,18),dt.datetime(2011,4,12)],
                ['2018-2019',dt.datetime(2010,10,17),dt.datetime(2011,4,11)],
                ['2019-2020',dt.datetime(2010,10,26),dt.datetime(2011,8,15)]]
                # add new year index
                
                
season_df = pd.DataFrame(season_index, columns = ['Season', 'Start', 'End'])

df['month'] = pd.to_datetime(df['GAME_DATE']).apply(lambda x: x.strftime('%Y/%m'))
