import numpy as n
import pandas as pd
import os
from mlinc.oanda_examples.candle_data import candles
from mlinc.notifier import notification
from mlinc.position_size_calc import *
import json
import oandapyV20.endpoints.orders as orders
from oandapyV20.exceptions import V20Error

# redundant packages:
# from oandapyV20 import API
# import logging
# import oandapyV20.endpoints.accounts as accounts

# TODO: make settings file (e.g. .ini bestand) such as maximum exposure percentage, max margin percentage
# TODO: Market order and position size calculator use 'mid' price (avg of bid and ask).
# TODO: Should either be bid or ask depending on short or long position. On Daily chart no issue
# TODO: Also see developer's pdf:
# TODO: https://media.readthedocs.org/pdf/oanda-api-v20/latest/oanda-api-v20.pdf

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


def notify(message, *args):
    if 'v' in args or 'vincent' in args:
        try:
            notification(file_vincent, message)
        except:
            print('vincent could not be reached')
    # if 'b' in args or 'bastijn' in args:
    #     try:
    #         notification(file_bastijn, message)
    #     except:
    #         print('bastijn could not be reached')
    if 'c' in args or 'christof' in args:
        try:
            notification(file_christof, message)
        except:
            print('christof could not be reached')
    if 'r' in args or 'robert' in args:
        try:
            notification(file_robert, message)
        except:
            print('robert could not be reached')
    if 'j' in args or 'jelle' in args:
        try:
            notification(file_jelle, message)
        except:
            print('jelle could not be reached')


