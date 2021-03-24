import dash_tabulator
import json
from textwrap import dedent as d
from database import ORMLayer
from app import app
from dash.dependencies import Input, Output, State
'''order_tab_columns = [{'title': column_name, 'field': column_name, "editor": "input"} for column_name in
                     ORMLayer.order_table_columns_names]
for column in order_tab_columns:
    print(column)'''
order_tab_columns = [{'title': 'contract_num', 'field': 'contract_num', 'editor': 'input'},
                     {'title': 'order_num', 'field': 'order_num', 'editor': 'input'},
                     {'title': 'status', 'field': 'status', 'editor': 'input'}]

order_tab_styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'overflowY': 'scroll'
    }
}

order_tab_options = {"selectable": 1}

order_tab_data = []
for order in ORMLayer.get_order_table_df(None):
    order_tab_data.append({
        ORMLayer.contract_table_columns_names[0]: order[0],
        ORMLayer.contract_table_columns_names[1]: order[1],
        ORMLayer.contract_table_columns_names[2]: order[2]
    })

order_tabulator = dash_tabulator.DashTabulator(
            id='orderpos_table_tabulator',
            columns=order_tab_columns,
            data=order_tab_data,
            options=order_tab_options,
)
