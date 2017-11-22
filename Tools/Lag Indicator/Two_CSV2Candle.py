#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 13:51:55 2017
@author: rweegenaar

This script reads in two CSVs, equalizes the dates and times and plots candlestick charts.
Place 2 CSVs in folder. Rest is automatic
"""
import glob
from math import pi

import pandas as pd
from bokeh.plotting import figure, show, output_file

# Read CSVs
file_names = glob.glob('*.csv')
name1 = file_names[0]
name2 = file_names[1]


df1 = pd.read_csv(name1,
                  header=None,names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

df2 = pd.read_csv(name2,
                  header=None,names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

# Equalize CSV DataFrames ######

# test whether frequency is 1D or higher
# 1D times in CSV may not be equal
test_freq = df1['time'][1] == df1['time'][2]

if test_freq == True:
            A1 = df1['date']
            B1 = df2['date']

else:
            A1 = df1['date'] + " " + df1['time'] 
            B1 = df2['date'] + " " + df2['time']


D12 = list(set(A1) & set(B1))
D12_date = pd.to_datetime(D12)
D12_date.values.sort()

k = 0
m = D12_date.size

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
while df1['date'].size > df2['date'].size:
    p = df1['date'].size - 1
    df1 = df1.drop(df1.index[p])
    A1.pop(p)

while df1['date'].size < df2['date'].size:
    q = df2['date'].size - 1
    df2 = df2.drop(df2.index[q])
    B1.pop(q)    
    


###### PLOT 1 ######
A1 = pd.to_datetime(A1)
 
inc = df1.close > df1.open
dec = df1.open > df1.close

if test_freq == True:
    w = 4E7  # width candle bar

else:
    w = 2E6  # width candle bar

 
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
 
p = figure(x_axis_type="datetime", tools=TOOLS,
       plot_width=1000, title = name1)
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3
 
p.segment(A1, df1.high, A1, df1.low, color="black")
p.vbar(A1[inc], w,  df1.open[inc], df1.close[inc],
   fill_color="#00FF00", line_color="black")
p.vbar(A1[dec], w,  df1.open[dec], df1.close[dec],
   fill_color="#F2583E", line_color="black")
 
output_file("candlestick1.html", title=name1)
 
show(p)  # open a browser


###### PLOT 2 ######
B1 = pd.to_datetime(B1)
 
inc = df2.close > df2.open
dec = df2.open > df2.close

if test_freq == True:
    w = 4E7  # width candle bar

else:
    w = 2E6  # width candle bar
 
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
 
p = figure(x_axis_type="datetime", tools=TOOLS,
           plot_width=1000, title = name2)
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3
 
p.segment(B1, df2.high, B1, df2.low, color="black")
p.vbar(B1[inc], w,  df2.open[inc], df2.close[inc],
       fill_color="#00FF00", line_color="black")
p.vbar(B1[dec], w,  df2.open[dec], df2.close[dec],
       fill_color="#F2583E", line_color="black")
 
output_file("candlestick2.html", title=name2)
 
show(p)  # open a browser
