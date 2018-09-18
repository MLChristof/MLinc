import oandapyV20.endpoints.forexlabs as labs
from mlinc.oanda_examples.exampleauth import exampleAuth
import oandapyV20
from datetime import datetime


# Example script for retrieving spread on given instrument

def get_spread():
    # see http://developer.oanda.com/rest-live/forex-labs/#spreads
    inst = 'XCU_USD'
    accountID, access_token = exampleAuth()
    api = oandapyV20.API(access_token=access_token)

    params = {
        "instrument": inst,
        "period": 1
    }
    r = labs.Spreads(params=params)
    api.request(r)
    return r.response

print(str(get_spread()['avg'][0][1]/10000))
