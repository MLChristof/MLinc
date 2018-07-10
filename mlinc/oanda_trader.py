import numpy as n
import pandas as pd
import backtrader as bt
import os

from mlinc.oanda_examples.candle_data import candles

# test_list = {'instrument': 'EUR_USD', 'granularity': 'H1', 'candles': [{'complete': True, 'volume': 3138, 'time': '2018-07-09T15:00:00.000000000Z',
#               'mid': {'o': '1.17590', 'h': '1.17618', 'l': '1.17406', 'c': '1.17444'}},
#              {'complete': True, 'volume': 1988, 'time': '2018-07-09T16:00:00.000000000Z',
#               'mid': {'o': '1.17450', 'h': '1.17510', 'l': '1.17418', 'c': '1.17466'}}]}


def hma(values, window):
    # requires wma.py

    # HMA = WMA(2*WMA(PRICE, N/2) - WMA(PRICE, N), SQRT(N))

    period = int(n.sqrt(window))

    # created wma array with NaN values for indexes < window value
    # hull_moving_averages = np.empty(window)
    # hull_moving_averages[:] = np.NAN

    wma1 = 2 * wma(values, n.int(window/2))
    wma2 = wma(values, window)

    hull_moving_averages = wma((wma1 - wma2), period)

    return hull_moving_averages


def wma(values, window):
    # requires trinum.py

    # using definition provided at
    # http://www.oanda.com/forex-trading/learn/forex-indicators/weighted-moving-average

    # create an array of weights
    # use floats when creating array, or the result is integer division below
    # and, note that they are reversed.  why?  read this:
    # http://stackoverflow.com/questions/12816011/weighted-moving-average-with-numpy-convolve
    weights = n.arange(window, 0, -1.0)
    weights /= trinum(window)

    # created wma array with NaN values for indexes < window value
    weighted_moving_averages = n.empty(window - 1)
    weighted_moving_averages[:] = n.NAN

    # then append the wma's onto the end
    weighted_moving_averages = n.append(weighted_moving_averages, n.convolve(values, weights, 'valid'))

    return weighted_moving_averages


def trinum(num):
    # calculates the "triangular number" of a number
    # https://www.mathsisfun.com/algebra/triangular-numbers.html

    return num * (num + 1) / 2


def oanda_to_csv(oanda_output):
    oanda_list = list()
    for i, item in enumerate(oanda_output['candles']):
        d = {'complete': item['complete'],
             'volume': item['volume'],
             'time': item['time'],
             'open': item['mid']['o'],
             'high': item['mid']['h'],
             'low': item['mid']['l'],
             'close': item['mid']['c']}
        oanda_list.append(d)

    dataframe = pd.DataFrame(oanda_list)
    dataframe.to_csv(os.getcwd() + '\\oanda_data\\' + oanda_output['instrument'],
                     sep=',',
                     columns=['time', 'open', 'high', 'low', 'close'],
                     index=False)


    # feed = bt.feeds.GenericCSVData(dataname=os.getcwd() + '\data\{}.csv'.format(name),
    #                                open=open,
    #                                close=close,
    #                                high=high,
    #                                low=low,
    #                                volume=volume,
    #                                dtformat='%Y-%m-%d',
    #                                start_date=self.start_date,
    #                                end_date=self.end_date)





if __name__ == '__main__':
    test_data = candles(inst=['EUR_USD'], granularity=['D'], count=[20], From=None, to=None, price=None, nice=True)
    oanda_to_csv(test_data)

