# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 17:43:04 2016

@author: minmhan
"""

import pandas as pd
import pandas.io.data
import numpy as np
import datetime
import matplotlib.pyplot as plt

def getStockData(ticker, start, end):
    data = pd.io.data.DataReader(ticker, "yahoo",start,end)
    data.rename(columns={'Adj Close':'AdjClose'}, inplace=True)
    data.insert(0, "Ticker", ticker)
    return data
    
    
def getDataForMultipleStocks(tickers, start, end):
    stocks = dict()
    for ticker in tickers:
        s = getStockData(ticker, start, end)
        stocks[ticker] = s
        
    return stocks

def pivotTickersToColumns(raw,col):
    items = []
    for k in raw:
        data = raw[k]
        subset = data[["Ticker",col]]
        items.append(subset)
        
    combined = pd.concat(items)
    ri = combined.reset_index()
    return ri.pivot("Date", "Ticker", col)
    
    
start = datetime.datetime(2012,1,1)
end = datetime.datetime(2014,12,31)
raw = getDataForMultipleStocks(["MSFT","AAPL","GE","IBM","AA","DAL","UAL","PEP","KO"], start, end)
close_px = pivotTickersToColumns(raw, 'AdjClose')
#print(close_px[:5])
#close_px['AAPL'].plot()
#close_px[['MSFT','AAPL']].plot()
volumes = pivotTickersToColumns(raw,"Volume")
msftV = volumes[["MSFT"]]
#plt.bar(msftV.index, msftV["MSFT"])
#plt.gcf().set_size_inches(15,8)
##Daily percentage change
daily_pc = (close_px / close_px.shift(1)) - 1
#print(daily_pc[:5])
## Daily cumulative return
daily_cr = (1 + daily_pc).cumprod()
print(daily_cr[:5])
