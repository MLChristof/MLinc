# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from mlinc.oanda.trader import OandaTrader
import configparser
import base64


def from_conf_file(instruments, conf):
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

    return input

def update_figure(selected_account):
    conf_input = from_conf_file('all', r'C:\Data\Documents\Christof\Python\Trading\MLinc\mlinc\conf.ini')
    conf_input['accountid'] = selected_account

    trader = OandaTrader('all', **conf_input)

    trade_data = trader.get_all_trades()
    account_balance = trader.account_balance()

    trade_data['balance'] = 0

    trade_data = trade_data.sort_values(by='closeTime', ascending=False)
    # trade_data.reset_index(drop=True)

    balance = account_balance
    trade_data.balance.iloc[0] = balance
    for idx, val in enumerate(trade_data.index):
        if idx+1 in trade_data.index:
            balance -= trade_data.iloc[idx]['realizedPL']
            trade_data.balance.iloc[idx+1] = balance

    print(trade_data[['realizedPL','balance']])

if __name__ == '__main__':
    update_figure('101-004-7108173-004')