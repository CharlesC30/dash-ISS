import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px

import pandas as pd

app = dash.Dash(__name__)
app.title = "ISS testing"

from example_table import table_dict
df = pd.DataFrame(table_dict)

# create table in plotly and display with dcc.Graph
# fig = go.Figure(data=[go.Table(
#     header=dict(values=list(df.columns)),
#     cells=dict(values=[df[col] for col in df.columns])
# )])

test_fig = px.scatter(x=[1,2,3], y=[1,2,3])

app.layout = html.Div([
    html.H1('Example Table'),

    html.P(id='selected-cell'),
    html.P(id='selected-cols'),
    html.Button("Swap Cols", id='swap-cols'),
    # create table using dash DataTable
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
        style={"display": "inline-block"}
    ),
    html.Div(
        dcc.Graph(figure=test_fig),
        style={"display": "inline-block"}
    )
])


def df_column_switch(_df, column1, column2):
    """ swap positions of two cols in dataframe """
    i = list(_df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    _df = _df[i]
    return _df


@app.callback(
    Output('main-table', 'data'),
    Output('main-table', 'columns'),
    Input('swap-cols', 'n_clicks'),
    Input('main-table', 'selected_columns'),
)
def column_swap(btn, selected_columns):
    global df
    print(dash.ctx.triggered_id)
    # check button press triggered call back
    if 'swap-cols' == dash.ctx.triggered_id:
        if selected_columns and len(selected_columns) == 2:
            df = df_column_switch(df, selected_columns[0], selected_columns[1])
    return df.to_dict('records'), [{"name": i, "id": i, "hideable": True, 'selectable': True} for i in df.columns]


# callback decorator automatically runs function whenever input is changed
@app.callback(
    # keywords are optional (only two arguments for Input/Output)
    Output(component_id='selected-cell', component_property='children'),
    Input('main-table', 'active_cell')
)
def display_selected_cell(active_cell):
    if active_cell:
        cell_data = df.iloc[active_cell['row']][active_cell['column_id']]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    else:
        return "Data:"


@app.callback(
    Output('selected-cols', 'children'),
    Input('main-table', 'selected_columns')
)
def display_selected_cols(selected_columns):
    if selected_columns:
        return f"Selected Columns: {selected_columns}"
    else:
        return "Selected Columns:"


if __name__ == "__main__":
    app.run_server(debug=True)
