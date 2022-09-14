# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 23:23:18 2020

@author: Yen Ju
"""

%reset -f
%clear

import pandas as pd
import numpy as np
import datetime as dt


merge = pd.read_csv('season_fp.csv')

merge['fppd'] = merge.fp/merge.price
merge['price'] = merge['price'].fillna(0)

merge.to_csv('merge.csv', index = False)


