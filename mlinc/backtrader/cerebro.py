import backtrader as bt
import datetime
import os

from mlinc.backtrader.strategies.bacon_buyer_strategy import BaconBuyerStrategy
from mlinc.quandl.get_data import QuandlGet


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

    def import_quandl_data(self, name, stock, datetime=None, time=None, open=None, high=None, low=None, close=None, volume=None):
        # stock = QuandlGet(quandl_key=stock,
        #                   api_key=self.api_key,
        #                   start_date=self.start_date,
        #                   end_date=self.end_date)
        # stock.save_to_csv(os.getcwd() + '\data\{}.csv'.format(name))
        feed = bt.feeds.GenericCSVData(dataname=os.getcwd() + '\data\{}.csv'.format(name),
                                       datetime=datetime,
                                       time=time,
                                       open=open,
                                       close=close,
                                       high=high,
                                       low=low,
                                       volume=volume,
                                       dtformat='%Y-%m-%d',
                                       tmformat='%H:%M:%S',
                                       start_date=self.start_date,
                                       end_date=self.end_date)
        self.cerebro.adddata(feed, name=name)

    @property
    def run(self):
        return self.cerebro.run()

    def plot(self):
        self.cerebro.run()
        self.cerebro.plot(volume=True, style='candle')


if __name__ == '__main__':
    with open("C:\Data\\2_Personal\quandl_api.txt", 'r') as f:
        api_key = f.read()

    # RSI = Trader(strategy=RsiStrategy,
    #              start_date=datetime.datetime(2018, 1, 1),
    #              end_date=None,
    #              stock='CHRIS/ODE_TR1',
    #              api_key=api_key,
    #              start_cash=10000)
    # RSI.import_quandl_data(instrument='RICE', stock='CHRIS/ODE_TR1', close=1)
    # RSI.plot()

    HMA = Trader(strategy=BaconBuyerStrategy,
                 start_date=None,
                 end_date=None,
                 stock=None,
                 api_key=api_key,
                 start_cash=10000)
    # HMA.cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    HMA.cerebro.addsizer(bt.sizers.PercentSizer, percents=0.5)

    HMA.cerebro.broker.setcommission(commission=0.001, mult=50)
    HMA.import_quandl_data(name='BCO_USD_1H_OANDA_new_mod', stock=None, datetime=0, time=1, open=2, high=3, low=4, close=5,
                           volume=6)
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


