import dash
from dash import html,dash_table
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

df = pd.read_csv('data/PM25.csv')

app.layout = html.Div([
    html.Div(children='First Deployed Dash App'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

if __name__ == "__main__":
    app.run(debug=True)