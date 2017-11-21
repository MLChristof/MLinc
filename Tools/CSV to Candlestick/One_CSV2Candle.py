#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 13:51:55 2017

@author: rweegenaar
"""

from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file

df = pd.read_csv('BrentOil1440.csv',
                 header=None,names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

print(df)

df['date'] = pd.to_datetime(df['date'])
df['time'] = pd.to_datetime(df['time'])
 
inc = df.close > df.open
dec = df.open > df.close
w = 4E7 #width candle bar
 
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
 
p = figure(x_axis_type="datetime", tools=TOOLS,
       plot_width=1000, title = "Candlestick Chart")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3
 
p.segment(df.date, df.high, df.date, df.low, color="black")
p.vbar(df.date[inc], w,  df.open[inc], df.close[inc],
   fill_color="#00FF00", line_color="black")
p.vbar(df.date[dec], w,  df.open[dec], df.close[dec],
   fill_color="#F2583E", line_color="black")
 
output_file("candlestick.html", title="candlestick.py example")
 
show(p)  # open a browser

