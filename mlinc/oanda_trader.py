import numpy as n
import pandas as pd
import os
from mlinc.oanda_examples.candle_data import candles
from mlinc.notifier import notification
from mlinc.oanda_examples.instruments_list import instrument_list


file_jelle = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_jelle.txt'
file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'
file_christof = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_christof.txt'
file_vincent = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_vincent.txt'

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
    # print(values)
    # print(weights)
    weighted_moving_averages = n.append(weighted_moving_averages, n.convolve(values, weights, 'valid'))

    return weighted_moving_averages


def trinum(num):
    # calculates the "triangular number" of a number
    # https://www.mathsisfun.com/algebra/triangular-numbers.html

    return num * (num + 1) / 2


def rsi(prices, window):
    """ Relative Strength Index
    RSI < 30: Oversold, Potential rate increase -> Long
    RSI > 70: Overbought, Potential rate decrease -> Short
    RSI movement below the CL to above is seen as a rising trend
    RSI crossover from above the CL to below, indicates a falling trend

    Calculation:
    Relative Strength (RS) = average gain (gain_avg) / average loss (loss_avg)
    RSI = 100 - [100 / (1 + RS)]
    """

    deltas = n.diff(prices)
    seed = deltas[:window + 1]
    up = seed[seed>=0].sum() / window
    down = -seed[seed<0].sum() / window
    rs = up/down
    rsi = n.zeros_like(prices)
    rsi[:window] = 100.0 - (100.0 / (1.0 + rs))

    for i in range(window, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (window - 1) + upval) / window
        down = (down * (window - 1) + downval) / window

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi


def oanda_to_dataframe(oanda_output):
    oanda_list = list()
    for i, item in enumerate(oanda_output['candles']):
        d = {'complete': item['complete'],
             'volume': item['volume'],
             'time': item['time'],
             'open': float(item['mid']['o']),
             'high': float(item['mid']['h']),
             'low': float(item['mid']['l']),
             'close': float(item['mid']['c'])}
        oanda_list.append(d)

    dataframe = pd.DataFrame(oanda_list)
    return dataframe


def oanda_to_csv(oanda_output):
    dataframe = oanda_to_dataframe(oanda_output)
    dataframe.to_csv(os.getcwd() + '\\oanda_data\\' + oanda_output['instrument'],
                     sep=',',
                     columns=['time', 'open', 'high', 'low', 'close', 'volume'],
                     index=False)


def oanda_baconbuyer(inst, oanda_output, hma_window=14, rsi_window=14):
    dataframe = oanda_to_dataframe(oanda_output)

    df_hma = hma(n.array(dataframe['close'].tolist()), hma_window)
    dataframe['hma'] = pd.Series(df_hma, index=dataframe.index)

    df_rsi = rsi(n.array(dataframe['close'].tolist()), rsi_window)
    dataframe['rsi'] = pd.Series(df_rsi, index=dataframe.index)

    dataframe_days = dataframe.tail(10)
    rsi_min_days, rsi_max_days = (dataframe_days['rsi'].min(), dataframe_days['rsi'].max())
    hma_diff = dataframe_days.tail(7)['hma'].diff().reset_index()['hma']

    hma_5 = list(hma_diff.iloc[1:6])
    hma_1 = hma_diff.iloc[6]

    if rsi_max_days > 70 and all(item > 0 for item in hma_5) and hma_1 < 0:
        message = 'Go Short on {} because: (RSI: {} and HMA: {})'.format(inst,
                                                                         rsi_max_days,
                                                                         'Just Changed RiCo')
        notification(file_robert, message)
        print(message)
    elif rsi_min_days < 30 and all(item < 0 for item in hma_5) and hma_1 > 0:
        message = 'Go Long on {} because: (RSI: {} and HMA: {})'.format(inst,
                                                                        rsi_max_days,
                                                                        'Just Changed RiCo')
        notification(file_robert, message)
        print(message)

    return dataframe


if __name__ == '__main__':
    # test_data = candles(inst=['EUR_USD'], granularity=['D'], count=[50], From=None, to=None, price=None, nice=True)
    # df = oanda_baconbuyer('EUR_USD', test_data, hma_window=14, rsi_window=14)

    instr_list = instrument_list()
    for i in instr_list:
        test_data = candles(inst=[i], granularity=['D'], count=[50], From=None, to=None, price=None, nice=True)
        df = oanda_baconbuyer(i, test_data, hma_window=14, rsi_window=14)
        print(i)
