import datetime

import numpy as n
import pandas as pd
import re
import os
import json
import configparser

from mlinc.notifier import notification
from mlinc.oanda.instruments_list import instrument_list, custom_list

import oandapyV20
import oandapyV20.endpoints.orders as orders
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.transactions as transactions
import oandapyV20.endpoints.forexlabs as labs
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import warnings


# TODO: add normal SL in case price distance is not met
# TODO: Only send IFTTT message for opening position if v20 api sends confirmation (if not send returned error) (JtB)
# TODO: Also see developer's pdf:
# TODO: https://media.readthedocs.org/pdf/oanda-api-v20/latest/oanda-api-v20.pdf

file_jelle = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_jelle.txt'
file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'
file_christof = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_christof.txt'
file_vincent = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_vincent.txt'
file_bastijn = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_bastijn.txt'


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


def notify(message, send_notification, *args):
    if send_notification == 'True':
        if 'v' in args or 'vincent' in args:
            try:
                notification(file_vincent, message)
            except:
                print('vincent could not be reached')
        if 'b' in args or 'bastijn' in args:
            try:
                notification(file_bastijn, message)
            except:
                print('bastijn could not be reached')
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


def custom_list():
    """"
    This function contains an instrument list based on low spreads and low(er) risk coupling
    e.g. XAU_EUR and XAU_USD -> XAU_EUR removed
    """
    custom_inst = ['EUR_USD',
                   'GBP_USD',
                   'USD_CAD',
                   'USD_CHF',
                   'USD_JPY',
                   'AUD_USD',
                   'CAD_CHF',
                   'USD_HKD',
                   'BCO_USD',
                   'CAD_SGD',
                   'DE10YB_EUR',
                   'EU50_EUR',
                   'EUR_AUD',
                   'EUR_CAD',
                   'EUR_CHF',
                   'EUR_DKK',
                   'EUR_GBP',
                   'EUR_JPY',
                   'GBP_AUD',
                   'GBP_HKD',
                   'GBP_JPY',
                   'GBP_SGD',
                   'HKD_JPY',
                   'NZD_CAD',
                   'NZD_HKD',
                   'NZD_JPY',
                   'NZD_SGD',
                   'NZD_USD',
                   'SGD_CHF',
                   'SGD_HKD',
                   'SGD_JPY',
                   'USD_MXN',
                   'USD_SGD',
                   'XAU_USD',
                   'XCU_USD',
                   'SG30_SGD',
                   'HK33_HKD',
                   'AU200_AUD',
                   'IN50_USD',
                   'JP225_USD',
                   'SPX500_USD',
                   'UK10YB_GBP',
                   'USB10Y_USD',
                   ]

    return custom_inst


