import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import contractsAndOrders, bills, shipments, warehouse, analytics, home


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "8rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "8rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.H2("Menu", className="display-6"),
        html.Hr(),
        html.P(
            "Start ure work from here", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Contracts and Orders", href="/apps/contracts", active="exact"),
                dbc.NavLink("Bills", href="/apps/bills", active="exact"),
                dbc.NavLink("Shipments", href="/apps/shipments", active="exact"),
                dbc.NavLink("Warehouse", href="/apps/warehouse", active="exact"),
                dbc.NavLink("Analytics", href="/apps/analytics", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/apps/contracts":
        return contractsAndOrders.layout
    elif pathname == "/apps/bills":
        return bills.layout
    elif pathname == "/apps/shipments":
        return shipments.layout
    elif pathname == "/apps/warehouse":
        return warehouse.layout
    elif pathname == "/apps/analytics":
        return analytics.layout
    elif pathname == "/":
        return home.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=False)
