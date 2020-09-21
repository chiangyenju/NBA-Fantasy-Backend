# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 08:15:08 2020

@author: Andrew
"""

%reset -f
%clear

import pandas as pd

from nba_api.stats.static import players
player_list = players.get_players()


player_active_list = [player for player in player_list if player['is_active'] == True]

# stats
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

all_player_game_log_df = pd.DataFrame()

# loop career stats for all players
for player in player_active_list:
    player_id = player['id']
    player_game_log = playergamelog.PlayerGameLog(player_id, season = SeasonAll.all)
    player_game_log_df = player_game_log.get_data_frames()[0]
    all_player_game_log_df = all_player_game_log_df.append(player_game_log_df)
    

# player name with id
player_active_list_df = pd.DataFrame(player_active_list, columns={'id','full_name'})
player_active_list_df = player_active_list_df.rename(columns={"id":"Player_ID"})

# collect useful columns
useful_columns = ['Player_ID','MIN','FGM','FGA','FG3M','FG3A','FTM','FTA','OREB','DREB','AST','STL','BLK','TOV','PTS']   
fantasy_df = all_player_game_log_df[useful_columns]
del fantasy_df['full_name']
fantasy_df = pd.merge(fantasy_df, player_active_list_df, on = 'Player_ID', how = 'left',)

# calculate fantasy point




