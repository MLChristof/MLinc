import oandapyV20.endpoints.forexlabs as labs
from mlinc.oanda_examples.exampleauth import exampleAuth
import oandapyV20
from datetime import datetime


# Example script for retrieving spread on given instrument
# TODO: easier to get ask and bid price and subtract. No if else statements needed
def get_spread():
    # see http://developer.oanda.com/rest-live/forex-labs/#spreads
    inst = 'DE30_EUR'
    accountID, access_token = exampleAuth()
    api = oandapyV20.API(access_token=access_token)

    params = {
        "instrument": inst,
        "period": 1
             }
    r = labs.Spreads(params=params)
    api.request(r)
    if 'JPY' in inst:
        spread = format(r.response['avg'][0][1] / 1, '.3f')
    elif 'BCO' in inst:
        spread = format(r.response['avg'][0][1] / 100, '.3f')
    elif 'DE30' in inst:
        spread = format(r.response['avg'][0][1] / 1, '.1f')
    else:
        spread = format(r.response['avg'][0][1] / 10000, '.5f')
    return spread

print(get_spread())
