import numpy as n
import pandas as pd


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


if __name__ == '__main__':
    pass