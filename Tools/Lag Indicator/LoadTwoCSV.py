#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 13:51:55 2017
@author: rweegenaar

This script reads in two CSVs, equalizes the dates and times and plots candlestick charts.
Place 2 CSVs in folder. Rest is automatic
"""
import glob
import pandas as pd

#Read CSVs
file_names = glob.glob('*.csv')
name1 = file_names[0]
name2 = file_names[1]

#dataframe1
df1 = pd.read_csv(name1,

                 header=None,names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
#dataframe2
df2 = pd.read_csv(name2,
                 header=None,names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

###### Equalize CSV DataFrames ######

#test whether frequency is 1D or higher
#1D times in CSV may not be equal
test_freq = df1['time'][1] == df1['time'][2]

if test_freq == True:
            df1['DateTime'] = pd.to_datetime(df1['date'])
            df2['DateTime'] = pd.to_datetime(df2['date'])

else:
            df1['DateTime'] = pd.to_datetime(df1['date'] + " " + df1['time'])
            df2['DateTime'] = pd.to_datetime(df2['date'] + " " + df2['time'])

A1 = df1['DateTime']
B1 = df2['DateTime']

# find common dates or date_times
D12 = list(set(df1['DateTime']) & set(df2['DateTime']))
D12.sort()
D12_date = pd.to_datetime(D12) 


k = 0
m = len(D12)

while k < m:

    if A1[k] > B1[k]:
        B1.pop(k)
        B1 = B1.reset_index(drop=True)
        df2 = df2.drop(df2.index[k])
        df2 = df2.reset_index(drop=True)

        
    elif A1[k] < B1[k]:
        A1.pop(k)
        A1 = A1.reset_index(drop=True) 
        df1 = df1.drop(df1.index[k])
        df1 = df1.reset_index(drop=True)        

    else: k = k + 1


# Delete remaining rows
while df1['DateTime'].size > df2['DateTime'].size:
    p = df1['DateTime'].size - 1
    df1 = df1.drop(df1.index[p])
    A1.pop(p)

while df1['DateTime'].size < df2['DateTime'].size:
    q = df2['DateTime'].size - 1
    df2 = df2.drop(df2.index[q])
    B1.pop(q)    
    
