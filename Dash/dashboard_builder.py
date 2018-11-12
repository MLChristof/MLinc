# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from mlinc import oanda_trader
from datetime import datetime

trader = oanda_trader.OandaTrader.from_conf_file('all',
                                                 r'C:\Data\Documents\Christof\Python\Trading\MLinc\mlinc\conf.ini')

trade_data = trader.get_all_trades()
account_balance = trader.account_balance()

trade_data['balance'] = 0

balance = account_balance
for idx in trade_data.index:
    balance -= trade_data.iloc[idx+1]['realizedPL']
    trade_data.at[idx, 'balance'] = balance

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='MLinc Thunder Dashboard'),

    html.Div(children='''
        Making billions and billions and billions.
    '''),

    dcc.Dropdown(
        options=[
            {'label': 'Fritsie op de daily', 'value': 'daily'},
            {'label': 'Fritsie op de hourly', 'value': 'hourly'}
        ],
        value='daily'
    ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': trade_data['closeTime'], 'y': trade_data['realizedPL'], 'type': 'line', 'name': 'PL'},
                {'x': trade_data['closeTime'], 'y': trade_data['balance'], 'type': 'line', 'name': 'Balance','yaxis': 'y2'}
            ],
            'layout': {
                'title': 'Account balance history',
                'yaxis': dict(
                    title='Realized PL',
                    titlefont=dict(
                        color='#1f77b4'
                    ),
                    tickfont=dict(
                        color='#1f77b4'
                    )
                ),
                'yaxis2': dict(
                    title='Balance',
                    titlefont=dict(
                        color='#d62728'
                    ),
                    tickfont=dict(
                        color='#d62728'
                    ),
                    anchor='x',
                    overlaying='y',
                    side='right'
                ),
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)