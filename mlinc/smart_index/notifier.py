from mlinc.smart_index.strategies.backtrader_strategies import TestStrategy, BenchMarkStrategy
import backtrader as bt
import os, sys
import datetime

# Create a cerebro entity
cerebro = bt.Cerebro()
# cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)

# Add a strategy
cerebro.addstrategy(TestStrategy)
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