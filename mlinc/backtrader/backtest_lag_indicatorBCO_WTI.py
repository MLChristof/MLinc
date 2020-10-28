from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import math
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import numpy as np
from backtrader.utils import flushfile
import btoandav20
import json
from mlinc.backtrader.strategies.lag_indicator_strategy import MlLagIndicatorStrategy


StoreCls = btoandav20.stores.OandaV20Store
DataCls = btoandav20.feeds.OandaV20Data


# BrokerCls = btoandav20.brokers.OandaV20Broker


if __name__ == '__main__':
    with open("C:\\Data\\2_Personal\\Python_Projects\\MLinc\\mlinc\\oanda\\conf_files\\backtrader_config.json",
              "r") as file:
        config = json.load(file)

    storekwargs = dict(
        token=config["oanda"]["token"],
        account=config["oanda"]["account"],
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='Oanda API token')
    parser.add_argument('--account', help='Oanda API account')
    args = parser.parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    cerebro.addstrategy(MlLagIndicatorStrategy, threshold=0.6, SL=0.005, TP=0.05,
                        maperiod=4, printlog=True)
    # cerebro.optstrategy(MlLagIndicatorStrategy,
    #                     threshold=[0.6],
    #                     maperiod=[3],
    #                     SL=[0.005, 0.05],
    #                     TP=[0.005, 0.05],
    #                     )

    oandastore = StoreCls(**storekwargs, practice=True)

    data0 = oandastore.getdata(dataname='BCO_USD',
                               compression=1,
                               backfill=False,
                               fromdate=datetime.datetime(2005, 7, 31),
                               todate=datetime.datetime(2020, 7, 31),
                               tz='CET',
                               qcheck=0.5,
                               timeframe=bt.TimeFrame.Days,
                               backfill_start=False,
                               historical=True,
                               )

    data1 = oandastore.getdata(dataname='WTICO_USD',
                               compression=1,
                               backfill=False,
                               fromdate=datetime.datetime(2005, 7, 31),
                               todate=datetime.datetime(2020, 7, 31),
                               tz='CET',
                               qcheck=0.5,
                               timeframe=bt.TimeFrame.Days,
                               backfill_start=False,
                               historical=True,
                               )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data0)
    cerebro.adddata(data1)

    # Set our desired cash start
    cerebro.broker.setcash(10000)

    # Add sizer
    # cerebro.addsizer(btoandav20.sizers.OandaV20RiskCashSizer)
    # cerebro.addsizer(bt.sizers.AllInSizer)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=35)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0, mult=10)

    # Add Analyzer
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='ta')

    # Run over everything
    # uncomment for optimization run
    # thestrats = cerebro.run(maxcpus=1)
    # uncomment for single run
    thestrats = cerebro.run()
    thestrat = thestrats[0]

    won = thestrat.analyzers.ta.get_analysis().won.total
    lost = thestrat.analyzers.ta.get_analysis().lost.total
    #
    # print Sharpe
    print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
    print('Trades Won:', won)
    print('Trades Lost:', lost)
    print(f'Won/Lost: {won/lost:.2f}')

    # Plot the result
    cerebro.plot(volume=False, preload=False)

