import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# example df
df = pd.DataFrame({'numbers': [1, 2, 3], 'letters': ['A', 'B', 'C']})

# App layout
app = dash.Dash(__name__, prevent_initial_callbacks=True, suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'A', 'value': 1},
            {'label': 'B', 'value': 2},
            {'label': 'C', 'value': 3}
        ],
        value=1
    ),
    dash_table.DataTable(id='dd-output-container',
                         data=df.to_dict('records'),
                         columns=[{'id': c, 'name': c} for c in df.columns.values]) #
])
@app.callback(
    dash.dependencies.Output('dd-output-container', 'data'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    print(value)
    dfs = df.loc[df['numbers'] == value]
    return dfs.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)