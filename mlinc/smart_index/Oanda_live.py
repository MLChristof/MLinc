from mlinc.smart_index.strategies.backtrader_strategies import *
import backtrader as bt


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    oandastore = bt.stores.OandaStore()
    cerebro.broker = oandastore.getbroker()
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)

    # Add a strategy
    cerebro.addstrategy()
    # cerebro.addstrategy(BenchMarkStrategy)
    # cerebro.addstrategy(MlLagIndicatorStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # modpath = modpath[:-11]
    # datapath1 = os.path.join(modpath, 'data/EURUSD14402.csv')
    # datapath2 = os.path.join(modpath, 'data/Aluminium1440.csv')

    # Create a Data Feed
    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(2009, 2, 24),
    #     # Do not pass values before this date
    #     todate=datetime.datetime(2013, 2, 24),
    #     # Do not pass values after this date
    #     reverse=False)

    # data_EURUSD = bt.feeds.GenericCSVData(
    #     dataname=datapath1,
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(2010, 9, 20),
    #     # Do not pass values before this date
    #     todate=datetime.datetime(2017, 8, 11),
    #     nullvalue=0.0,
    #     dtformat=('%Y-%m-%d'),
    #     openinterest=-1,
    #     seperator=','
    #     )

    # data_alu = bt.feeds.GenericCSVData(
    #     dataname=datapath2,
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(2017, 5, 1),
    #     # Do not pass values before this date
    #     todate=datetime.datetime(2018, 4, 10),
    #     nullvalue=0.0,
    #     dtformat=('%Y.%m.%d'),
    #     openinterest=-1,
    #     seperator=','
    # )

    # Add the Data Feed to Cerebro
    # cerebro.adddata(data_EURUSD, name='EURUSD')
    # cerebro.adddata(data_alu, name='Alu')

    # Set our desired cash start
    # cerebro.broker.setcash(10000.0)

    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=500)

    # Set the commission and leverage
    # cerebro.broker.setcommission(commission=0.005, mult=50.0, name='EURUSD')

    # Print out the starting conditions
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # start = cerebro.broker.getvalue()

    # Run over everything
    cerebro.run()

    # Print out the final result
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # end = cerebro.broker.getvalue()
    # ans = (end - start) / end * 100
    # print('Percentage profit: %.3f' % ans)

    # Plot the result
    # cerebro.plot(style='candle')




