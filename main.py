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
        value='PM25'
    ),
    dcc.Graph(id='air-quality-graph')
])

@app.callback(
    Output('air-quality-graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_pollutant):
    if selected_pollutant == 'all':
        traces = []
        for pollutant in pollutants:
            trace = go.Scatter(
                x=df['DATETIMEDATA'],
                y=df[pollutant],
                mode='lines',
                name=pollutant
            )
            traces.append(trace)
        
        layout = go.Layout(
            title='Air Quality',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest'
        )
        
        return {'data': traces, 'layout': layout}
    else:
        trace = go.Scatter(
            x=df['DATETIMEDATA'],
            y=df[selected_pollutant],
            mode='lines',
            name=selected_pollutant
        )
        
        layout = go.Layout(
            title='Air Quality',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest'
        )
        
        return {'data': [trace], 'layout': layout}


if __name__ == "__main__":
    app.run_server(debug=True)
