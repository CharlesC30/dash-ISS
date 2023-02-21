import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px

import pandas as pd

from example_table import table_dict
df = pd.DataFrame(table_dict)

app = dash.Dash(__name__)
app.title = "ISS testing"

test_fig = px.scatter(x=[1,2,3], y=[1,2,3])

app.layout = html.Div([
    html.Div(
        dash_table.DataTable(
            id='main-table',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i, "hideable": True, 'selectable': True} for i in df.columns],
            hidden_columns=['scan_uid'],
            sort_action='native',
            column_selectable='multi',

            # css styles
            style_cell={
                'textAlign': 'left',
                'font-family': 'arial',
            }, 
        ),
        style={"display": "inline-block","width": "40%"}
    ),
    # html.Div(
    #         dcc.Graph(figure=test_fig),
    #         style={"display": "inline-block"},
    # ),
    html.Div(
        className='box',
        style={'display': 'inline-block', 'top': '400px', 'position': 'relative'}
    )
])


if __name__ == "__main__":
    app.run_server(debug=True)
