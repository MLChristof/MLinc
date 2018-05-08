from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import os.path
import sys

import backtrader as bt
import backtrader.feeds as btfeeds
import numpy as n

# Import ML indicators and strategies
from mlinc.smart_index.indicators.backtrader_indicators import *
from mlinc.smart_index.strategies.backtrader_strategies import *

cerebro = bt.Cerebro()

# Add a strategy
cerebro.addstrategy(TestStrategy)

data = bt.feeds.Quandl(
    dataname='AAPL',
    fromdate=datetime(2016, 1, 1),
    todate=datetime(2017, 1, 1),
    buffered=True
    )

# Add the Data Feed to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(100000.0)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=0.5)

# Set the commission
# cerebro.broker.setcommission(commission=0.02)

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
cerebro.plot(style='candle')