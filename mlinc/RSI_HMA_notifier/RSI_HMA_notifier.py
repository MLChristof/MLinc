import quandl
import matplotlib.pyplot as plt

# This script returns the latest RSI and HMA values

RSI_period = 14
HMA_period = 20

# Commodity: Rough Rice
df1 = quandl.get('CHRIS/CME_RR1.6', start_date='2018-05-01')

plt.plot(df1.index, df1.values)
# plt.show()

tail = df1.tail(HMA_period)
avg_tail = tail.values.sum()/HMA_period

