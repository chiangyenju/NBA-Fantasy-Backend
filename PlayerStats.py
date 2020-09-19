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
player_id = player_active_list['id']

#stats
from nba_api.stats.endpoints import  playergamelog
from nba_api.stats.library.parameters import SeasonAll


        
        