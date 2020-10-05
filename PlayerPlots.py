# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:47:15 2020

@author: Andrew
"""

%reset -f
%clear


import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from sklearn.linear_model import LinearRegression


#plot style
plt.style.use('fivethirtyeight')

#clear plotting cache
plt.clf()


#import player data
from nba_api.stats.static import players
player_dict = players.get_players()

#input name
player1_name = 'Nikola Jokic'


#fetch player id
player1 = [player for player in player_dict if player['full_name'] == player1_name][0]
player1_id = player1['id']


#fetch game log from fantasy_df
plot_df = pd.read_pickle("./fantasy_df.pkl")
plot_df.dtypes


#set ids and dates, form new df in this py, containing daily fp and dates
dates_fp_columns = ['GAME_DATE','FP']
player1_fpoints = plot_df.loc[plot_df['Player_ID'] == player1_id][dates_fp_columns]
player1_fpoints.columns = ['date','fp']

#turn daily dates to monthly dates
player1_fpoints['month'] = pd.to_datetime(player1_fpoints['date']).dt.strftime('%Y/%m')


#combine daily data to month by fpoints mean and in order
player1_fpoints_mean  = player1_fpoints.groupby(['month'],as_index=False).mean().sort_values(by='month', ascending=True)

#combine daily data to month by fpoints sum and in order
player1_fpoints_sum = player1_fpoints.groupby(['month'],as_index=False).sum().sort_values(by='month', ascending=True)


#plot ax1 linear reg + scatter fp mean needed values
fpoints_forplot_mean = player1_fpoints_mean['fp']
player1_fpoints_mean['month'] = pd.to_datetime(player1_fpoints_mean['month'])

#plot ax2 plot fp sum
fpoints_forplot_sum = player1_fpoints_sum['fp']
player1_fpoints_sum['month'] = pd.to_datetime(player1_fpoints_sum['month'])


#turn date format into numerical date format
date_forplot_mean = player1_fpoints_mean['month'].map(dt.datetime.toordinal)
date_forplot_sum = player1_fpoints_sum['month'].map(dt.datetime.toordinal)


#ax1 linear regression
linereg = LinearRegression()

#reshape to autosize column as -1 (meaning to auto calculate), size 1 for row
date_forplot_mean = date_forplot_mean.values.reshape(-1,1)
linereg.fit(date_forplot_mean, fpoints_forplot_mean)
pred_fpoints_mean = linereg.predict(date_forplot_mean)


''' start drawing '''


fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2)

#ax1 linear reg + scatter
ax1.plot(date_forplot_mean,pred_fpoints_mean, color = 'red', lw = 0.5)
#change date format back for better reading in plot
date_forplot_mean = pd.to_datetime(player1_fpoints_mean['month'])
#fpoints_scatter
ax1.scatter(date_forplot_mean, fpoints_forplot_mean, label = player1_name, edgecolor='black',linewidth = 1, alpha = 0.75)


#ax2 fpoints sum bar chart
date_forplot_sum = pd.to_datetime(player1_fpoints_sum['month'])
ax2.bar(date_forplot_sum, fpoints_forplot_sum, width= 30, edgecolor = 'black')





# date_fmt = mdates.DateFormatter('%Y/%m')
# plt.gca().xaxis.set_major_formatter(date_fmt)
# plt.gcf().autofmt_xdate()


fig.show()
plt.close(1)


