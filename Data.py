# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 00:28:37 2020

@author: Andrew
"""


import pandas as pd

#id from api
from nba_api.stats.static import players
player_dict = players.get_players()



bron = [player for player in player_dict if player['full_name'] == 'LeBron James'][0]
bron_id = bron['id']

players.find_players_by_last_name('^(james|love)$')

from nba_api.stats.static import teams
team_dict = teams.get_teams()

gsw = [team for team in team_dict if team['full_name'] == 'Golden State Warriors'][0]
gsw_id = gsw['id']

#stats from api
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

bron_gamelog = playergamelog.PlayerGameLog(bron_id)
bron_gamelog_df = bron_gamelog.get_data_frames()[0]

bron_gamelog_all = playergamelog.PlayerGameLog(bron_id, season = SeasonAll.all)
bron_gamelog_all_df = bron_gamelog_all.get_data_frames()[0]

#teams log
from nba_api.stats.endpoints import leaguegamefinder
gsw_team_log = leaguegamefinder.LeagueGameFinder(team_id_nullable = gsw_id).get_data_frames()[0]


#player career stats
from nba_api.stats.endpoints import playercareerstats
playercareerstats_dict = playercareerstats.PlayerCareerStats()

bron_careerstats = [player for player in playercareerstats_dict if player]