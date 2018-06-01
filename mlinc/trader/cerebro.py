import backtrader as bt
import datetime
import os

from mlinc.strategies.rsi_strategy import RsiStrategy
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
        self.cerebro.addstrategy(self.strategy)

        try:
            self.cerebro.adddata(stock)
        except:
            pass
            # print('Failed to add stock. Please run import_quandl_data method.')

        if self.start_cash:
            self.cerebro.broker.set_cash(100000)

        # self.cerebro.addsizer(bt.sizers.FixedSize, stake=0.5)
        # self.cerebro.broker.setcommission(commission=0.02)

    def import_quandl_data(self, name, open=None, close=None):
        stock = QuandlGet(quandl_key=self.stock,
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
        self.cerebro.adddata(feed, name=self.stock)

    def run(self):
        self.cerebro.run()

    def plot(self):
        self.run()
        self.cerebro.plot(volume=False)


if __name__ == '__main__':
    with open("C:\Data\\2_Personal\quandl_api.txt", 'r') as f:
        api_key = f.read()

    RSI = Trader(strategy=RsiStrategy,
                 start_date=datetime.datetime(2017, 11, 1),
                 end_date=datetime.datetime(2018, 1, 1),
                 stock='LME/PR_AL',
                 api_key=api_key,
                 start_cash=10000)
    RSI.import_quandl_data(name='ALU', close=2)
    RSI.run()
    RSI.plot()


