"""
This is the master file for arbitrage trading
Date: 25-02-2018

"""
import pandas as pd
import logging
from socketclusterclient import Socketcluster


class TradeEngine(object):

    def __init__(self, db_name):
        """
        Parameters
        ----------
        DB_name = str
            DB_name is the instrument of the validated database.
        """
        self.db_name = db_name

    def get_trade_arguments(self, priority_spec):
        """
        Parameters
        ----------
        priority_spec = str
            priority_spec defines how to pick the first order out of the database

        Returns
        -------
        trade_args = pandas dataframe
            trad_args is 1 row of input arguments for a trade
        """
        database = pd.read_csv(self.db_name, names=['ID', 'Date', 'ex_buy', 'coin_buy', 'coin_sell', 'volume', 'ex_sell'
                                                    , 'priority'])
        database['Date'] = pd.to_datetime(database['Date'])
        if priority_spec == 'chance':
            database.sort_values('priority')
        elif priority_spec == 'date':
            database.sort_values('Date')

        trade_args = database.iloc[0]
        return trade_args

    # def place_order(self, arguments):
    #     socket = Socketcluster.socket("wss://sc-02.coinigy.com/socketcluster/")
    #     socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    #     socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    #     socket.setreconnection(False)
    #     socket.connect()
    #     return order_succes


if __name__ == '__main__':
    trade = TradeEngine(r'C:\Data\Documents\Christof\Python\Trading\MLinc\mlinc\Data\DATABASE_format_test.csv')
    arguments = trade.get_trade_arguments('chance')
    # order_succes = trade.place_order(arguments)
