# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def simulate(dt_start, dt_end, ls_symbols, ratio):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open','high','low','close','volume','actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    #for l in ls_symbols:
        

    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0,:]
    na_normalized_price_ratio = np.multiply(na_normalized_price, ratio)
    all_price_ratio = np.sum(na_normalized_price_ratio, axis=1)    
    
    """ calculate Volatility """
    vol = np.std(tsu.returnize0(all_price_ratio))    
    
    """ daily return """
    daily_ret = np.mean(tsu.returnize0(all_price_ratio))
    """ cumulative daily return"""
    cum_ret = 0
    sharpe = 0
    
    return vol, daily_ret, sharpe, cum_ret


dt_start = dt.datetime(2011,1,1)
dt_end = dt.datetime(2011,12,31)
        
vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ['AAPL','GLD','GOOG','XOM'], [0.4,0.4,0.0,0.2])

print vol, daily_ret