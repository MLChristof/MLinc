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

print(instrument_list())

