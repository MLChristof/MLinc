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
    cerebro.addstrategy(MlLagIndicatorStrategy)

    oandastore = StoreCls(**storekwargs, practice=True)

    data1 = oandastore.getdata(dataname='BCO_USD',
                              compression=1,
                              backfill=False,
                              fromdate=datetime.datetime(2015, 7, 31),
                              todate=datetime.datetime(2020, 7, 31),
                              tz='CET',
                              qcheck=0.5,
                              timeframe=bt.TimeFrame.Days,
                              backfill_start=False,
                              historical=True,
                              )

    data2 = oandastore.getdata(dataname='WTICO_USD',
                              compression=1,
                              backfill=False,
                              fromdate=datetime.datetime(2015, 7, 31),
                              todate=datetime.datetime(2020, 7, 31),
                              tz='CET',
                              qcheck=0.5,
                              timeframe=bt.TimeFrame.Days,
                              backfill_start=False,
                              historical=True,
                              )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data1)
    cerebro.adddata(data2)

    # Set our desired cash start
    cerebro.broker.setcash(10000)

    # Add sizer
    # cerebro.addsizer(btoandav20.sizers.OandaV20RiskCashSizer)
    # cerebro.addsizer(bt.sizers.AllInSizer)
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.00005)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0, mult=5)

    # Add Analyzer
    # cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    # cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='ta')

    # Run over everything
    # thestrats = cerebro.run(maxcpus=1)
    thestrats = cerebro.run()

    thestrat = thestrats[0]

    # won = thestrat.analyzers.ta.get_analysis().won.total
    # lost = thestrat.analyzers.ta.get_analysis().lost.total
    #
    # # print Sharpe
    # print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
    # print('Trades Won:', won)
    # print('Trades Lost:', lost)
    # print(f'Won/Lost: {won/lost:.2f}')
    # #
    # # # Plot the result
    cerebro.plot(style='candle', volume=False, preload=False)
    # #
