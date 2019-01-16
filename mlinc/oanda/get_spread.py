# from mlinc.oanda_examples.exampleauth import exampleAuth
import oandapyV20
from mlinc.oanda.candle_data import candles

# Example script for retrieving spread on given instrument


def get_spread(inst, accountID, access_token):
    api = oandapyV20.API(access_token=access_token)
    test = candles(inst, granularity=['M1'], count=[1], From=None, to=None, price=['BA'], nice=True, access_token=access_token)
    bid = float(test['candles'][0]['bid']['c'])
    ask = float(test['candles'][0]['ask']['c'])
    print(bid)
    print(ask)
    spread = float(format(ask-bid, '.5f'))
    return spread


if __name__ == "__main__":
    test = get_spread(inst=['XAU_CAD'])
    print(test)
