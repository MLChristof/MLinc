from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import numpy as n


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


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)

    # Add a strategy
    cerebro.addstrategy(BaconBuyerStrategy)
    # cerebro.addstrategy(BenchMarkStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    modpath = modpath[:-11]
    datapath = os.path.join(modpath, 'data/^GSPC.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2009, 2, 24),
        # Do not pass values before this date
        todate=datetime.datetime(2013, 2, 24),
        # Do not pass values after this date
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

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
    cerebro.plot()

