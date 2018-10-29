from mlinc.oanda_examples.candle_data import candles
from mlinc.oanda_examples.exampleauth import exampleAuth

accountID, access_token = exampleAuth()


def get_spread_ratio(inst):
    test = candles(inst=[inst], granularity=['M1'], count=[1], From=None, to=None, price=['BA'], nice=True,
                   access_token=access_token)
    bid = float(test['candles'][0]['bid']['c'])
    ask = float(test['candles'][0]['ask']['c'])
    spread = float(format(ask - bid, '.5f'))
    return format(100*(spread/bid), '.3f')


# custom list contains instruments with low(er) risk coupling
custom_inst = ['EUR_USD',
                   'GBP_USD',
                   'USD_CAD',
                   'USD_CHF',
                   'USD_JPY',
                   'AUD_NZD',
                   'AUD_USD',
                   'CAD_CHF',
                   'USD_DKK',
                   'USD_HKD',
                   'AUD_SGD',
                   'BCO_USD',
                   'CAD_SGD',
                   'CHF_JPY',
                   'DE10YB_EUR',
                   'EU50_EUR',
                   'EUR_AUD',
                   'EUR_CAD',
                   'EUR_CHF',
                   'EUR_DKK',
                   'EUR_GBP',
                   'EUR_JPY',
                   'EUR_SEK',
                   'EUR_SGD',
                   'GBP_AUD',
                   'GBP_CHF',
                   'GBP_HKD',
                   'GBP_JPY',
                   'GBP_NZD',
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
                   'USD_NOK',
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

inst_spread_ratio_dict = {}
expensive_motherfuckers = []
tradable_instruments = []

for inst in custom_inst:
    spread_ratio = get_spread_ratio(inst)
    inst_spread_ratio_dict[inst] = spread_ratio
    if float(spread_ratio) > 0.1:
        print('expensive', inst, spread_ratio)
        expensive_motherfuckers.append(inst)
    else:
        print('tradable', inst, spread_ratio)
        tradable_instruments.append(inst)

print('expensive_motherfuckers = ' + str(expensive_motherfuckers))
print('tradable_instruments = ' + str(tradable_instruments))




