"""
Created on Wed Nov 21 10:17:19 2017

@author: JELLETB
"""


"""
ystockquote does not work: Has been protected by the Yahoo Finance website strucutre
"""
import ystockquote
from pprint import pprint
import urllib.request

# url = 'http://www.stopforumspam.com/ipcheck/212.91.188.166'
# req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# html = urllib.request.urlopen(req).read()

# print(ystockquote.get_price_book('GOOGL'))

# pprint(ystockquote.get_historical_prices('GOOGL', '2013-01-03', '2013-01-08'))

# from pandas.io import data, wb # becomes
from pandas_datareader import data, wb
import pandas_datareader as pdr
print(pdr.get_data_yahoo('AAPL'))




