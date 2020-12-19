from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
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

    fromdate = datetime.datetime(2020, 11, 19)
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

    # Set our desired cash start
    cerebro.broker.setcash(10000)

    # Add sizer
    # cerebro.addsizer(btoandav20.sizers.OandaV20RiskCashSizer)
    # cerebro.addsizer(bt.sizers.AllInSizer)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=20)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0, mult=10)

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
        print('Annual Return [%]:', df_annual_return)
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
        diflen = len(value_array) - len(datetime_array)
        df_value = pd.DataFrame(index=datetime_array_dates, data={"value": value_array[diflen:]})
        df_value.to_csv(r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\value_array.csv')
        df_annual_return.to_excel(r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\annual_return_mosterd.xlsx')
        df_transactions.to_excel(r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\transactions_mosterd.xlsx')
        # # Plot the result
        cerebro.plot(style='candle', volume=False, preload=False)
    else:
        # loop over runs for results from analyzers
        run_counter = 0
        file_name = r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\backtest\annual_return_mosterd_opt.xlsx'
        for i in thestrats:
            won = i[0].analyzers.ta.get_analysis().won.total
            lost = i[0].analyzers.ta.get_analysis().lost.total
            if run_counter == 0:
                dict_annual_return = i[0].analyzers.annual_return.get_analysis()
                dict_annual_return.update((x, round(y * 100, 2)) for x, y in dict_annual_return.items())
                df_annual_return = pd.DataFrame(dict_annual_return.values(), index=dict_annual_return.keys(),
                                                columns=[f'run 0; SL={i[0].params.SL}; TP={i[0].params.TP}; '
                                                         f'threshold={i[0].params.threshold}; '
                                                         f'maperiod={i[0].params.maperiod}'])
            else:
                dict_annual_return = i[0].analyzers.annual_return.get_analysis()
                dict_annual_return.update((x, round(y * 100, 2)) for x, y in dict_annual_return.items())
                df_annual_return[f'run {run_counter}; SL={i[0].params.SL}; TP={i[0].params.TP}; '
                                 f'threshold={i[0].params.threshold}; '
                                 f'maperiod={i[0].params.maperiod}'] = dict_annual_return.values()
            # print Results
            print('Sharpe Ratio:', i[0].analyzers.mysharpe.get_analysis())
            print('Annual Return [%]:', df_annual_return)
            print('Trades Won:', won)
            print('Trades Lost:', lost)
            print(f'Won/Lost: {won/lost:.2f}')
            run_counter += 1

        # save as Excel
        df_annual_return.to_excel(file_name)  # Write DateFrame back as Excel file
