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
from mlinc.backtrader.strategies.bacon_buyer_strategy import BaconBuyerStrategy

StoreCls = btoandav20.stores.OandaV20Store
DataCls = btoandav20.feeds.OandaV20Data


# BrokerCls = btoandav20.brokers.OandaV20Broker

# Create a Stratey
class MA_CrossOver(bt.SignalStrategy):
    alias = ('SMA_CrossOver',)

    params = (
        # period for the fast Moving Average
        ('pfast', 5),
        # period for the slow moving average
        ('pslow', 60)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)

    def notify_store(self, msg, *args, **kwargs):
        print('*' * 5, 'STORE NOTIF:', msg)

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # self.dataclose = self.datas[0].close
        self.dataclose = self.data.close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Indicators
        sma1, sma2 = bt.ind.SMA(period=self.p.pfast), bt.ind.SMA(period=self.p.pslow)
        self.signal_add(bt.SIGNAL_LONGSHORT, bt.ind.CrossOver(sma1, sma2))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('GROSS %.5f, NET %.5f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Date: %s, Close, %.5f' % (self.data.datetime.datetime(), self.dataclose[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return


class maxRiskSizer(bt.Sizer):
    params = (('risk', 0.1),)

    def __init__(self):
        if self.p.risk > 1 or self.p.risk < 0:
            raise ValueError('The risk parameter is a percentage which must be entered as a float. e.g. 0.5')

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = math.floor((cash * self.p.risk) / data.close[0])
        else:
            size = position.size
        return size


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
    # cerebro.addstrategy(MA_CrossOver)
    # XCU Single run
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=0.4, min_hma_slope=0.002)
    # XCU Optimization
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=5, min_hma_slope=0.00154, printlog=True)
    # cerebro.optstrategy(BaconBuyerStrategy,
    #                     RRR=[0.4],
    #                     min_hma_slope=[0.0020, 0.0022]
    #                     )
    # BCO Single run
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=0.4, min_hma_slope=0.11, stakepercent=0.01, printlog=True)
    # BCO Optimization
    # cerebro.optstrategy(BaconBuyerStrategy,
    #                     stakepercent=0.01,
    #                     RRR=[0.4],
    #                     min_hma_slope=[0.105, 0.110, 0.115]
    #                     )
    # DE10YB_EUR Single run
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=1, min_hma_slope=0.022, stakepercent=1, printlog=True)
    # DE10YB_EUR Optimization
    # cerebro.optstrategy(BaconBuyerStrategy,
    #                     stakepercent=1,
    #                     RRR=[1],
    #                     min_hma_slope=[0.022, 0.023, 0.024]
    #                     )
    # UK10YB_GBP Single run
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=1, min_hma_slope=0.015, stakepercent=0.004,
    #                     printlog=True, SL_multiplier=1)
    # UK10YB_GBP Optimization
    cerebro.optstrategy(BaconBuyerStrategy,
                        stakepercent=[0.004],
                        RRR=[1.0],
                        min_hma_slope=[0.015],
                        )
    # EUR_USD Single run
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=0.4, min_hma_slope=0.0004, stakepercent=1, printlog=True)
    # EUR_USD Optimization
    # cerebro.optstrategy(BaconBuyerStrategy,
    #                     stakepercent=1,
    #                     RRR=[0.4, 0.5, 0.6],
    #                     min_hma_slope=[0.0002, 0.0003, 0.0004]
    #                     )
    # XAU_EUR Single run
    # cerebro.addstrategy(BaconBuyerStrategy, RRR=1, min_hma_slope=0.6, stakepercent=0.001, printlog=True)
    # XAU_EUR Optimization
    # cerebro.optstrategy(BaconBuyerStrategy,
    #                     stakepercent=0.001,
    #                     RRR=[1],
    #                     min_hma_slope=[0.5, 0.6, 0.70, 0.8, 0.9, 1]
    #                     )


    # instantiate data
    # cerebro.broker = oandastore.getbroker()
    oandastore = StoreCls(**storekwargs, practice=True)

    data = oandastore.getdata(dataname='UK10YB_GBP',
                              compression=60,
                              backfill=False,
                              fromdate=datetime.datetime(2010, 7, 30),
                              todate=datetime.datetime(2015, 7, 30),
                              tz='CET',
                              qcheck=0.5,
                              timeframe=bt.TimeFrame.Minutes,
                              backfill_start=False,
                              historical=True,
                              )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000)

    # Add sizer
    # cerebro.addsizer(btoandav20.sizers.OandaV20RiskCashSizer)
    # cerebro.addsizer(bt.sizers.AllInSizer)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0, mult=5)

    # Add Analyzer
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='ta')

    # Run over everything
    thestrats = cerebro.run(maxcpus=1)
    # thestrats = cerebro.run()

    # thestrat = thestrats[0]
    #
    # won = thestrat.analyzers.ta.get_analysis().won.total
    # lost = thestrat.analyzers.ta.get_analysis().lost.total
    #
    # # print Sharpe
    # print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
    # print('Trades Won:', won)
    # print('Trades Lost:', lost)
    # print(f'Won/Lost: {won/lost:.2f}')
    #
    # # Plot the result
    # cerebro.plot(style='candle', volume=False, preload=False)
