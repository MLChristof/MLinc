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

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


def hma(values, window):
    period = int(n.sqrt(window))

    wma1 = 2 * wma(values, n.int(window/2))
    wma2 = wma(values, window)

    hull_moving_averages = wma((wma1 - wma2), period)

    return hull_moving_averages


def wma(values, window):
    weights = n.arange(window, 0, -1.0)
    weights /= trinum(window)

    # created wma array with NaN values for indexes < window value
    weighted_moving_averages = n.empty(window - 1)
    weighted_moving_averages[:] = n.NAN

    weighted_moving_averages = n.append(weighted_moving_averages, n.convolve(values, weights, 'valid'))

    return weighted_moving_averages


def trinum(num):
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


class OandaTrader(object):
    id = 0
    instruments = []

    def __init__(self, instrument, granularity='D', count=50, **kwargs):
        self.instrument = instrument
        self.granularity = granularity
        self.count = count

        self.hma_window = kwargs.get('hma_window') if kwargs.get('hma_window') else 14
        self.rsi_window = kwargs.get('rsi_window') if kwargs.get('rsi_window') else 14

        self.strategy = kwargs.get('strategy') if kwargs.get('strategy') else 'Baconbuyer'

        OandaTrader.instruments.append(self.instrument)
        OandaTrader.id += 1

    @property
    def instrument(self):
        return self.__instrument

    @instrument.setter
    def instrument(self, instrument):
        count_instrument = "Instrument_%i" % self.id

        if instrument is None:
            self.__instrument = count_instrument
        elif instrument in OandaTrader.instruments:
            raise UserWarning("Instrument '{}' already in use, instrument given is {}.".format(
                instrument, count_instrument))
        else:
            self.__instrument = instrument

    @property
    def data(self):
        try:
            data = candles(inst=[self.instrument],
                           granularity=[self.granularity],
                           count=[self.count],
                           From=None, to=None, price=None, nice=True)
            return data
        except:
            raise ValueError('Failed to load data from Oanda using instrument {}'.format(self.instrument))

    @property
    def data_as_dataframe(self):
        oanda_list = list()
        for i, item in enumerate(self.data['candles']):
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

    def save_data_to_csv(self):
        dataframe = self.data_as_dataframe
        dataframe.to_csv(os.getcwd() + '\\oanda_data\\' + self.data['instrument'],
                         sep=',',
                         columns=['time', 'open', 'high', 'low', 'close', 'volume'],
                         index=False)

    def baconbuyer(self):
        dataframe = self.data_as_dataframe

        df_hma = hma(n.array(dataframe['close'].tolist()), self.hma_window)
        dataframe['hma'] = pd.Series(df_hma, index=dataframe.index)

        df_rsi = rsi(n.array(dataframe['close'].tolist()), self.rsi_window)
        dataframe['rsi'] = pd.Series(df_rsi, index=dataframe.index)

        dataframe_days = dataframe.tail(10)
        rsi_min_days, rsi_max_days = (dataframe_days['rsi'].min(), dataframe_days['rsi'].max())
        hma_diff = dataframe_days.tail(7)['hma'].diff().reset_index()['hma']

        hma_5 = list(hma_diff.iloc[1:6])
        hma_1 = hma_diff.iloc[6]

        if rsi_max_days > 70 and all(item > 0 for item in hma_5) and hma_1 < 0:
            message = 'Possibility to go Short on {} because: RSI was > 70 ({}) and HMA just peaked on {} chart.'. \
                format(self.instrument, int(rsi_max_days), self.granularity)

            # notification(file_robert, message)
            # notification(file_vincent, message)
            # notification(file_christof, message)
            # notification(file_jelle, message)
            print(dataframe_days)
            print(message)

        elif rsi_min_days < 30 and all(item < 0 for item in hma_5) and hma_1 > 0:
            message = 'Possibility to go Long on {} because: RSI was < 30 ({}) and HMA just dipped on {} chart.'. \
                format(self.instrument, int(rsi_min_days), self.granularity)

            # notification(file_robert, message)
            # notification(file_vincent, message)
            # notification(file_christof, message)
            # notification(file_jelle, message)
            print(dataframe_days)
            print(message)

        return dataframe

    def analyse(self):
        if self.strategy == 'Baconbuyer':
            return self.baconbuyer()


if __name__ == '__main__':
    class_list = []
    for inst in instrument_list():
        trader = OandaTrader(inst)
        class_list.append(trader)
        trader.analyse()
        print(trader.instrument)




