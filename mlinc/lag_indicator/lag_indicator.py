from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import time

# Import the backtrader platform
import backtrader as bt
import numpy as n

# Import ML indicators
from mlinc.smart_index.indicators.backtrader_indicators import *
from mlinc.quandl_get import QuandlGet
from mlinc.notifier import notification

with open("C:\Data\\2_Personal\quandl_api.txt", 'r') as f:
    api_key = f.read()

file_jelle = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_jelle.txt'
file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.month = [1, 2]

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # TODO: Open long postiion every 1st of the month or next trading day
        # TODO: Detect Bear market (retrace of 25% from peak in one year
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        self.month.append(self.datas[0].datetime.date(0).month)

        if self.month[-1] != self.month[-2]:
            if self.month[-1] > 9 or self.month[-1] < 5:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
            elif self.month[-1] == 5:
                self.order = self.close()
            elif self.month[-1] == 9:
                self.order = self.buy(size=8)
            else:
                return


class BenchMarkStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        # print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.month = [1, 2]

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        self.month.append(self.datas[0].datetime.date(0).month)

        if self.month[-1] != self.month[-2]:
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.order = self.buy()
        else:
            return


class BaconBuyerStrategy(bt.Strategy):
    params = (
        ('maperiod', 14),
        ('RRR', 1),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        # print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.indicator = bt.indicators.HullMovingAverage(self.datas[0], period=self.params.maperiod)
        # self.indicatorSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        hma_data = n.array((self.indicator.lines.hma[-6],
                            self.indicator.lines.hma[-5],
                            self.indicator.lines.hma[-4],
                            self.indicator.lines.hma[-3],
                            self.indicator.lines.hma[-2],
                            self.indicator.lines.hma[-1],
                            self.indicator.lines.hma[0]))

        hma_diff = n.diff(hma_data)
        # Open Long Position
        if hma_diff[5] - hma_diff[4] > 0 \
            and hma_diff[4] - hma_diff[3] < 0 \
            and hma_diff[3] - hma_diff[2] < 0 \
            and hma_diff[2] - hma_diff[1] < 0 \
            and hma_diff[1] - hma_diff[0] < 0:

            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.order = self.buy(exectype=bt.Order.StopTrail, trailamount=0.25)


        # self.month.append(self.datas[0].datetime.date(0).month)
        #
        # if self.month[-1] != self.month[-2]:
        #     self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #     self.order = self.buy()
        # else:
        #     return


class MlLagIndicatorStrategy(bt.Strategy):
    params = (
        ('maperiod', 10),
        )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        # print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.lagindex = [0, 0, 0]
        self.threshold_long = -0.6
        self.threshold_short = 0.95

        self.indicator = MlLagIndicator(self.datas[0], self.datas[1], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        self.lagindex.append(self.indicator.lag_index())
        # print(self.lagindex[-1])

        if self.lagindex[-3] > self.lagindex[-2] < self.lagindex[-1] and self.lagindex[-2] < self.threshold_long:
            self.log('Go Long!!! Because lagindex is [{}, {}, {}]'.format(self.lagindex[-3],
                                                                          self.lagindex[-2],
                                                                          self.lagindex[-1]))
            self.order = self.buy(data=self.datas[0])
        elif self.lagindex[-3] < self.lagindex[-2] > self.lagindex[-1] and self.lagindex[-2] > self.threshold_short:
            self.log('Go Short!!! Because lagindex is [{}, {}, {}]'.format(self.lagindex[-3],
                                                                           self.lagindex[-2],
                                                                           self.lagindex[-1]))
            self.order = self.sell(data=self.datas[0])
        else:
            return


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(MlLagIndicatorStrategy)

    end_date = datetime.datetime.today() - datetime.timedelta(days=0)

    quandl_alu = QuandlGet(quandl_key='LME/PR_AL',
                           api_key=api_key,
                           start_date=datetime.datetime(2017, 10, 1),
                           end_date=end_date
                           )
    quandl_alu.save_to_csv(os.getcwd() + '\\data\\LME_PR_AL.csv')
    data_alu = bt.feeds.GenericCSVData(
        dataname=os.getcwd() + '\\data\\LME_PR_AL.csv',
        close=2,
        dtformat='%Y-%m-%d',
        start_date=datetime.datetime(2017, 10, 1),
        end_date=end_date
    )

    quandl_oil = QuandlGet(quandl_key='CHRIS/ICE_B1',
                           api_key=api_key,
                           start_date=datetime.datetime(2017, 10, 1),
                           end_date=end_date
                           )
    quandl_oil.save_to_csv(os.getcwd() + '\\data\\ICE_B1.csv')
    data_oil = bt.feeds.GenericCSVData(
        dataname=os.getcwd() + '\\data\\ICE_B1.csv',
        volume=7,
        openinterest=8,
        dtformat='%Y-%m-%d',
        start_date=datetime.datetime(2017, 10, 1),
        end_date=end_date
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data_alu, name='Alu')
    cerebro.adddata(data_oil, name='Oil')

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.5)

    # Set the commission
    cerebro.broker.setcommission(commission=0.02)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    start = cerebro.broker.getvalue()

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    end = cerebro.broker.getvalue()
    ans = (end - start) / end * 100
    print('Percentage profit: %.3f' % ans)

    # Plot the result
    # cerebro.plot(style='candle')
    cerebro.plot(volume=False)

