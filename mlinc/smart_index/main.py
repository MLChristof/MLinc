import quandl
import datetime
import pandas as p
import numpy as n
import matplotlib.pyplot as plt
import os

file = open("C:/Users/Jelle/Desktop/quandl_api.txt")
api = file.readline()
quandl.ApiConfig.api_key = api


def multiply(numbers):
    total = 1
    for x in numbers:
        total *= x
    return total


month = {'1': 'january',
         '2': 'february',
         '3': 'march',
         '4': 'april',
         '5': 'may',
         '6': 'june',
         '7': 'july',
         '8': 'august',
         '9': 'september',
         '10': 'oktober',
         '11': 'november',
         '12': 'december'}


class SmartIndex(object):
    def __init__(self, symbol):
        self.symbol = symbol

    def quandl_stocks(self, start_date=(2000, 1, 1), ticker=None, end_date=None):
        """
        symbol is a string representing a stock symbol, e.g. 'AAPL'

        start_date and end_date are tuples of integers representing the year, month,
        and day

        end_date defaults to the current date when None
        """

        # query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]
        query_list = [self.symbol]
        # print(query_list)

        start_date = datetime.date(*start_date)

        if end_date:
            end_date = datetime.date(*end_date)
        else:
            end_date = datetime.date.today()

        quandlpd = quandl.get(query_list,
                              returns='pandas',
                              start_date=start_date,
                              end_date=end_date,
                              collapse='daily',
                              order='asc',
                              ticker=ticker
                              )

        # types = list(quandlpd.dtypes.index)
        # print(types)
        # for i, item in enumerate(types):
        #     item = str(item)
        #     item = item.lower()
        #     if 'open' in item:
        #         types[i] = 'open'
        #     elif 'high' in item:
        #         types[i] = 'high'
        #     elif 'low' in item:
        #         types[i] = 'low'
        #     elif 'last' or 'close' in item:
        #         types[i] = 'close'
        # print(types)

        # stockID = self.symbol + ' - Open'

        # print(n.array(quandlpd[stockID]))

        date = quandlpd.index
        # print(date)
        # print(type(date))
        print(date['datetime64[ns]'])

        open = n.array(quandlpd[self.symbol + ' - Open'])
        high = n.array(quandlpd[self.symbol + ' - High'])
        low = n.array(quandlpd[self.symbol + ' - Low'])
        close = n.array(quandlpd[self.symbol + ' - Last'])
        volume = n.array(quandlpd[self.symbol + ' - Volume'])

        output = {'open': open, 'high': high, 'low': low, 'close': close, 'volume': volume}

        return output


if __name__ == '__main__':
    Test = SmartIndex(symbol='CHRIS/CME_SP1')
    Test.quandl_stocks(start_date=(1984, 1, 1), end_date=None)