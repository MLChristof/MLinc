import backtrader as bt
import datetime
import os

from mlinc.strategies.rsi_strategy import RsiStrategy
from mlinc.strategies.lag_indicator_strategy import MlLagIndicatorStrategy
from mlinc.strategies.bacon_buyer_strategy import BaconBuyerStrategy
from mlinc.quandl_get import QuandlGet


class Trader(object):
    def __init__(self, strategy, start_date, end_date, stock, api_key, start_cash=None):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.stock = stock
        self.api_key = api_key
        self.start_cash = start_cash

        self.cerebro = bt.Cerebro()

        if isinstance(self.strategy, list):
            for strat in self.strategy:
                self.cerebro.addstrategy(strat)
        else:
            self.cerebro.addstrategy(self.strategy)

        # # Add a FixedSize sizer according to the stake
        # self.cerebro.addsizer(bt.sizers.FixedSize, stake=0.5)
        #
        # # Set the commission
        # self.cerebro.broker.setcommission(commission=0.02)

        # if self.stock is None:
        #     pass
        # else:
        #     try:
        #         self.cerebro.adddata(stock)
        #     except:
        #         pass
        # print('Failed to add stock. Please run import_quandl_data method.')

        # if self.start_cash is None:
        #     self.cerebro.broker.setcash(100000)
        # else:
        #     self.cerebro.broker.setcash(self.start_cash)

        # self.cerebro.addsizer(bt.sizers.FixedSize, stake=0.5)
        # self.cerebro.broker.setcommission(commission=0.02)

    def import_quandl_data(self, name, stock, open=None, close=None):
        stock = QuandlGet(quandl_key=stock,
                          api_key=self.api_key,
                          start_date=self.start_date,
                          end_date=self.end_date)
        stock.save_to_csv(os.getcwd() + '\data\{}.csv'.format(name))
        feed = bt.feeds.GenericCSVData(dataname=os.getcwd() + '\data\{}.csv'.format(name),
                                       open=open,
                                       close=close,
                                       dtformat='%Y-%m-%d',
                                       start_date=self.start_date,
                                       end_date=self.end_date)
        self.cerebro.adddata(feed, name=name)

    @property
    def run(self):
        return self.cerebro.run()

    def plot(self):
        self.cerebro.run()
        self.cerebro.plot(volume=False)


if __name__ == '__main__':
    with open("C:\Data\\2_Personal\quandl_api.txt", 'r') as f:
        api_key = f.read()

    # RSI = Trader(strategy=RsiStrategy,
    #              start_date=datetime.datetime(2018, 1, 1),
    #              end_date=None,
    #              stock='CHRIS/ODE_TR1',
    #              api_key=api_key,
    #              start_cash=10000)
    # RSI.import_quandl_data(name='RICE', stock='CHRIS/ODE_TR1', close=1)
    # RSI.plot()

    HMA = Trader(strategy=BaconBuyerStrategy,
                 start_date=datetime.datetime(2001, 1, 1),
                 end_date=None,
                 stock=None,
                 api_key=api_key,
                 start_cash=10000)
    HMA.cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
    HMA.cerebro.broker.setcommission(commission=0.01, mult=50)
    HMA.import_quandl_data(name='EUROFX', stock='CHRIS/CME_EC1', close=6, open=1)
    HMA.plot()

    # LagIndicator = Trader(MlLagIndicatorStrategy,
    #                       datetime.datetime(2017, 10, 1),
    #                       None,
    #                       None,
    #                       api_key,
    #                       1000000000000000000000000)
    # LagIndicator.import_quandl_data('ALU', 'LME/PR_AL', close=2)
    # LagIndicator.import_quandl_data('BRENT', 'CHRIS/ICE_B1', close=4)
    # LagIndicator.cerebro.broker.setcash(100)
    # LagIndicator.cerebro.addsizer(bt.sizers.FixedSize, stake=0.00005)
    # LagIndicator.cerebro.broker.setcommission(commission=0.02)
    # # LagIndicator.run()
    # LagIndicator.plot()


