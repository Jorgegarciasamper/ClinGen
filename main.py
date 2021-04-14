import dash_table
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import base64

url_data = 'https://raw.githubusercontent.com/Jorgegarciasamper/ClinGen/master/CSV/Clingen-Gene-Disease-Summary-2021-04-09.csv'
df = pd.read_csv(url_data,delimiter=',',skiprows=(0,1,2,3,5),header=[0])
df_genes_disease = df[['GENE SYMBOL', 'DISEASE LABEL']]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

image_filename = 'assets/img/head.png' # image head
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

header = html.Div(

            children=[
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),height=50),
                html.H1(
                    children="ClinGen", className="header-title"
                ),
                html.P(
                    children="This application relates "
                             "gene to implicated disease",
                    className="header-description",
                ),
            ],className="header" # Aprovechamos el css header para poner la imagen centrada
)


sidebar = html.Div([
    html.H2("Gens"),
    html.Hr(),
    html.P("Select the gene to visualize the disease", className="lead"),
    dcc.Dropdown( id='demo-dropdown',
                options=[
                    {'label': gen, 'value': gen}
                    for gen in df_genes_disease['GENE SYMBOL'].unique()
                ],
                value='A2ML1',

                ),

    ],
    className="SIDEBAR_STYLE"
)

cdivs = [dash_table.DataTable(id='dd-output-container',
                         data=df_genes_disease.to_dict('records'),
                         columns=[{'id': c, 'name': c} for c in df_genes_disease.columns.values])]


content = html.Div(cdivs, className="CONTENT_STYLE")

app.layout = html.Div([header, sidebar, content])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'data'),
    [dash.dependencies.Input('demo-dropdown', 'value')])

def update_output(value):
    dfs = df_genes_disease.loc[df_genes_disease['GENE SYMBOL'] == value]
    return dfs.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)