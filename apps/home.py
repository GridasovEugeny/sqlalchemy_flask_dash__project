import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app
from database import ORMLayer
from database import DBModel
import pandas as pd
import numpy as np

df = ORMLayer.select_homepage_analytic()
sLength = len(df['contract_num'])
df['readyness'] = pd.Series(np.random.randint(0, 100, sLength), index=df.index)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)


fig = px.scatter(df, x="contract_date", y="readyness",
                 size="count", color="manufacturer", hover_name="contract_num",
                  size_max=60)
help(px.scatter())
layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])