class OandaTrader(object):
    def __init__(self, instruments, **kwargs):
        account = kwargs.get('accountid') if kwargs.get('accountid') else None
        token = kwargs.get('token') if kwargs.get('token') else None
        self.accountID, self.access_token = (account, token)
        self.client = oandapyV20.API(access_token=self.access_token)
        if instruments == 'all':
            self.instruments = self.instrument_list
        else:
            self.instruments = instruments

        self.strategy = kwargs.get('strategy') if kwargs.get('strategy') else 'Baconbuyer'
        self.granularity = kwargs.get('granularity') if kwargs.get('granularity') else 'D'
        self.count = int(kwargs.get('count')) if kwargs.get('count') else 50
        self.hma_window = int(kwargs.get('hma_window')) if kwargs.get('hma_window') else 14
        self.rsi_window = int(kwargs.get('rsi_window')) if kwargs.get('rsi_window') else 14
        self.notify_who = list(kwargs.get('notify_who')) if kwargs.get('notify_who') else ['r', 'j', 'c', 'b', 'v']
        self.send_notification = kwargs.get('send_notification') if kwargs.get('send_notification') else 'False'
        self.rsi_max = float(kwargs.get('rsi_max')) if kwargs.get('rsi_max') else 70
        self.rsi_min = float(kwargs.get('rsi_min')) if kwargs.get('rsi_min') else 30
        self.max_margin_closeout_percent = float(kwargs.get('max_margin_closeout_percent')) \
            if kwargs.get('max_margin_closeout_percent') else 50
        self.max_exposure_percent = float(kwargs.get('max_exposure_percent')) if \
            kwargs.get('max_exposure_percent') else 0.6
        self.allow_simultaneous_trades = kwargs.get('allow_simultaneous_trades') \
            if kwargs.get('allow_simultaneous_trades') else 'True'
        self.rrr = float(kwargs.get('rrr')) if kwargs.get('rrr') else 3
        self.sl_multiplier = float(kwargs.get('sl_multiplier')) if kwargs.get('sl_multiplier') else 1
        self.tsl = kwargs.get('tsl') if kwargs.get('tsl') else 'Off'
        open_trades = self.get_open_trades()
        if self.allow_simultaneous_trades == 'False':
            self.instruments = self.neglect_open_trades(open_trades_list=open_trades, instrument_list=self.instruments)
        self.min_hma_slope = float(kwargs.get('min_hma_slope')) if kwargs.get('min_hma_slope') else 0

    @classmethod
    def from_conf_file(cls, instruments, conf):
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(conf)

        input = {}
        for item in config['OandaTraderInput']:
            input[item] = config['OandaTraderInput'][item]

        try:
            assert input['strategy']
            strategy = input['strategy']
            if strategy in ['Baconbuyer', 'Inverse_Baconbuyer']:
                pass
            else:
                raise ValueError(f'Strategy not possible...')
        except AssertionError:
            raise ValueError(f'Please provide a strategy in: {conf}')

        return cls(instruments, **input)

    @property
    def instrument_list(self):
        """
        Function to retrieve all tradable instruments from Oanda.

        Returns List with instrument codes
        -------
        """

        instr_list = []
        r = accounts.AccountInstruments(accountID=self.accountID)
        rv = self.client.request(r)

        for i in range(len(rv['instruments'])):
            instr_list.append(rv['instruments'][i]['name'])

        return instr_list

    def get_mid_price(self, instrument, api):
        params = {"instruments": instrument}
        r = oandapyV20.endpoints.pricing.PricingInfo(accountID=self.accountID, params=params)
        api.request(r)
        pricing = r.response['prices']
        bid_price = float(pricing[0]['bids'][0]['price'])
        ask_price = float(pricing[0]['asks'][0]['price'])
        return (bid_price + ask_price) / 2

    def get_trade_volume(self, SL, current_price, balance, max_exp, inst, api, account_cur='EUR'):
        # max exposure in balance currency (e.g. EUR)
        max_exp_cur = balance * max_exp / 100
        # difference between price and SL in pips (absolute value)
        SL_diff = 10000 * abs(SL - current_price)

        # case nr.1
        if account_cur == inst[-3:]:
            # for e.g. SILVER/EUR
            units = round(10000 * max_exp_cur / SL_diff)

        # case nr.2
        elif account_cur == inst[:3]:
            # for e.g. EUR
            units = round(10000 * current_price * max_exp_cur / SL_diff)

        # case nr.3
        elif account_cur not in inst and inst[4:] + '_' + account_cur in self.instrument_list:
            # test case inst='EUR_GBP', account_cur='USD'
            # conversion pair
            conv_pair = inst[4:] + '_' + account_cur
            # conversion pair exchange rate GBP/USD
            # price_conv_pair = 1.75 # baby pips example
            price_conv_pair = self.get_mid_price(conv_pair, api)
            # for e.g. EUR/GBP
            units = round(10000 * (1 / price_conv_pair) * max_exp_cur / SL_diff)

        # case nr.4
        elif account_cur not in inst and account_cur + '_' + inst[-3:] in self.instrument_list:
            # test case inst='USD_JPY', account_cur='CHF'
            # conversion pair
            conv_pair = account_cur + '_' + inst[-3:]
            # conversion pair exchange rate CHF/JPY
            # price_conv_pair = 85.00 # baby pips example
            price_conv_pair = self.get_mid_price(conv_pair, api)
            # for e.g. USD/JPY
            units = round(10000 * price_conv_pair * max_exp_cur / SL_diff)

        else:
            print('Oops, could not determine trade volume, '
                  'check if your instrument is tradable and conversion pair exists. \n'
                  '(e.g. USD_CNH is not possible, since conversion pair EUR_CNH or CNH_EUR does not exist in Oanda)\n'
                  'Please determine trading volume in web interface.')
            units = 0

        return units

    def candles(self, inst, From, to, price, nice):
        def check_date(s):
            dateFmt = "[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}Z"
            if not re.match(dateFmt, s):
                raise ValueError("Incorrect date format: ", s)
            return True

        if inst:
            params = {}
            if self.granularity:
                params.update({"granularity": self.granularity})
            if self.count:
                params.update({"count": self.count})
            if From and check_date(From):
                params.update({"from": From})
            if to and check_date(to):
                params.update({"to": to})
            if price:
                params.update({"price": price})
            for i in inst:
                r = instruments.InstrumentsCandles(instrument=i, params=params)
                rv = self.client.request(r)
                kw = {}
                if nice:
                    kw = {"indent": nice}
                # print("{}".format(json.dumps(rv, **kw)))
                return rv

    def data(self, instrument):
        try:
            data = self.candles(inst=[instrument],
                                From=None, to=None, price=None, nice=True)
            return data
        except:
            raise ValueError('Failed to load data from Oanda using instrument {}'.format(instrument))

    def data_as_dataframe(self, instrument):
        oanda_list = list()
        for i, item in enumerate(self.data(instrument)['candles']):
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

    def save_data_to_csv(self, instrument):
        dataframe = self.data_as_dataframe(instrument)
        dataframe.to_csv(os.getcwd() + '\\oanda_data\\' + self.data(instrument)['instrument'],
                         sep=',',
                         columns=['time', 'open', 'high', 'low', 'close', 'volume'],
                         index=False,
                         )

    def baconbuyer(self, instrument):
        dataframe = self.data_as_dataframe(instrument)

        df_hma = hma(n.array(dataframe['close'].tolist()), self.hma_window)
        dataframe['hma'] = pd.Series(df_hma, index=dataframe.index)

        df_rsi = rsi(n.array(dataframe['close'].tolist()), self.rsi_window)
        dataframe['rsi'] = pd.Series(df_rsi, index=dataframe.index)

        rsi_min_days, rsi_max_days = (dataframe.tail(10)['rsi'].min(), dataframe.tail(10)['rsi'].max())
        hma_diff = dataframe['hma'].diff().reset_index()['hma'].tolist()

        if rsi_max_days > self.rsi_max and all(item > 0 for item in hma_diff[-7:-2]) and hma_diff[-2] < 0:
            sl = dataframe.tail(7)['hma'].max()
            close = float(dataframe.tail(1)['close'])
            tp = close - (sl - close) / self.rrr
            nr_decimals_close = str(close)[::-1].find('.')

            message = 'Possibility to go Short on {} because: RSI was > {} ({}) and HMA just peaked on {} chart. \n' \
                      'BaconBuyer recommends a stop loss of {} and a take profit of {}, good luck!'. \
                format(instrument,
                       self.rsi_max,
                       int(rsi_max_days),
                       self.granularity,
                       format(sl, '.' + str(nr_decimals_close) + 'f'),
                       format(tp, '.' + str(nr_decimals_close) + 'f'))

            notify(message, self.send_notification, *self.notify_who)
            print(dataframe.tail(10))
            print(message)

        elif rsi_min_days < self.rsi_min and all(item < 0 for item in hma_diff[-7:-2]) and hma_diff[-2] > 0:
            sl = dataframe.tail(7)['hma'].min()
            close = float(dataframe.tail(1)['close'])
            tp = (close - sl) / self.rrr + close
            nr_decimals_close = str(close)[::-1].find('.')

            message = 'Possibility to go Long on {} because: RSI was < {} ({}) and HMA just dipped on {} chart. \n' \
                      'BaconBuyer recommends a stop loss of {} and a take profit of {}, good luck!'. \
                format(instrument,
                       self.rsi_min,
                       int(rsi_min_days),
                       self.granularity,
                       format(sl, '.' + str(nr_decimals_close) + 'f'),
                       format(tp, '.' + str(nr_decimals_close) + 'f'))

            notify(message, self.send_notification, *self.notify_who)
            print(dataframe.tail(10))
            print(message)

        return dataframe

    def baconbuyer_auto(self, instrument):
        dataframe = self.data_as_dataframe(instrument)

        df_hma = hma(n.array(dataframe['close'].tolist()), self.hma_window)
        dataframe['hma'] = pd.Series(df_hma, index=dataframe.index)

        df_rsi = rsi(n.array(dataframe['close'].tolist()), self.rsi_window)
        dataframe['rsi'] = pd.Series(df_rsi, index=dataframe.index)

        rsi_min_days, rsi_max_days = (dataframe.tail(10)['rsi'].min(), dataframe.tail(10)['rsi'].max())
        hma_diff = dataframe['hma'].diff().reset_index()['hma'].tolist()

        print(datetime.datetime.now())
        print(dataframe.tail(10))
        print(hma_diff[-7:-1])

        # log if hma_diff between 0 and threshold
        if all(item > 0 for item in hma_diff[-7:-2]) and 0 > hma_diff[-2] > -self.min_hma_slope:
            print(f"short position not opened because threshold value of  {self.min_hma_slope} not met")
            print(f"hma_diff = {round(hma_diff[-2], 5)}")
        if all(item < 0 for item in hma_diff[-7:-2]) and 0 < hma_diff[-2] < self.min_hma_slope:
            print(f"long position not opened because threshold value of {self.min_hma_slope} not met")
            print(f"hma_diff = {round(hma_diff[-2], 5)}")

        # conditions to go short
        if all(item > 0 for item in hma_diff[-7:-2]) and hma_diff[-2] < -self.min_hma_slope:
            # set half spread (prices are all 'mid', avg of bid and ask)
            spread = self.get_spread(instrument)
            half_spread = 0.5*spread
            # set stoploss
            sl = dataframe.tail(7)['hma'].max()
            close = float(dataframe.tail(1)['close'])
            # sl_mult sets SL further away from price
            # sl_multiplier=1 -> SL on hma like usual, sl_multiplier=2 -> SL twice as far away
            sl_dist = (sl - close) * (self.sl_multiplier - 1)
            sl += sl_dist
            # set take profit
            tp = close - (sl - close) / self.rrr
            # account for spreads
            sl += spread
            tp -= spread
            # format sl and tp
            nr_decimals_close = str(close)[::-1].find('.')
            sl = float(format(sl, '.' + str(nr_decimals_close) + 'f'))
            tp = float(format(tp, '.' + str(nr_decimals_close) + 'f'))

            if self.margin_closeout_percent() < self.max_margin_closeout_percent:
                if self.tsl == 'On':
                    self.tsl_order(sl, tp, close, instrument, 'short', self.max_exposure_percent)
                    message = 'Fritsie just opened a Short position on {} with TSL={} and TP={} ' \
                              'because: HMA just peaked on {} chart. \n' \
                              'BaconBuyer used a RRR={}'. \
                        format(instrument,
                               sl,
                               tp,
                               self.granularity,
                               self.rrr)
                else:
                    self.market_order(sl, tp, close, instrument, 'short', self.max_exposure_percent)
                    message = 'Fritsie just opened a Short position on {} with SL={} and TP={} ' \
                              'because: HMA just peaked on {} chart. \n' \
                              'BaconBuyer used a RRR={}'. \
                        format(instrument,
                               sl,
                               tp,
                               self.granularity,
                               self.rrr)
                notify(message, self.send_notification, *self.notify_who)
                print(dataframe.tail(10))
                print(message)
            else:
                notify('Position not opened due to insufficient margin', self.send_notification, *self.notify_who)

        # conditions to go long
        elif all(item < 0 for item in hma_diff[-7:-2]) and hma_diff[-2] > self.min_hma_slope:
            # set half spread (prices are all 'mid', avg of bid and ask)
            spread = self.get_spread(instrument)
            half_spread = 0.5*spread
            # set stoploss
            sl = dataframe.tail(7)['hma'].min()
            close = float(dataframe.tail(1)['close'])
            # sl_mult sets SL further away from price
            # sl_multiplier=1 -> SL on hma like usual, sl_multiplier=2 -> SL twice as far away
            sl_dist = (close - sl) * (self.sl_multiplier - 1)
            sl -= sl_dist
            # set take profit
            tp = (close - sl) / self.rrr + close
            # account for spreads
            sl -= spread
            tp += spread
            # format sl and tp
            nr_decimals_close = str(close)[::-1].find('.')
            sl = float(format(sl, '.' + str(nr_decimals_close) + 'f'))
            tp = float(format(tp, '.' + str(nr_decimals_close) + 'f'))

            if self.margin_closeout_percent() < self.max_margin_closeout_percent:
                if self.tsl == 'On':
                    self.tsl_order(sl, tp, close, instrument, 'long', self.max_exposure_percent)
                    message = 'Fritsie just opened a Long position on {} with TSL={} and TP={} ' \
                              'because: HMA just dipped on {} chart. \n' \
                              'BaconBuyer used a RRR={}'. \
                        format(instrument,
                               sl,
                               tp,
                               self.granularity,
                               self.rrr)
                else:
                    self.market_order(sl, tp, close, instrument, 'long', self.max_exposure_percent)
                    message = 'Fritsie just opened a Long position on {} with SL={} and TP={} ' \
                              'because: HMA just dipped on {} chart. \n' \
                              'BaconBuyer used a RRR={}'. \
                        format(instrument,
                               sl,
                               tp,
                               self.granularity,
                               self.rrr)
                notify(message, self.send_notification, *self.notify_who)
                print(dataframe.tail(10))
                print(message)
            else:
                notify('Position not opened due to insufficient margin', self.send_notification, *self.notify_who)

        return dataframe

    def inverse_baconbuyer_auto(self, instrument):
        dataframe = self.data_as_dataframe(instrument)

        df_hma = hma(n.array(dataframe['close'].tolist()), self.hma_window)
        dataframe['hma'] = pd.Series(df_hma, index=dataframe.index)

        df_rsi = rsi(n.array(dataframe['close'].tolist()), self.rsi_window)
        dataframe['rsi'] = pd.Series(df_rsi, index=dataframe.index)

        rsi_min_days, rsi_max_days = (dataframe.tail(10)['rsi'].min(), dataframe.tail(10)['rsi'].max())
        hma_diff = dataframe['hma'].diff().reset_index()['hma'].tolist()

        # conditions to go long (high rsi and hma local minimum)
        if rsi_max_days > self.rsi_max and all(item > 0 for item in hma_diff[-7:-2]) and hma_diff[-2] < 0:
            # set half spread (prices are all 'mid', avg of bid and ask)
            spread = self.get_spread(instrument)
            half_spread = 0.5*spread
            # set take profit
            tp = dataframe.tail(7)['hma'].max()
            close = float(dataframe.tail(1)['close'])
            # set stop loss
            sl = (close - tp) / self.rrr + close
            sl -= spread
            tp += spread
            nr_decimals_close = str(close)[::-1].find('.')
            sl = float(format(sl, '.' + str(nr_decimals_close) + 'f'))
            tp = float(format(tp, '.' + str(nr_decimals_close) + 'f'))

            if self.margin_closeout_percent() < self.max_margin_closeout_percent:
                self.market_order(sl, tp, close, instrument, 'long', self.max_exposure_percent)
                message = 'Fritsie just opened a Long position on {} with SL={} and TP={} ' \
                          'because: RSI was > {} ({}) and HMA just peaked on {} chart. \n' \
                          'Inverse BaconBuyer used a RRR={}'. \
                    format(instrument,
                           sl,
                           tp,
                           self.rsi_max,
                           int(rsi_min_days),
                           self.granularity,
                           self.rrr)
                notify(message, self.send_notification, *self.notify_who)
                print(dataframe.tail(10))
                print(message)
            else:
                notify('Position not opened due to insufficient margin', self.send_notification, *self.notify_who)

        # conditions to go short (low rsi and hma local maximum)
        elif rsi_min_days < self.rsi_min and all(item < 0 for item in hma_diff[-7:-2]) and hma_diff[-2] > 0:
            # set half spread (prices are all 'mid', avg of bid and ask)
            spread = self.get_spread(instrument)
            half_spread = 0.5*spread
            # set take profit
            tp = dataframe.tail(7)['hma'].min()
            close = float(dataframe.tail(1)['close'])
            # set take stop loss
            sl = close - (tp - close) / self.rrr
            sl += spread
            tp -= spread
            nr_decimals_close = str(close)[::-1].find('.')
            sl = float(format(sl, '.' + str(nr_decimals_close) + 'f'))
            tp = float(format(tp, '.' + str(nr_decimals_close) + 'f'))

            if self.margin_closeout_percent() < self.max_margin_closeout_percent:
                self.market_order(sl, tp, close, instrument, 'short', self.max_exposure_percent)
                message = 'Fritsie just opened a Short position on {} with SL={} and TP={} ' \
                          'because: RSI was < {} ({}) and HMA just dipped on {} chart. \n' \
                          'BaconBuyer used a RRR={}'. \
                    format(instrument,
                           sl,
                           tp,
                           self.rsi_min,
                           int(rsi_min_days),
                           self.granularity,
                           self.rrr)
                notify(message, self.send_notification, *self.notify_who)
                print(dataframe.tail(10))
                print(message)
            else:
                notify('Position not opened due to insufficient margin', self.send_notification, *self.notify_who)

        return dataframe

    def analyse(self):
        if self.strategy == 'Baconbuyer':
            for instrument in self.instruments:
                print(instrument)
                self.baconbuyer(instrument=instrument)

    def auto_trade(self):
        for instrument in self.instruments:
            print(instrument)
            if self.strategy == 'Inverse_Baconbuyer':
                self.inverse_baconbuyer_auto(instrument)
            elif self.strategy == 'Baconbuyer':
                self.baconbuyer_auto(instrument)

    def market_order(self, sl, tp, close, inst, short_long, max_exp):

        # short/long order
        if short_long == 'short':
            sign = -1
        elif short_long == 'long':
            sign = 1
        else:
            raise ValueError('unclear if long or short')
        balance = self.account_balance()
        volume = sign*self.get_trade_volume(sl, close, balance, max_exp, inst, self.client)

        # set correct nr of decimals
        nr_decimals_close = str(close)[::-1].find('.')

        orderConf = [
            {
                "order": {
                    "units": volume,
                    "instrument": inst,
                    "stopLossOnFill": {
                        "timeInForce": "GTC",
                        "price": format(sl, '.' + str(nr_decimals_close) + 'f')
                    },
                    "takeProfitOnFill": {
                        "timeInForce": "GTC",
                        "price": format(tp, '.' + str(nr_decimals_close) + 'f')
                    },
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
        ]

        # create and process order requests
        for O in orderConf:

            r = orders.OrderCreate(accountID=self.accountID, data=O)
            print("processing : {}".format(r))
            print("===============================")
            print(r.data)
            try:
                response = self.client.request(r)
            except V20Error as e:
                print("V20Error: {}".format(e))
            else:
                print("Response: {}\n{}".format(r.status_code,
                                                json.dumps(response, indent=2)))
            try:
                tradeID = response["orderFillTransaction"]["id"]
            except:
                print('No trade ID available. Trade not opened')

    def tsl_order(self, sl, tp, close, inst, short_long, max_exp):
        """"
        This function gives a market order, followed by an order
        to add a trailing stop loss (tsl).
        The tsl distance to current price should be set and a trade ID should be given.
        """
        # short/long order
        if short_long == 'short':
            sign = -1
        elif short_long == 'long':
            sign = 1
        else:
            raise ValueError('unclear if long or short')
        balance = self.account_balance()
        volume = sign*self.get_trade_volume(sl, close, balance, max_exp, inst, self.client)

        # set correct nr of decimals
        nr_decimals_close = str(close)[::-1].find('.')

        orderConf = [
            {
                "order": {
                    "units": volume,
                    "instrument": inst,
                    # "takeProfitOnFill": {
                    #     "timeInForce": "GTC",
                    #     "price": format(tp, '.' + str(nr_decimals_close) + 'f')
                    # },
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
        ]

        # create and process order requests
        # place market order
        for O in orderConf:
            r = orders.OrderCreate(accountID=self.accountID, data=O)
            print("processing : {}".format(r))
            print("===============================")
            print(r.data)
            try:
                response = self.client.request(r)
            except V20Error as e:
                print("V20Error: {}".format(e))
            else:
                print("Response: {}\n{}".format(r.status_code,
                                                json.dumps(response, indent=2)))
            try:
                tradeID = int(response["orderFillTransaction"]["id"])
            except:
                print('No trade ID available. Trade not opened')

        tsl_distance = abs(sl - close)

        orderConf2 = {
                            "order": {
                                "type": "TRAILING_STOP_LOSS",
                                "tradeID": str(tradeID),
                                "timeInForce": "GTC",
                                "distance": format(tsl_distance, '.' + str(nr_decimals_close) + 'f')
                            }
                        }

        r = orders.OrderCreate(accountID=self.accountID, data=orderConf2)
        try:
            response = self.client.request(r)
        except V20Error as e:
            print("V20Error: {}".format(e))
        else:
            # add normal SL and TP in case min price distance is not met
            print(r.response)

    def account_balance(self):
        r = accounts.AccountDetails(accountID=self.accountID)
        rv = self.client.request(r)
        details = rv.get('account')
        balance = float(details.get('NAV'))
        return balance

    def margin_closeout_percent(self):
        r = accounts.AccountDetails(accountID=self.accountID)
        rv = self.client.request(r)
        details = rv.get('account')
        margin_percent = 100*float(details.get('marginCloseoutPercent'))
        return margin_percent

    def get_spread(self, instrument):
        api = oandapyV20.API(access_token=self.access_token)
        test = self.candles(inst=[instrument], From=None, to=None, price=['BA'], nice=True)
        bid = float(test['candles'][0]['bid']['c'])
        ask = float(test['candles'][0]['ask']['c'])
        spread = float(format(ask-bid, '.5f'))
        return spread

    def get_open_trades(self):
        r = trades.OpenTrades(accountID=self.accountID)
        self.client.request(r)
        return r.response

    @staticmethod
    def neglect_open_trades(open_trades_list, instrument_list):
        open_trades = open_trades_list['trades']

        for open_trade in open_trades:
            instrument = open_trade['instrument']
            try:
                idx = instrument_list.index(instrument)
            except:
                pass
            else:
                warnings.warn('One or more instruments deleted from instrument list due to open positions')
                del instrument_list[idx]
        return instrument_list

    def get_closed_trades(self, date):
        r = trades.TradesList(accountID=self.accountID, params={'state': 'CLOSED',
                                                                'count': 100})
        self.client.request(r)
        df = pd.DataFrame(list(r.response['trades']))
        df['closeTime'] = pd.to_datetime(df['closeTime'], errors='coerce')
        df['realizedPL'] = pd.to_numeric(df['realizedPL'], errors='coerce')
        return df.loc[df['closeTime'].dt.day == date.day]

    def get_all_trades(self):
        r = trades.TradesList(accountID=self.accountID, params={'count': 500,
                                                                'state': 'CLOSED'})
        self.client.request(r)
        df = pd.DataFrame(list(r.response['trades']))
        df['closeTime'] = pd.to_datetime(df['closeTime'], errors='coerce')
        df['realizedPL'] = pd.to_numeric(df['realizedPL'], errors='coerce')
        return df

    def result_summary(self, date):
        data = self.get_closed_trades(date)

        balance = data['realizedPL'].sum()
        total_balance = self.account_balance()

        message = 'Today\'s P/L = {:.2f} euro \n' \
                  'Total Account Balance = {:.2f}'.format(balance, total_balance)
        print(message)

        notify(message, 'True', *self.notify_who)


if __name__ == '__main__':
    # Set auto_trade to On or Off in conf.ini. If off fritsie will only send out notifications for opportunities.
    # Start auto-trader

    message_fritsie = 'Fritsie is looking if he can open some positions'
    notify(message_fritsie, False)

    trader = OandaTrader.from_conf_file(['BCO_USD'],
                                        r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\oanda\conf_files\conf.ini')
    # trader = OandaTrader.from_conf_file(custom_list(),
    #                                     r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\oanda\conf_files\conf.ini')

    # save data to csv
    # trader.save_data_to_csv('BCO_USD')

    # auto trade
    trader.auto_trade()


