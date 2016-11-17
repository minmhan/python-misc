# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 13:17:16 2016

@author: minmhan
"""

import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

def find_events(ls_symbols, d_data):
    df_close = d_data['close']
    ts_market = df_close['SPY']
    
    print 'Finding Events'
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NaN
    
    ldt_timestamps = df_close.index
    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            """calculate returns of this timestamp"""
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i-1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i-1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) -1
            
            """ Event is found if symbol is down more than 3% while market is up more then 2%"""
            if f_symreturn_today <= -0.03 and f_marketreturn_today >= 0.02:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
            
    return df_events
    

if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1,1)
    dt_end = dt.datetime(2009,12,31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    
    ls_keys = ['open','high','low','close','volume','actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    for k in ls_keys:
        d_data[k] = d_data[k].fillna(method='ffill')
        d_data[k] = d_data[k].fillna(method='bfill')
        d_data[k] = d_data[k].fillna(1.0)
    
    df_events = find_events(ls_symbols, d_data)
    print df_events
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
    