class OandaTrader(object):
    id = 0
    instruments = []

    def __init__(self, instrument, granularity='D', count=50, **kwargs):
        self.accountID, self.access_token = exampleAuth()
        self.instrument = instrument
        self.granularity = granularity
        self.count = count

        self.hma_window = kwargs.get('hma_window') if kwargs.get('hma_window') else 14
        self.rsi_window = kwargs.get('rsi_window') if kwargs.get('rsi_window') else 14

        self.strategy = kwargs.get('strategy') if kwargs.get('strategy') else 'Baconbuyer'

        self.rrr = kwargs.get('rrr') if kwargs.get('rrr') else 3
        self.api = oandapyV20.API(access_token=self.access_token)

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
                           From=None, to=None, price=None, nice=True,
                           access_token=self.access_token)
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

        rsi_min_days, rsi_max_days = (dataframe.tail(10)['rsi'].min(), dataframe.tail(10)['rsi'].max())
        hma_diff = dataframe['hma'].diff().reset_index()['hma'].tolist()

        if rsi_max_days > 70 and all(item > 0 for item in hma_diff[-7:-2]) and hma_diff[-2] < 0:
            sl = dataframe.tail(7)['hma'].max()
            close = float(dataframe.tail(1)['close'])
            tp = close - (sl - close) / self.rrr
            nr_decimals_close = str(close)[::-1].find('.')

            message = 'Possibility to go Short on {} because: RSI was > 70 ({}) and HMA just peaked on {} chart. \n' \
                      'BaconBuyer recommends a stop loss of {} and a take profit of {}, good luck!'. \
                format(self.instrument,
                       int(rsi_max_days),
                       self.granularity,
                       round(sl, nr_decimals_close),
                       round(tp, nr_decimals_close))

            notify(message, 'j', 'r', 'c', 'v')
            print(dataframe.tail(10))
            print(message)

        elif rsi_min_days < 30 and all(item < 0 for item in hma_diff[-7:-2]) and hma_diff[-2] > 0:
            sl = dataframe.tail(7)['hma'].min()
            close = float(dataframe.tail(1)['close'])
            tp = (close - sl) / self.rrr + close
            nr_decimals_close = str(close)[::-1].find('.')

            message = 'Possibility to go Long on {} because: RSI was < 30 ({}) and HMA just dipped on {} chart. \n' \
                      'BaconBuyer recommends a stop loss of {} and a take profit of {}, good luck!'. \
                format(self.instrument,
                       int(rsi_min_days),
                       self.granularity,
                       round(sl, nr_decimals_close),
                       round(tp, nr_decimals_close))

            notify(message, 'j', 'r', 'c', 'v')
            print(dataframe.tail(10))
            print(message)

        return dataframe

    def baconbuyer_auto(self):
        dataframe = self.data_as_dataframe

        df_hma = hma(n.array(dataframe['close'].tolist()), self.hma_window)
        dataframe['hma'] = pd.Series(df_hma, index=dataframe.index)

        df_rsi = rsi(n.array(dataframe['close'].tolist()), self.rsi_window)
        dataframe['rsi'] = pd.Series(df_rsi, index=dataframe.index)

        rsi_min_days, rsi_max_days = (dataframe.tail(10)['rsi'].min(), dataframe.tail(10)['rsi'].max())
        hma_diff = dataframe['hma'].diff().reset_index()['hma'].tolist()

        if rsi_max_days > 70 and all(item > 0 for item in hma_diff[-7:-2]) and hma_diff[-2] < 0:
            sl = dataframe.tail(7)['hma'].max()
            close = float(dataframe.tail(1)['close'])
            tp = close - (sl - close) / self.rrr
            nr_decimals_close = str(close)[::-1].find('.')

            if self.margin_closeout_percent() < 50:
                self.market_order(sl, tp, close, self.instrument, short_long='short')
                message = 'Fritsie just opened a Short position on {} with SL={} and TP={} ' \
                          'because: RSI was > 70 ({}) and HMA just peaked on {} chart. \n' \
                          'BaconBuyer used a RRR={}'. \
                    format(self.instrument,
                           round(sl, nr_decimals_close),
                           round(tp, nr_decimals_close),
                           int(rsi_min_days),
                           self.granularity,
                           self.rrr)
                # notify(message, 'j', 'r', 'c', 'v')
                notify(message, 'j')
                print(dataframe.tail(10))
                print(message)
            else:
                notify('Position not opened due to insufficient margin', 'j', 'r', 'c', 'v')

        elif rsi_min_days < 30 and all(item < 0 for item in hma_diff[-7:-2]) and hma_diff[-2] > 0:
            sl = dataframe.tail(7)['hma'].min()
            close = float(dataframe.tail(1)['close'])
            tp = (close - sl) / self.rrr + close
            nr_decimals_close = str(close)[::-1].find('.')

            if self.margin_closeout_percent() < 50:
                self.market_order(sl, tp, close, self.instrument, short_long='long')
                message = 'Fritsie just opened a Long position on {} with SL={} and TP={} ' \
                          'because: RSI was < 30 ({}) and HMA just dipped on {} chart. \n' \
                          'BaconBuyer used a RRR={}'. \
                    format(self.instrument,
                           round(sl, nr_decimals_close),
                           round(tp, nr_decimals_close),
                           int(rsi_min_days),
                           self.granularity,
                           self.rrr)
                # notify(message, 'j', 'r', 'c', 'v')
                notify(message, 'j')
                print(dataframe.tail(10))
                print(message)
            else:
                notify('Position not opened due to insufficient margin', 'j', 'r', 'c', 'v')

        return dataframe

    def analyse(self):
        if self.strategy == 'Baconbuyer':
            return self.baconbuyer()

    def auto_trade(self):
        if self.strategy == 'Baconbuyer':
            return self.baconbuyer_auto()

    def market_order(self, sl, tp, close, inst, short_long, max_exp=0.1):

        # built in logging function:
        # logging.basicConfig(
        #     filename="log.out",
        #     level=logging.INFO,
        #     format='%(asctime)s [%(levelname)s] %(instrument)s : %(message)s',
        # )

        # short/long order
        if short_long == 'short':
            sign = -1
        elif short_long == 'long':
            sign = 1
        else:
            raise ValueError('unclear if long or short')
        balance = self.account_balance()
        volume = sign*get_trade_volume(sl, close, balance, max_exp, inst, self.api)

        # set correct nr of decimals (dirty trick, but it works)
        nr_decimals_close = str(close)[::-1].find('.')
        sl = round(sl, nr_decimals_close)
        tp = round(tp, nr_decimals_close)
        sl = sl - sl % (10 ** -nr_decimals_close)
        tp = tp - tp % (10 ** -nr_decimals_close)

        orderConf = [
            {
                "order": {
                    "units": volume,
                    "instrument": inst,
                    "stopLossOnFill": {
                        "timeInForce": "GTC",
                        "price": sl
                    },
                    "takeProfitOnFill": {
                        "timeInForce": "GTC",
                        "price": tp
                    },
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
        ]

        # client

        # create and process order requests
        for O in orderConf:

            r = orders.OrderCreate(accountID=self.accountID, data=O)
            print("processing : {}".format(r))
            print("===============================")
            print(r.data)
            try:
                response = self.api.request(r)
            except V20Error as e:
                print("V20Error: {}".format(e))
            else:
                print("Response: {}\n{}".format(r.status_code,
                                                json.dumps(response, indent=2)))

    def account_balance(self):
        import oandapyV20.endpoints.accounts as accounts
        r = accounts.AccountDetails(accountID=self.accountID)
        rv = self.api.request(r)
        details = rv.get('account')
        balance = float(details.get('NAV'))
        return balance

    def margin_closeout_percent(self):
        import oandapyV20.endpoints.accounts as accounts
        r = accounts.AccountDetails(accountID=self.accountID)
        rv = self.api.request(r)
        details = rv.get('account')
        margin_percent = 100*float(details.get('marginCloseoutPercent'))
        return margin_percent


if __name__ == '__main__':

    # # Run notifier
    # message_fritsie = 'This is your daily update from Fritsie'
    # notify(message_fritsie, 'j', 'r', 'c', 'v')
    # class_list = []
    # for inst in instrument_list():
    #     trader = OandaTrader(inst, granularity='D')
    #     class_list.append(trader)
    #     trader.analyse()
    #     print(trader.instrument)
    # # trader = OandaTrader('GBP_CHF')
    # # trader.analyse()

    # Start auto-trader
    message_fritsie = 'Fritsie is looking if he can open some positions'
    # notify(message_fritsie, 'j', 'r', 'c', 'v')
    notify(message_fritsie, 'j')
    class_list = []
    for inst in instrument_list():
        trader = OandaTrader(inst, granularity='D')
        class_list.append(trader)
        trader.auto_trade()
        print(trader.instrument)

