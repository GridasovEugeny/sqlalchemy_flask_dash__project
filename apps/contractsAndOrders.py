import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_tabulator
import json
from textwrap import dedent as d
from app import app
from database import ORMLayer
from dash.dependencies import Input, Output, State
import dash_ui as dui

# Grid Testing
grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=5)
# Сборка табулятора контрактов
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
    }
}
contract_tabulator_options = {'layout': 'fitDataFill',
                              'height': '150px', 'selectable': 1}
contract_tabulator_data = []
for contract in ORMLayer.select_contract_table():
    contract_tabulator_data.append({
        ORMLayer.contract_table_columns_names[0]: contract[0],
        ORMLayer.contract_table_columns_names[1]: contract[1].strftime('%Y-%m-%d'),
        ORMLayer.contract_table_columns_names[2]: contract[2],
        ORMLayer.contract_table_columns_names[3]: contract[3]})
contract_tabulator = dash_tabulator.DashTabulator(
    id='contract_table_tabulator',
    columns=contract_tabulator_columns,
    data=contract_tabulator_data,
    options=contract_tabulator_options,
)

# Сборка табулятора заказов
'''order_tab_columns = [{'title': column_name, 'field': column_name, "editor": "input"} for column_name in
                     ORMLayer.order_table_columns_names]
for column in order_tab_columns:
    print(column)'''
order_tabulator_columns = [{'title': 'contract_num', 'field': 'contract_num', 'editor': 'input'},
                           {'title': 'order_num', 'field': 'order_num', 'editor': 'input'},
                           {'title': 'status', 'field': 'status', 'editor': 'input'}]
order_tab_styles = {
    'pre': {
    }
}
order_tabulator_options = {'layout': 'fitDataFill',
                           'height': '250px', 'groupBy': 'contract_num', 'selectable': 1}
order_tabulator_data = []
for order in ORMLayer.select_order_table(None):
    order_tabulator_data.append({
        ORMLayer.order_table_columns_names[0]: order[0],
        ORMLayer.order_table_columns_names[1]: order[1],
        ORMLayer.order_table_columns_names[2]: order[2]
    })
order_tabulator = dash_tabulator.DashTabulator(
    id='order_table_tabulator',
    columns=order_tabulator_columns,
    data=order_tabulator_data,
    options=order_tabulator_options,
)
# Сборка табулятора позиций
'''order_tab_columns = [{'title': column_name, 'field': column_name, "editor": "input"} for column_name in
                     ORMLayer.order_table_columns_names]
for column in order_tab_columns:
    print(column)'''
orderpos_tabulator_columns = [{'title': 'contract_num', 'field': 'contract_num', 'editor': 'input'},
                              {'title': 'order_num', 'field': 'order_num', 'editor': 'input'},
                              {'title': 'status', 'field': 'status', 'editor': 'input'}]
orderpos_tabulator_styles = {
    'pre': {
    }
}
orderpos_tabulator_options = {'layout': 'fitDataFill',
                              'height': '250px', 'selectable': 1}
orderpos_tabulator_data = []
for order in ORMLayer.select_order_table(None):
    order_tabulator_data.append({
        ORMLayer.order_table_columns_names[0]: order[0],
        ORMLayer.order_table_columns_names[1]: order[1],
        ORMLayer.order_table_columns_names[2]: order[2]
    })
orderpos_tabulator = dash_tabulator.DashTabulator(
    id='orderpos_table_tabulator',
    columns=orderpos_tabulator_columns,
    data=orderpos_tabulator_data,
    options=orderpos_tabulator_options,
)
# Разметка страницы
layout = html.Div([
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(contract_tabulator)
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dbc.Button('Add Row', id='add_contract_row_button', className='mr-1')], width=2),
                dbc.Col([dbc.Button('Remove Row', id='remove_contract_row_button', className='mr-1')], width=2)
            ],
            no_gutters=True,

        ),
        dbc.Row(
            [
                dbc.Col(order_tabulator)
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dbc.Button('Add Row', id='add_order_row_button', className='mr-1')], width=2),
                dbc.Col([dbc.Button('Remove Row', id='remove_order_row_button', className='mr-1')], width=2)
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col([dbc.Button('Save to DB', id='save_to_db_button', className='mr-1')], width=2)
            ],
            justify='end'
        )
    ])
])
