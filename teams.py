# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 18:22:29 2021

@author: Yen Ju
"""

%reset -f
%clear

import pandas as pd
import time
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerprofilev2
from nba_api.stats.endpoints import commonteamroster

teams_list = teams.get_teams()
players_list = players.get_active_players()

# for player in players_list:
#     player_id = player['id']
#     career_highs_list = playerprofilev2.PlayerProfileV2()
#     career_highs_list_df = career_highs_list.get_data_frames()[0]
#     all_player_career_highs_df = all_player_career_highs_list_df.append(career_highs_list_df)

# for team in teams_list:
#     team_id = team['id']
#     teams = commonteamroster.CommonTeamRoster(team_id).get_data_frames()
#     all_df = all_df.append(teams)
#     time.sleep(.100)

col = ['TeamID', 'PLAYER', 'POSITION', 'PLAYER_ID']
col2 = ['id', 'full_name', 'abbreviation']

all_df = pd.DataFrame()
all_df = all_df[col]
all_df = all_df.rename(columns = {'TeamID' : 'team_id', 'PLAYER' : 'player', 'POSITION' : 'position', "PLAYER_ID" : "player_id"})
                       
teams_df = pd.DataFrame(teams_list, columns = col2)
teams_df = teams_df.rename(columns = {'id': 'team_id', 'full_name':'team', 'abbreviation' : 'team_abb'})

merge_df = all_df.merge(teams_df, how = 'left', on=['team_id'])

