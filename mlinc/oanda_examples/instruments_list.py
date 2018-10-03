# import json
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
from mlinc.oanda_examples.exampleauth import exampleAuth

def instrument_list():
    """
    Function to retrieve all tradable instruments from Oanda.

    Returns List with instrument codes
    -------
    """

    instr_list = []
    accountID, token = exampleAuth()
    client = oandapyV20.API(access_token=token)
    r = accounts.AccountInstruments(accountID=accountID)
    rv = client.request(r)

    # instr_dict = json.dumps(rv, indent=2)

    for i in range(len(rv['instruments'])):
        instr_list.append(rv['instruments'][i]['name'])

    return instr_list

def custom_list():
    custom_inst = ['EUR_USD',
                   'GBP_USD',
                   'USD_CAD',
                   'USD_CHF',
                   'USD_JPY',
                   'AU200_AUD',
                   'AUD_CHF',
                   'AUD_NZD',
                   'AUD_SGD',
                   'AUD_USD',
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
                   'US2000_USD',
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
                   'DE10YB_EUR',
                   ]

    return custom_inst

# print(instrument_list())
# print(custom_list())

