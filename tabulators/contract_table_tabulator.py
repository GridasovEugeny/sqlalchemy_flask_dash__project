import dash_tabulator
import json
from textwrap import dedent as d
from app import app
from database import ORMLayer
from dash.dependencies import Input, Output, State

'''contract_tab_columns = [{'title': column_name, 'field': column_name, "editor": "input"} for column_name in
                        ORMLayer.contract_table_columns_names]
for column in contract_tab_columns:
    print(column)'''
contract_tabulator_columns = [{'title': 'contract_num', 'field': 'contract_num', 'editor': 'input'},
                              {'title': 'contract_date', 'field': 'contract_date', 'editor': 'input'},
                              {'title': 'status', 'field': 'status', 'editor': 'input'},
                              {'title': 'manufacturer', 'field': 'manufacturer', 'editor': 'input'}]

contract_tab_styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'overflowY': 'scroll'
    }
}

contract_tabulator_options = {"selectable": 1}

contract_tabulator_data = []
for contract in ORMLayer.select_contract_table():
    contract_tabulator_data.append({
        ORMLayer.contract_table_columns_names[0]: contract[0],
        ORMLayer.contract_table_columns_names[1]: contract[1].strftime('%Y-%m-%d'),
        ORMLayer.contract_table_columns_names[2]: contract[2],
        ORMLayer.contract_table_columns_names[3]: contract[3]})

contract_table_tabulator = dash_tabulator.DashTabulator(
    id='contract_table_tabulator',
    columns=contract_tabulator_columns,
    data=contract_tabulator_data,
    options=contract_tabulator_options,
)


'''@app.callback([Output('contract_table_tabulator', 'columns'),
               Output('contract_table_tabulator', 'data')],
              [Input('interval-component-iu', 'n_intervals')])
def contract_tab_initialize(val):
    return contract_tabulator_columns, contract_tabulator_data'''
