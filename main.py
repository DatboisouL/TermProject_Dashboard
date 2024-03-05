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
    dcc.Graph(id='air-quality-graph'),
    html.Div([
        dcc.Graph(id='example-scatter-plot')
    ], className="six columns"),
    html.Div([
        dcc.Graph(id='pie-chart')
    ], className="six columns"),
    html.Div([
        dcc.Graph(id='bar-chart')
    ])
], className="row")

@app.callback(
    Output('example-scatter-plot', 'figure'),
    Input('dropdown', 'value')
)
def update_scatter_plot(selected_pollutant):
    if selected_pollutant == 'all':
        fig = go.Figure()
        for pollutant in pollutants:
            fig.add_trace(go.Scatter(
                x=df['DATETIMEDATA'],
                y=df[pollutant],
                mode='markers',
                name=pollutant
            ))
        layout = go.Layout(
            title='Air Quality Scatter Plot',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest',
            template="plotly_dark"
        )
        fig.update_layout(layout)
    else:
        fig = px.scatter(df, x='DATETIMEDATA', y=selected_pollutant,
                         template="plotly_dark", title=selected_pollutant)
    return fig

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
            hovermode='closest',
            template="plotly_dark"
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
            hovermode='closest',
            template="plotly_dark"
        )
        
        return {'data': [trace], 'layout': layout}

@app.callback(
    Output('pie-chart', 'figure'),
    Input('dropdown', 'value')
)
def update_pie_chart(selected_pollutant):
    if selected_pollutant == 'all':
        fig = go.Figure(data=[go.Pie(labels=pollutants, values=[df[pollutant].sum() for pollutant in pollutants], hole=0.7)])
        layout = go.Layout(
            title='Total Concentration by Pollutant',
            template="plotly_dark"
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Pie(labels=[selected_pollutant], values=[df[selected_pollutant].sum()], hole=0.7)])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant}',
            template="plotly_dark"
        )
        fig.update_layout(layout)
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    Input('dropdown', 'value')
)
def update_bar_chart(selected_pollutant):
    if selected_pollutant == 'all':
        fig = go.Figure(data=[go.Bar(x=pollutants, y=[df[pollutant].sum() for pollutant in pollutants])])
        layout = go.Layout(
            title='Total Concentration by Pollutant (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Total Concentration'),
            template="plotly_dark"
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Bar(x=[selected_pollutant], y=[df[selected_pollutant].sum()])])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant} (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Total Concentration'),
            template="plotly_dark"
        )
        fig.update_layout(layout)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True,port=6969)
