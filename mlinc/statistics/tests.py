import sys
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("C:\Data\Python\MLinc")

from mlinc.oanda.trader import OandaTrader
from statsmodels.tsa.stattools import adfuller

trader = OandaTrader(["XAU_USD", "XAG_USD"], accountid="101-004-7108173-016", token="0dd3f3c2a10b6c4c98d34990bb97f994-ee519f5c44917cd7699b9510c48074c0")
trader.count = 500
trader.granularity = 'H1'

b_oil = trader.data_as_dataframe("BCO_USD")["close"]
w_oil= trader.data_as_dataframe("WTICO_USD")['close']

# PEARSON CORRELATION TEST!!!
c, p = stats.pearsonr(b_oil, w_oil)

b_oil_diff = np.diff(b_oil)
w_oid_diff = np.diff(w_oil)

#TODO: Extedn this python file with other correlation tests. in OOP format.