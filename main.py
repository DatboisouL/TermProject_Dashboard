import dash
from dash import html, dash_table, dcc
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

df = pd.read_csv('data/PM25.csv')

pollutants = ['PM25', 'PM10', 'O3', 'NO2', 'SO2', 'CO']
columns = [{'label': col, 'value': col} for col in df.columns if col in pollutants]
columns.append({'label': 'All Pollutants', 'value': 'all'})

app.layout = html.Div([
    html.Div(children='First Deployed Dash App'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Dropdown(
        id='dropdown',
        options=columns,
        value='PM25'  # Default value
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
