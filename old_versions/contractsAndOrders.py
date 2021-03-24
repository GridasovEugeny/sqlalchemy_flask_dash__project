import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app
from database import ORMLayer
from database import DBModel

contract_columns = [{'name': "contract_num", "id": "contract_num"},
                    {'name': "contract_date", "id": "contract_date", "type": "date"},
                    {'name': 'status', 'id': 'status'},
                    {'name': "manufacturer", "id": "manufacturer"}]
contract_df_empty_row = {'contract_num': '', 'contract_date': '', 'status': '',  'manufacturer': ''}

order_columns = [{'name': "contract_num", "id": "contract_num"},
                 {"name": "order_num", "id": "order_num", 'width': '100'},
                 {'name': 'status', 'id': 'status'}]
order_df_empty_row = {'contract_num': '',  'order_num': '', 'status': ''}

order_positions_columns = [{'name': "contract_num", "id": "contract_num"},
                           {"name": "order_num", "id": "order_num", 'width': '100'},
                           {"name": "device_type", "id": "device_type_id", 'width': '100'},
                           {"name": "count", "id": "count", 'width': '50'}]
order_positions_df_empty_row = {'contract_num': '',  'order_num': '', 'id': '', 'device_type': '', 'count': ''}

# contract_base_data = ORMLayer.get_contract_table_df().append(contract_df_empty_row, ignore_index=True)
# order_base_data = ORMLayer.get_order_table_df(None).append(order_df_empty_row, ignore_index=True)
# order_positions_base_data = ORMLayer.get_orderpos_table_df(None).append(order_positions_df_empty_row, ignore_index=True)

contract_datatable = dash_table.DataTable(
    id='contracts_datatable',
    columns=contract_columns,
#   data=contract_base_data.to_dict('records'),
    editable=True,
    row_deletable=True,
    row_selectable='single',
    fixed_rows={'headers': True, 'data': 0},
    style_cell={'whiteSpace': 'normal'},
    virtualization=True,
    page_action='none',
    style_table={'height': 300},
)
'''
style_data={
    'width': '150px',
    'maxWidth': '150px',
    'minWidth': '150px',
},
'''
order_datatable = dash_table.DataTable(
    id='orders_datatable',
    columns=order_columns,
#    data=order_base_data.to_dict('records'),
    editable=True,
    row_deletable=True,
    row_selectable='single',
    style_table={'height': 300},
    style_data={
        'width': '150px',
        'maxWidth': '150px',
        'minWidth': '150px',
    }
)

order_position_datatable = dash_table.DataTable(
    id='order_positions_datatable',
    columns=order_positions_columns,
#    data=order_positions_base_data.to_dict('records'),
    editable=True,
    row_deletable=True,
    style_data={
        'width': '150px',
        'maxWidth': '150px',
        'minWidth': '150px',
    }
)

layout = html.Div([
    dbc.Col([  # Левая сторона интерфейса с таблицами
        dbc.Row([
            dbc.Col([contract_datatable]),
            dbc.Col([
                dbc.Row([order_datatable]),
                dbc.Row([order_position_datatable]),
            ])
        ]),

        dbc.Row([
            html.Button('Save to PostgreSQL', id='save_to_postgres', n_clicks=0),
        ], align="end", justify="end")
    ], width=7),
    dbc.Col([  # Правая сторона интерфейса с графиком

    ], width=5)
])


def update_contract_datatable():
    return ORMLayer.get_contract_table_df().to_dict('records')


def update_order_datatable():
    return ORMLayer.get_contract_table_df().to_dict('records')
