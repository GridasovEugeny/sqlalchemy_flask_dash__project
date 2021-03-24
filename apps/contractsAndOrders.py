import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_tabulator
from textwrap import dedent as d
import json
from app import app
from database import ORMLayer
from database import DBModel

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Setup some columns
# This is the same as if you were using tabulator directly in js
# Notice the column with "editor": "input" - these cells can be edited
# See tabulator editor for options http://tabulator.info/docs/4.8/edit
columns = [{'title': column_name, 'name': column_name} for column_name in ORMLayer.contract_table_columns_names]
data = []
# Setup some data
for contract in ORMLayer.get_contract_table_df():
    data.append({
           ORMLayer.contract_table_columns_names[0]: contract[0],
           ORMLayer.contract_table_columns_names[1]: contract[1].strftime('%Y-%m-%d'),
           ORMLayer.contract_table_columns_names[2]: contract[2],
           ORMLayer.contract_table_columns_names[3]: contract[3]})
print(data)
# Additional options can be setup here
# these are passed directly to tabulator
# In this example we are enabling selection
# Allowing you to select only 1 row
# and grouping by the col (color) column

options = {"selectable": 1}

# Add a dash_tabulator table
# columns=columns,
# data=data,
# Can be setup at initialization or added with a callback as shown below
# thank you @AnnMarieW for that fix


layout = html.Div([
    dash_tabulator.DashTabulator(
        id='tabulator',
        columns=columns,
        data=data,
        options=options,
    ),
    html.Div(id='output'),
    dcc.Interval(
        id='interval-component-iu',
        interval=1 * 10,  # in milliseconds
        n_intervals=0,
        max_intervals=0
    )

])


# dash_tabulator can be populated from a dash callback
'''@app.callback([Output('tabulator', 'columns'),
               Output('tabulator', 'data')],
              [Input('interval-component-iu', 'n_intervals')])
def initialize(val):
    return columns, data'''


# dash_tabulator can register a callback on rowClicked,
#  cellEdited => a cell with a header that has "editor": "input" etc.. will be returned with row, initial value, old value, new value
# dataChanged => full table upon change (use with caution)
# dataFiltering => header filters as typed, before filtering has occurred (you get partial matching)
# dataFiltered => header filters and rows of data returned
# to receive a dict of the row values
'''
@app.callback(Output('output', 'children'),
              [Input('tabulator', 'cellEdited')])
def display_output(row, cell):
    print(row)
    print(cell)
    return 'You have clicked row {} ; cell {}'.format(row, cell)
'''