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
               'AU200_AUD',
               'AUD_CHF',
               'AUD_SGD',
               'BCO_USD',
               'CAD_CHF',
               'CAD_SGD',
               'CHF_HKD',
               'CHF_JPY',
               'CHF_ZAR',
               'CN50_USD',
               'CORN_USD',
               'DE30_EUR',
               'EU50_EUR',
               'EUR_AUD',
               'EUR_CAD',
               'EUR_CHF',
               'EUR_CZK',
               'EUR_DKK',
               'EUR_GBP',
               'EUR_HUF',
               'EUR_JPY',
               'EUR_NOK',
               'EUR_PLN',
               'EUR_SEK',
               'EUR_SGD',
               'EUR_ZAR',
               'FR40_EUR',
               'GBP_AUD',
               'GBP_CAD',
               'GBP_CHF',
               'GBP_HKD',
               'GBP_JPY',
               'GBP_NZD',
               'GBP_PLN',
               'GBP_SGD',
               'HK33_HKD',
               'HKD_JPY',
               'IN50_USD',
               'JP225_USD',
               'NAS100_USD',
               'NATGAS_USD',
               'NL25_EUR',
               'NZD_CAD',
               'NZD_CHF',
               'NZD_HKD',
               'NZD_JPY',
               'NZD_SGD',
               'NZD_USD',
               'SG30_SGD',
               'SGD_CHF',
               'SGD_HKD',
               'SGD_JPY',
               'SOYBN_USD',
               'SPX500_USD',
               'SUGAR_USD',
               'TRY_JPY',
               'TWIX_USD',
               'UK100_GBP',
               'USB10Y_USD',
               'USD_CNH',
               'USD_CZK',
               'USD_DKK',
               'USD_HKD',
               'USD_HUF',
               'USD_INR',
               'USD_MXN',
               'USD_NOK',
               'USD_PLN',
               'USD_SAR',
               'USD_SEK',
               'USD_SGD',
               'USD_THB',
               'USD_TRY',
               'USD_ZAR',
               'WHEAT_USD',
               'XAG_USD',
               'XAU_USD',
               'XAU_XAG',
               'XCU_USD',
               'XPD_USD',
               'XPT_USD',
               'ZAR_JPY',
               'UK10YB_GBP',
               'DE10YB_EUR']

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




