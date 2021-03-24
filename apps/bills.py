import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app
from database import ORMLayer
from database import DBModel

layout = html.Div()
