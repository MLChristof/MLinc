from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import math
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
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
    # RRR=1, min_hma_slope=0.015
    cerebro.addstrategy(BaconBuyerStrategy, RRR=1, min_hma_slope=0.015, stakepercent=0.004,
                        printlog=True, SL_multiplier=1.0)
    # UK10YB_GBP Optimization
    # cerebro.optstrategy(BaconBuyerStrategy,
    #                     stakepercent=[0.004],
    #                     RRR=[1],
    #                     min_hma_slope=[0.014, 0.015, 0.016, 0.018, 0.02],
    #                     SL_multiplier=[1.00],
    #                     )
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
                              fromdate=datetime.datetime(2020, 1, 1),
                              todate=datetime.datetime(2020, 11, 11),
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
    cerebro.addsizer(btoandav20.sizers.OandaV20RiskCashSizer)
    cerebro.addsizer(bt.sizers.AllInSizer)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0, mult=5)

    # Add Analyzers
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='ta')
    cerebro.addanalyzer(btanalyzers.Transactions, _name='transactions')
    # Add observer
    cerebro.addobserver(bt.observers.Value, _name='value')

    # Run over everything for opt strategy
    thestrats = cerebro.run(maxcpus=1)
    # for normal strategy
    # thestrats = cerebro.run()

    if isinstance(cerebro.strats[0], list):
        thestrat = thestrats[0]
        ta = thestrat.analyzers.ta.get_analysis()
        streak = ta.streak
        dict_annual_return = thestrat.analyzers.annual_return.get_analysis()
        dict_annual_return.update((x, round(y * 100, 2)) for x, y in dict_annual_return.items())
        df_annual_return = pd.DataFrame(dict_annual_return.values(), index=dict_annual_return.keys(),
                                        columns=['annual return'])
        dict_transactions = thestrat.analyzers.transactions.get_analysis()
        df_transactions = pd.DataFrame(dict_transactions.values(), index=dict_transactions.keys(),
                                       columns=['transactions'])
        # print Results
        print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
        print('Annual Return:', df_annual_return)
        print('Draw Down:', thestrat.analyzers.drawdown.get_analysis())
        print('Total Trades:', ta.total)
        print('Trades Won:', ta.won)
        print('Trades Lost:', ta.lost)
        print(f'Won/Lost: {ta.won.total / ta.lost.total:.2f}')
        print('Streak:', streak)

        # save results to files
        # get datetimes
        datetime_array = thestrat.observers.value.data0_datetime.array
        datetime_array_dates = [bt.num2date(x) for x in datetime_array]
        value_array = thestrat.observers.value.array
        df_value = pd.DataFrame(index=datetime_array_dates, data={"value": value_array})
        df_value.to_csv(r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\value_array.csv')
        df_annual_return.to_excel(r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\annual_return_bacbuy.xlsx')
        df_transactions.to_excel(r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\transactions_bacbuy.xlsx')


        # # Plot the result
        cerebro.plot(style='candle', volume=False, preload=False)
    else:
        # loop over runs for results from analyzers
        run_counter = 0
        file_name = r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\annual_return_bacbuy_opt.xlsx'
        for i in thestrats:
            won = i[0].analyzers.ta.get_analysis().won.total
            lost = i[0].analyzers.ta.get_analysis().lost.total
            if run_counter == 0:
                dict_annual_return = i[0].analyzers.annual_return.get_analysis()
                dict_annual_return.update((x, round(y * 100, 2)) for x, y in dict_annual_return.items())
                df_annual_return = pd.DataFrame(dict_annual_return.values(), index=dict_annual_return.keys(),
                                                columns=['run 0'])
            else:
                dict_annual_return = i[0].analyzers.annual_return.get_analysis()
                dict_annual_return.update((x, round(y * 100, 2)) for x, y in dict_annual_return.items())
                df_annual_return['run ' + str(run_counter)] = dict_annual_return.values()
            # print Results
            print('Sharpe Ratio:', i[0].analyzers.mysharpe.get_analysis())
            print('Annual Return:', df_annual_return)
            print('Trades Won:', won)
            print('Trades Lost:', lost)
            print(f'Won/Lost: {won/lost:.2f}')
            run_counter += 1

        # save as Excel
        df_annual_return.to_excel(file_name)  # Write DateFrame back as Excel file



