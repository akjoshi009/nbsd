# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from plotly import graph_objs as go
N = 100000


app = dash.Dash()
app.config['suppress_callback_exceptions']=True

server = app.server

#US_STATES_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'

#US_AG_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv'

app.layout = html.Div(
    html.H1('Hello Dash'))

if __name__ == '__main__':
    app.run_server(debug=True)
