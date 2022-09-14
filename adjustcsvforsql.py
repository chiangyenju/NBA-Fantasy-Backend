# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 12:03:55 2021

@author: Yen Ju
"""

%reset -f
%clear

import pandas as pd
import numpy as np
from pandas import DataFrame
from nba_api.stats.static import players

#import active players
player_list = players.get_active_players()
player_list_df = pd.DataFrame(player_list)
player_list_df_filter = player_list_df[['id', 'full_name']]
player_list_df_filter = player_list_df_filter.rename(columns = {'full_name':'name'})

#import data with newest team roster
player_index = pd.read_csv('player_index.csv')
player_index['name'] = player_index['PLAYER_FIRST_NAME'] + " " + player_index['PLAYER_LAST_NAME']
player_index['team'] = player_index['TEAM_CITY'] + " " + player_index['TEAM_NAME']
player_index_filter = player_index[['PERSON_ID','name', 'TEAM_ID', 'team', 'POSITION']]
player_index_filter = player_index_filter.rename(columns = {'PERSON_ID' : 'id','TEAM_ID' : 'team_id', 'POSITION' : 'position' })

#import fantasy points data
season_fp = pd.read_csv('season_fp.csv')
season_fp = season_fp.rename(columns = {'fp': 'points', 'pergfp': 'average'})

#set recent 3 years
season_3y = ['2021-2022',
             '2020-2021',
             '2019-2020']

#filter recent 3 years
season_fp = season_fp[(season_fp['season'] == season_3y[0]) | (season_fp['season'] == season_3y[1]) | (season_fp['season'] == season_3y[2])]


#set index to name and season
season_fp.set_index(['name', 'season'], drop=True, inplace=True)

x = season_fp.unstack(1)

#set column order
column_order = [('points',season_3y[0]),('points',season_3y[1]),('points',season_3y[2]),
                ('average',season_3y[0]),('average',season_3y[1]),('average',season_3y[2]),
                ('games',season_3y[0]),('games',season_3y[1]),('games',season_3y[2]),
                ('price',season_3y[0]),('price',season_3y[1]),('price',season_3y[2]),
                ]
unstack_ex = x.reindex(columns=column_order)
unstack_ex.fillna(0, inplace=True)


#to csv
unstack_ex.to_csv('3y_unstacked.csv', index = True)

y = pd.read_csv('3y_unstacked.csv')
y = y.iloc[2:]

y_column = ['name','y1_points','y2_points','y3_points',
                 'y1_average','y2_average','y3_average',
                 'y1_games','y2_games','y3_games',
                 'y1_price','y2_price','y3_price',]

numeric_column = ['y1_points','y2_points','y3_points',
                 'y1_average','y2_average','y3_average',
                 'y1_games','y2_games','y3_games',
                 'y1_price','y2_price','y3_price',]

y.columns = y_column

#turn string to float
y[numeric_column] = y[numeric_column].applymap(np.float64)

#merge season_fp and player_list for player index, for link to current team
z = y.merge(player_list_df_filter, how='left', on=['name'])
z = z.merge(player_index_filter, how = 'left', on=['name', 'id'])


z['y1_rank'] = z['y1_points'].rank(method = 'dense', ascending=False)
z['y2_rank'] = z['y2_points'].rank(method = 'dense', ascending=False)
z['y3_rank'] = z['y3_points'].rank(method = 'dense', ascending=False)


z_column = ['id','name', 'team', 'position',
            'y1_points', 'y1_rank',
            'y2_points', 'y2_rank',
            'y3_points', 'y3_rank',
            'y1_average','y2_average','y3_average',
            'y1_games','y2_games','y3_games',
            'y1_price','y2_price','y3_price',]


int_column = ['y1_rank','y2_rank','y3_rank',
              'y1_games','y2_games','y3_games',
              'y1_price','y2_price','y3_price',]


z = z[z_column]
z[int_column] = z[int_column].applymap(np.int64)
z['id'] = z['id'].astype(str)
z['id'].dtypes
z['team'].fillna('None', inplace=True)
z['position'].fillna('None', inplace=True)

# for player_id in 
# 'https://cdn.nba.com/headshots/nba/latest/260x190/'+player_id+'.png'

z.to_csv('fantasy_tableforjson.csv', index=False)
