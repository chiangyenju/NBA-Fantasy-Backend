# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 08:15:08 2020

@author: Andrew
"""

%reset -f
%clear

import pandas as pd
import time



# parse data
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
    time.sleep(.300)
    


# player name with id
player_active_list_df = pd.DataFrame(player_active_list, columns={'id','full_name'})
player_active_list_df = player_active_list_df.rename(columns={"id":"Player_ID"})



# collect useful columns
def form_fantasy_df():
    useful_columns = ['Player_ID','GAME_DATE','MATCHUP','MIN', \
                      'FGM','FGA','FG3M','FG3A','FTM','FTA','OREB','DREB','AST','STL','BLK','TOV','PTS']   
    fantasy_df = all_player_game_log_df[useful_columns]
    fantasy_df = pd.merge(fantasy_df, player_active_list_df, on = 'Player_ID', how = 'left')
    columns_order = ['Player_ID','full_name','GAME_DATE','MATCHUP','MIN', \
                      'FGM','FGA','FG3M','FG3A','FTM','FTA','OREB','DREB','AST','STL','BLK','TOV','PTS']
    fantasy_df = fantasy_df.reindex(columns=columns_order)
    return fantasy_df

fantasy_df = form_fantasy_df()


# detect which stats exceed 10, then create DD column
def double_double(fantasy_df):  
    dd_reb = fantasy_df['OREB'] + fantasy_df['DREB']
    dd_ast = fantasy_df['AST']
    dd_stl = fantasy_df['STL']
    dd_blk = fantasy_df['BLK']
    dd_pts = fantasy_df['PTS']
    dd_stats = [dd_reb, dd_ast, dd_stl, dd_blk, dd_pts]
    dd_stats_10 = [element for element in dd_stats if (element >= 10)]
    dd_stats_10_count = len(dd_stats_10)
    if (dd_stats_10_count >= 2):
        return 1
    else:
        return 0
    
fantasy_df['DD'] = fantasy_df.apply(double_double,axis = 1)


# detect which stats exceed 10, then create TD column
def triple_double(fantasy_df):  
    dd_reb = fantasy_df['OREB'] + fantasy_df['DREB']
    dd_ast = fantasy_df['AST']
    dd_stl = fantasy_df['STL']
    dd_blk = fantasy_df['BLK']
    dd_pts = fantasy_df['PTS']
    dd_stats = [dd_reb, dd_ast, dd_stl, dd_blk, dd_pts]
    dd_stats_10 = [element for element in dd_stats if (element >= 10)]
    dd_stats_10_count = len(dd_stats_10)
    if (dd_stats_10_count >= 3):
        return 1
    else:
        return 0
    
fantasy_df['TD'] = fantasy_df.apply(triple_double,axis = 1)



### check if adding td works properly
# def detect_first_td():
#     res = next(x for x, val in enumerate(fantasy_df["TD"]) if val ==1)
#     print(res)
    
#     # check how many tds    
#     td_check = [td for td in fantasy_df['TD'] if (td == 1)]
#     td_count = len(td_check)
#     print(td_count)




### add name to df, need to delete past data first
# try:
#     del fantasy_df['full_name']
# except Exception:
#     pass




def fantasy_points(fantasy_df):
    
    
    # calculate fantasy point
    fpoints_fgm = 3
    fpoints_fga = -0.5
    fpoints_fg3m = 2
    fpoints_fg3a = -0.5
    fpoints_ftm = 1.5
    fpoints_fta = -0.5
    fpoints_oreb = 2
    fpoints_dreb = 1
    fpoints_ast = 2.5
    fpoints_stl = 3
    fpoints_blk = 4
    fpoints_tov = -2
    fpoints_pts = 0.5
    fpoints_dd = 10
    fpoints_td = 10
    # try:
    #     del fantasy_df
    # except Exception:
    #     pass

    fantasy_df['FGM'] *= fpoints_fgm
    fantasy_df['FGA'] *= fpoints_fga
    fantasy_df['FG3M'] *= fpoints_fg3m
    fantasy_df['FG3A'] *= fpoints_fg3a
    fantasy_df['FTM'] *= fpoints_ftm
    fantasy_df['FTA'] *= fpoints_fta
    fantasy_df['OREB'] *= fpoints_oreb
    fantasy_df['DREB'] *= fpoints_dreb
    fantasy_df['AST'] *= fpoints_ast
    fantasy_df['STL'] *= fpoints_stl
    fantasy_df['BLK'] *= fpoints_blk
    fantasy_df['TOV'] *= fpoints_tov
    fantasy_df['PTS'] *= fpoints_pts
    fantasy_df['DD'] *= fpoints_dd
    fantasy_df['TD'] *= fpoints_td


    fp = fantasy_df.loc[['FGM','FGA','FG3M','FG3A','FTM','FTA','OREB','DREB','AST','STL','BLK','TOV','PTS','DD','TD']].sum()
    
    return fp

fantasy_df['FP'] = fantasy_df.apply(fantasy_points,axis = 1)

fantasy_df.to_pickle("./fantasy_df.pkl")
