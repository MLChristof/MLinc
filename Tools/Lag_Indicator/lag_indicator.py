#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 13:33:12 2017

@author: rweegenaar

This script plots a lag indicator for backtesting between 2 pairs
loaded in Two_CSV2Candle
"""

import Tools.Lag_Indicator.LoadTwoCSV
import numpy as np
import pandas as pd


# number of timesteps(days/hours/seconds) to normalize data over
timeFrame = 200
ThresholdLong = -0.6
ThresholdShort = 0.8

timeFrameStr = str(timeFrame)+' hours'
timeFrameDelta = pd.Timedelta(timeFrameStr)

# i is amount of days to backtest from end date (backwards in time)
i = LoadTwoCSV.m - timeFrame

lagindex = np.zeros(i)
Position = np.zeros(i)
CorrCoef = np.zeros(i)

StartDate = pd.DataFrame.min(LoadTwoCSV.df1['DateTime'])
StartDate = pd.to_datetime(StartDate)

EndDate = pd.DataFrame.max(LoadTwoCSV.df1['DateTime'])
EndDate = pd.to_datetime(EndDate)

StartTimeFrame = EndDate - timeFrameDelta - pd.Timedelta('1 hours')
print('Indicator up-to-date until:')
print(EndDate)    

# Create Sliding Date Frame

for j in range(i):

    # Find closest date to StartTimeFrame in LoadTwoCSV.D12
    # StartTimeFrame may not appear in LoadTwoCSV.D12
        SlidingStart = min(LoadTwoCSV.D12, key=lambda d: abs(d - StartTimeFrame))
        SlidingStart = pd.to_datetime(SlidingStart)
    # Index number of SlidingStart in LoadTwoCSV.D12
        SlidingStart_row = LoadTwoCSV.D12_date.get_loc(SlidingStart)
        SlidingStart_count = SlidingStart_row - j
        closest_time_start = LoadTwoCSV.D12[SlidingStart_count]

    # Find closest date to EndDate in LoadTwoCSV.D12
    # Exact EndDate may not appear in LoadTwoCSV.D12
        SlidingEnd = min(LoadTwoCSV.D12, key=lambda d: abs(d - EndDate))
        SlidingEnd = pd.to_datetime(SlidingEnd)
    # Index number of SlidingStart in LoadTwoCSV.D12
        SlidingEnd_row = LoadTwoCSV.D12_date.get_loc(SlidingEnd)
        SlidingEnd_count = SlidingEnd_row - j
        closest_time_end = LoadTwoCSV.D12[SlidingEnd_count]
        print(closest_time_end)
        
    # Dates for plot (end date of backward sliding data frame is start date plot)
        if j==(i-1):
            PlotDates = LoadTwoCSV.df1['DateTime'].iloc[SlidingEnd_count:]
            PlotPriceOpen = LoadTwoCSV.df2['open'].iloc[SlidingEnd_count:]
            PlotPriceHigh = LoadTwoCSV.df2['high'].iloc[SlidingEnd_count:]
            PlotPriceLow = LoadTwoCSV.df2['low'].iloc[SlidingEnd_count:]
            PlotPriceClose = LoadTwoCSV.df2['close'].iloc[SlidingEnd_count:]
        
    # Sliding DataFrames closing prices
        df1SlidingMatrix = LoadTwoCSV.df1['close'].iloc[SlidingStart_count:SlidingEnd_count]
        df2SlidingMatrix = LoadTwoCSV.df2['close'].iloc[SlidingStart_count:SlidingEnd_count]
        
    # Normalize closing prices sliding matrices
        Normdf1 = (df1SlidingMatrix.tail(1) - min(df1SlidingMatrix))/(max(df1SlidingMatrix)-min(df1SlidingMatrix))
        Normdf2 = (df2SlidingMatrix.tail(1) - min(df2SlidingMatrix))/(max(df2SlidingMatrix)-min(df2SlidingMatrix))
        lagindex[j] = Normdf2 - Normdf1
        
        
#    # Take Positions (test is backwards in time, so logical operators are reversed) 
#        if lagindex[j-1] > ThresholdLong and lagindex[j] < ThresholdLong:
#            Position[j] = 1 # Take Long Position
#        elif lagindex[j-1] < ThresholdShort and lagindex[j] > ThresholdShort:
#            Position[j] = -1 # Take Short Position
#        else: Position[j] = np.NaN # No Action
        
    # Take Positions (test is backwards in time, so logical operators are reversed)
        if lagindex[j-2] > lagindex[j-1] and lagindex[j-1] < lagindex[j] and lagindex[j-1] < ThresholdLong:
            Position[j] = 1 # Take Long Position in local minimum of lagindicator
        elif lagindex[j-2] < lagindex[j-1] and lagindex[j-1] > lagindex[j] and lagindex[j-1] > ThresholdShort:
            Position[j] = -1 # Take Short Position in local maximum of lag indicator
        else: Position[j] = np.NaN # No Action
            
lagindexFlip = np.flipud(lagindex)
Position = np.flipud(Position)

print('Latest lag-indicator value =')
print(lagindexFlip[-1])


# Plot Lagindex and price
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

output_file("LagIndicator.html")
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,crosshair"

# plot 1 - lagindicator
p1 = figure(plot_width=1050, plot_height=320, x_axis_type='datetime',
            tools=TOOLS, title = 'Lag_Indicator')
p1.line(PlotDates,lagindexFlip, line_width=2, color='navy')

# plot 2 - price linechart + positions
# redefine Position for graphics
# Convert 'Position' to entry prices for Long & Short Positions
PositionPlotLong = np.clip(Position,0,1)
PositionPlotLong[PositionPlotLong == 0] = np.nan
PositionPlotLong = PositionPlotLong*PlotPriceClose

PositionPlotShort = np.clip(Position,-1,0)
PositionPlotShort[PositionPlotShort == 0] = np.nan
PositionPlotShort = -PositionPlotShort*PlotPriceClose

p2 = figure(plot_width=1050, plot_height=320, x_axis_type='datetime',
            tools=TOOLS, title = 'Price '+LoadTwoCSV.name2+' Line Chart and Postions')
p2.line(PlotDates,PlotPriceClose, line_width=1, color='lime')
p2.line(PlotDates,PlotPriceLow, line_width=1, color='firebrick')
p2.line(PlotDates,PlotPriceHigh, line_width=1, color='navy')


p2.triangle(PlotDates, PositionPlotLong, size=15,
              line_color="black", fill_color="lime", alpha=0.8)
p2.inverted_triangle(PlotDates, PositionPlotShort, size=15,
              line_color="black", fill_color="red", alpha=0.7)

# p2.vbar(PlotDates, 1E6,  PlotPriceAVG, PositionPlot,fill_color="#00FF00", line_color="#00FF00", fill_alpha=0.3)
# p2.vbar(PlotDates, 1E6,  PositionShortPlot, max(PlotPriceClose),fill_color="#F2583E", line_color="#F2583E",
# fill_alpha=0.3)
        
# multi line renderer
p = column(p1,p2)

show(p)




        



