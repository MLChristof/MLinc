"""
Created on Wed Nov 21 10:17:19 2017

@author: JELLETB
"""

import ystockquote
from pprint import pprint
# pprint(ystockquote.get_historical_prices('GOOGL', '2013-01-03', '2013-01-08'))

print(ystockquote.get_price_book('GOOGL'))