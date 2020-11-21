from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import btoandav20
import json
from statsmodels.tsa.stattools import adfuller
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
    # threshold=0.5, SL=0.01, TP=0.01, maperiod=6, printlog=True
    cerebro.addstrategy(MlLagIndicatorStrategy, threshold=0.5, SL=0.01, TP=0.01,
                        maperiod=6, printlog=True)
    # cerebro.optstrategy(MlLagIndicatorStrategy,
    #                     threshold=[0.5, 0.6, 0.7, 0.8, 0.9],
    #                     maperiod=[5, 6],
    #                     SL=[0.01, 0.015, 0.02],
    #                     TP=[0.01, 0.015, 0.02],
    #                     )

    oandastore = StoreCls(**storekwargs, practice=True)

    fromdate = datetime.datetime(2020, 1, 1)
    todate = datetime.datetime(2020, 11, 21)

    data0 = oandastore.getdata(dataname='XAG_USD',
                               compression=60,
                               backfill=False,
                               fromdate=fromdate,
                               todate=todate,
                               tz='CET',
                               qcheck=0.5,
                               timeframe=bt.TimeFrame.Minutes,
                               backfill_start=False,
                               historical=True,
                               )

    data1 = oandastore.getdata(dataname='XAU_USD',
                               compression=60,
                               backfill=False,
                               fromdate=fromdate,
                               todate=todate,
                               tz='CET',
                               qcheck=0.5,
                               timeframe=bt.TimeFrame.Minutes,
                               backfill_start=False,
                               historical=True,
                               )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data0)
    cerebro.adddata(data1)
    print('x')




