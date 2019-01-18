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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'Marloes.PNG'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

account_id = ['101-004-7108173-001',
              '101-004-7108173-002',
              '101-004-7108173-003',
              '101-004-7108173-004',
              '101-004-7108173-005',
              '101-004-7108173-006',
              '101-004-7108173-007',
              '101-004-7108173-008',
              '101-004-7108173-009',]

app.layout = html.Div(children=[
    html.H1(children='MLinc Thunder Dashboard'),

    html.Div(children='''
        Making billions and billions and billions.
    '''),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in account_id],
        value=account_id[0]
    ),

    dcc.Graph(id='ML_dashboard', style={'height': '90vh'}),

    html.H2(children='Mede mogelijk gemaakt door:'),

    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
    ])


@app.callback(
    dash.dependencies.Output('ML_dashboard', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_figure(selected_account):
    # conf_input = from_conf_file('all', r'C:\Data\Documents\Christof\Python\Trading\MLinc\mlinc\conf.ini')
    conf_input = from_conf_file('all', r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\conf.ini')
    conf_input['accountid'] = selected_account

    trader = OandaTrader('all', **conf_input)

    trade_data = trader.get_all_trades()
    account_balance = trader.account_balance()

    trade_data['balance'] = 0

    trade_data = trade_data.sort_values(by='closeTime', ascending=False)
    # trade_data.reset_index(drop=True)

    balance = account_balance
    # for idx in trade_data.index:
    #     balance -= trade_data.iloc[idx]['realizedPL']
    #     trade_data.at[idx, 'balance'] = balance

    trade_data.balance.iloc[0] = balance
    for idx, val in enumerate(trade_data.index):
        if idx+1 in trade_data.index:
            balance -= trade_data.iloc[idx]['realizedPL']
            trade_data.balance.iloc[idx+1] = balance

    return {
        'data': [
            {'x': trade_data['closeTime'],
             'y': trade_data['realizedPL'],
             'mode': 'markers',
             'marker': dict(
                 color=(trade_data['realizedPL']),
                 colorscale='Bluered'
             ),
             'name': 'PL'},

            {'x': trade_data['closeTime'],
             'y': trade_data['balance'],
             'type': 'line',
             'name': 'Balance',
             'yaxis': 'y2'}
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


if __name__ == '__main__':
    app.run_server(debug=False)
