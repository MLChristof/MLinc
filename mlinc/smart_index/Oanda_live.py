import argparse
import datetime
import backtrader as bt

apikey = '0bfaffb667afd6db474f8ec3d3a54540-bc042d7e21b87eb55d958edc2997fd2a'
acc = '101-004-7108173-001'

# Create a Stratey
class TestStrategy(bt.Strategy):

    def __init__(self):
        pass

    #Provides any noticficaitons about the data.
    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)

    def notify_store(self, msg, *args, **kwargs):
        print('*' * 5, 'STORE NOTIF:', msg)

    def next(self):
        # Simply log the closing price of the series from the reference
        print('O: {} H: {} L: {} C: {}'.format(
                self.data.open[0],
                self.data.high[0],
                self.data.low[0],
                self.data.close[0],
                ))


    def start(self):
        if self.data0.contractdetails is not None:
            print('-- Contract Details:')
            print(self.data0.contractdetails)
        print('Started')
        acc_cash = cerebro.broker.getcash()
        acc_val = cerebro.broker.getvalue()
        print('Account Cash = {}'.format(acc_cash))
        print('Account Value = {}'.format(acc_val))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    oandastore = bt.stores.OandaStore(token=apikey, account=acc, practice=True)
    cerebro.broker = oandastore.getbroker()

    data0 = oandastore.getdata(dataname="GBP_USD", timeframe=bt.TimeFrame.Ticks, compression=1, backfill_start=False, backfill=False)

    #This is setting what timeframe we want to use.
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Minutes, compression=5)

    cerebro.addstrategy(TestStrategy)
    cerebro.run()