# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from mlinc import oanda_trader
from mlinc import oanda_examples

trader = oanda_trader.OandaTrader(object)

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
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)