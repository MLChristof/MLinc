from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')
# import datetime
# import os.path
# import sys
# import time
import numpy as n

import backtrader as bt


class BaconBuyerStrategy(bt.Strategy):
    # TODO Add smart staking/sizing
    # TODO Check Commission settings
    params = (
        ('maperiod', 14),
        ('RRR', 1),
        ('SL_multiplier', 1.02),
        ('stakepercent', 1),
        ('min_hma_slope', 0.00154)
    )

    # smart sizer
    # always loose or win set amount in account balance currency (max exposure in percent may varies per trade)
    def get_trade_volume(self, SL, current_price, balance, inst, mid_price, account_cur='EUR'):
        mult = self.broker.comminfo[None].params.mult
        # max exposure in balance currency (e.g. EUR)
        max_exp_cur = (1/mult) * balance * self.params.stakepercent / 100
        # difference between price and SL in pips (absolute value)
        SL_diff = 10000 * abs(SL - current_price)
        # prevent devision by zero error
        if SL_diff == 0:
            SL_diff = 1E-10

        # case nr.1
        if account_cur == inst[-3:]:
            # for e.g. SILVER/EUR
            units = round(10000 * max_exp_cur / SL_diff)

        # case nr.2
        elif account_cur == inst[:3]:
            # for e.g. EUR
            units = round(10000 * current_price * max_exp_cur / SL_diff)

        # case nr.3
        elif account_cur not in inst and str(inst[4:]) + '_' + account_cur in self.instrument_list():
            # test case inst='EUR_GBP', account_cur='USD'
            # conversion pair
            conv_pair = inst[4:] + '_' + account_cur
            # conversion pair exchange rate GBP/USD
            # price_conv_pair = 1.75 # baby pips example
            price_conv_pair = mid_price
            # for e.g. EUR/GBP
            units = round(10000 * (1 / price_conv_pair) * max_exp_cur / SL_diff)

        # case nr.4
        elif account_cur not in inst and account_cur + '_' + str(inst[-3:]) in self.instrument_list():
            # test case inst='USD_JPY', account_cur='CHF'
            # conversion pair
            conv_pair = account_cur + '_' + inst[-3:]
            # conversion pair exchange rate CHF/JPY
            # price_conv_pair = 85.00 # baby pips example
            price_conv_pair = mid_price
            # for e.g. USD/JPY
            units = round(10000 * price_conv_pair * max_exp_cur / SL_diff)

        else:
            print('Oops, could not determine trade volume, '
                  'check if your instrument is tradable and conversion pair exists. \n'
                  '(e.g. USD_CNH is not possible, since conversion pair EUR_CNH or CNH_EUR does not exist in Oanda)\n'
                  'Please determine trading volume in web interface.')
            units = 0

        return units

    def instrument_list(self):
        inst_list = ['UK100_GBP', 'USD_CAD', 'USB05Y_USD', 'EUR_HKD', 'HK33_HKD', 'FR40_EUR', 'USD_SAR', 'GBP_CAD', 'EUR_PLN',
                     'EUR_DKK', 'SGD_CHF', 'XAU_CHF', 'XPD_USD', 'BCO_USD', 'IN50_USD', 'JP225_USD', 'CN50_USD', 'NATGAS_USD',
                     'USD_PLN', 'GBP_AUD', 'USD_MXN', 'GBP_USD', 'CAD_CHF', 'DE30_EUR', 'XAG_HKD', 'WHEAT_USD', 'XAG_SGD',
                     'XAG_CAD', 'GBP_JPY', 'USD_TRY', 'AU200_AUD', 'EU50_EUR', 'GBP_CHF', 'USD_THB', 'NZD_JPY', 'EUR_GBP',
                     'EUR_JPY', 'USD_ZAR', 'CHF_HKD', 'NZD_CHF', 'CAD_HKD', 'XAU_HKD', 'NAS100_USD', 'EUR_USD', 'GBP_PLN',
                     'AUD_USD', 'EUR_HUF', 'XAG_EUR', 'NZD_USD', 'CHF_ZAR', 'GBP_NZD', 'USD_NOK', 'USD_CZK', 'CAD_SGD',
                     'US2000_USD', 'AUD_CAD', 'ZAR_JPY', 'USD_DKK', 'GBP_HKD', 'XAG_USD', 'USD_HUF', 'USB10Y_USD', 'XAG_JPY',
                     'XAG_GBP', 'CAD_JPY', 'USD_SGD', 'EUR_SEK', 'SUGAR_USD', 'SPX500_USD', 'USD_HKD', 'EUR_AUD', 'XAU_XAG',
                     'AUD_NZD', 'HKD_JPY', 'CHF_JPY', 'XCU_USD', 'USB02Y_USD', 'XAG_NZD', 'XAU_CAD', 'NZD_HKD', 'AUD_JPY',
                     'USD_CNH', 'EUR_ZAR', 'GBP_ZAR', 'EUR_CAD', 'XAU_USD', 'WTICO_USD', 'CORN_USD', 'TWIX_USD', 'EUR_CZK',
                     'AUD_SGD', 'USD_CHF', 'TRY_JPY', 'XAU_SGD', 'EUR_SGD', 'XAU_EUR', 'NL25_EUR', 'XPT_USD', 'EUR_NZD', 'XAG_CHF',
                     'NZD_SGD', 'AUD_HKD', 'SG30_SGD', 'EUR_TRY', 'USD_JPY', 'EUR_NOK', 'XAU_JPY', 'XAU_GBP', 'NZD_CAD', 'XAU_NZD',
                     'USB30Y_USD', 'EUR_CHF', 'SGD_HKD', 'SGD_JPY', 'XAG_AUD', 'SOYBN_USD', 'US30_USD', 'GBP_SGD', 'USD_SEK',
                     'DE10YB_EUR', 'UK10YB_GBP', 'USD_INR', 'AUD_CHF', 'XAU_AUD'
                     ]

        return inst_list

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        tm = self.datas[0].datetime.time(0)
        print('%s, %s' % (dt.isoformat()+' '+tm.isoformat(), txt))
        # print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.indicator = bt.indicators.HullMovingAverage(self.datas[0], period=self.params.maperiod)
        # self.indicatorSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        hma_data = n.array((self.indicator.lines.hma[-6],
                            self.indicator.lines.hma[-5],
                            self.indicator.lines.hma[-4],
                            self.indicator.lines.hma[-3],
                            self.indicator.lines.hma[-2],
                            self.indicator.lines.hma[-1],
                            self.indicator.lines.hma[0]))

        hma_diff = n.diff(hma_data)

        # Open Long Position on local minimum HMA
        # (if slope on last day of HMA is pos and 5 days before neg)
        if not self.position \
            and hma_diff[5] > self.params.min_hma_slope \
            and hma_diff[4] < 0 \
            and hma_diff[3] < 0 \
            and hma_diff[2] < 0 \
            and hma_diff[1] < 0 \
            and hma_diff[0] < 0:
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # determine Entry price, SL & TP
            EntryLong = self.datas[0]
            SL_long = self.indicator.lines.hma[0]

            sl_dist = (EntryLong - SL_long) * (self.params.SL_multiplier - 1)
            SL_long -= sl_dist

            TP_long = (1/self.params.RRR)*(EntryLong-SL_long)+EntryLong
            #Stake Size
            stake_size_long = self.get_trade_volume(SL_long,
                                                    EntryLong,
                                                    self.broker.getvalue(),
                                                    str(self.getdatanames()[0]),
                                                    EntryLong)
            dt = self.datas[0].datetime.date(0)
            tm = self.datas[0].datetime.time(0)
            print(str('%s' % (dt.isoformat()))+str(' ')+str(tm))
            print(hma_diff)
            print('EntryLong = '+str(EntryLong.tick_close))
            print('SL_long = '+str(SL_long))
            print('TP_long = '+str(TP_long))
            print('size = ' + str(stake_size_long))
            # place order
            self.order = self.buy_bracket(limitprice=TP_long,
                                          limitexec=bt.Order.Limit,
                                          price=EntryLong,
                                          exectype=bt.Order.Market,
                                          stopprice=SL_long,
                                          stopexec=bt.Order.Stop,
                                          size=stake_size_long)


        # Open Short Position on local maximum HMA
        # (if slope on last day of HMA is neg and 5 days before pos)
        if not self.position \
            and hma_diff[5] < -self.params.min_hma_slope \
            and hma_diff[4] > 0 \
            and hma_diff[3] > 0 \
            and hma_diff[2] > 0 \
            and hma_diff[1] > 0 \
            and hma_diff[0] > 0:
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            # determine Entry price, SL & TP
            EntryShort = self.datas[0]
            SL_short = self.indicator.lines.hma[0]

            sl_dist = (SL_short - EntryShort) * (self.params.SL_multiplier - 1)
            SL_short += sl_dist

            TP_short = (-1/self.params.RRR)*(SL_short - EntryShort) + EntryShort
            #Stake Size
            # stake_size = 2E-4*self.params.stakepercent*self.broker.getvalue()/(SL_short-EntryShort)
            stake_size_short = self.get_trade_volume(SL_short,
                                                     EntryShort,
                                                     self.broker.getvalue(),
                                                     str(self.getdatanames()[0]),
                                                     EntryShort)
            # print(SL_short-EntryShort)
            # print(self.broker.getvalue())
            # print(stake_size)
            dt = self.datas[0].datetime.date(0)
            tm = self.datas[0].datetime.time(0)
            print(str('%s' % (dt.isoformat())) + str(' ') + str(tm))
            print(hma_diff)
            print('EntryShort = '+str(EntryShort.tick_close))
            print('SL_Short = '+str(SL_short))
            print('TP_Short = '+str(TP_short))
            print('size = ' + str(stake_size_short))
            # place order
            self.order = self.sell_bracket(price=EntryShort,
                                           exectype=bt.Order.Market,
                                           stopprice=SL_short,
                                           stopexec=bt.Order.Stop,
                                           limitprice=TP_short,
                                           limitexec=bt.Order.Limit,
                                           size=stake_size_short)







