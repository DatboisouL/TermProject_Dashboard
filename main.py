import dash
from dash import dash_table, dcc, html
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])
app.title = "Air Quality"

df = pd.read_csv('data/PM25.csv')

pollutants = ['PM25', 'O3', 'WS', 'TEMP', 'RH', 'WD']
columns = [{'label': col, 'value': col} for col in df.columns if col in pollutants]
columns.append({'label': 'All Pollutants', 'value': 'all'})

app.layout = dbc.Container(fluid=True, style={'backgroundColor': '#f0f0f0'}, children=[
    dbc.Row([
        dbc.Col(html.H1("AIR QUALITY 🌫️", style={'text-align': 'center'}))
    ]),
    dbc.Row([
        dbc.Col(html.H6("6610110096 - NUTTASIT TINMAS", style={'text-align': 'center'}))
    ]),
    dbc.Row([
        dbc.Col(html.H6("6610110693 - ALONGKORN JONGYINGYOS", style={'text-align': 'center'}))
    ]),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Div("Parameters", style={'margin': 'auto'}),
                        dcc.Dropdown(
                            id='dropdown',
                            options=columns,
                            value='PM25',
                            clearable=False,
                            className="mr-3",
                            style={'margin': 'auto'}
                        ),
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.Div("Date", style={'margin': 'auto'}),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            min_date_allowed=pd.to_datetime('2024-01-01'),
                            max_date_allowed=pd.to_datetime('2024-03-01'),
                            initial_visible_month=pd.to_datetime('2024-01-01'),
                            start_date=pd.to_datetime('2024-01-01'),
                            end_date=pd.to_datetime('2024-03-01'),
                            className="mr-3",
                            style={'margin': 'auto'}
                        ),
                    ])
                )
            ])
        ])
    ]),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_cell={'textAlign': 'center'}, style_as_list_view=True,),
    dbc.Row([
        dbc.Col(dcc.Graph(id='air-quality-graph'), width=6),
        dbc.Col(dcc.Graph(id='example-scatter-plot'), width=6)
    ], style={'margin-bottom': '20px'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart'), width=6),
        dbc.Col(dcc.Graph(id='pie-chart'), width=6)
    ], style={'margin-bottom': '20px'}),
    dbc.Row([
        dbc.Col(html.H1("PM2.5 AND O3 PREDICTION 🔮", style={'text-align': 'center'}))
    ]),
    dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Div("Prediction Date", style={'text-align': 'center'}),
                    dcc.DatePickerRange(
                        id='prediction-date-picker-range',
                        min_date_allowed=pd.to_datetime('2024-03-02'),
                        max_date_allowed=pd.to_datetime('2024-04-01'),
                        initial_visible_month=pd.to_datetime('2024-03-02'),
                        start_date=pd.to_datetime('2024-03-02'),
                        end_date=pd.to_datetime('2024-04-01'),
                        className="mr-3",
                        style={'text-align': 'center'}
                    ),
                ])
            ])
        ])
    ], width=12)
]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='o3-prediction-graph'), width=6),
        dbc.Col(dcc.Graph(id='pm25-prediction-graph'), width=6)
    ], style={'margin-bottom': '20px'})
])

@app.callback(
    Output('example-scatter-plot', 'figure'),
    [Input('dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')]
)
def update_scatter_plot(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        fig = go.Figure()
        for pollutant in pollutants:
            fig.add_trace(go.Scatter(
                x=filtered_df['DATETIMEDATA'],
                y=filtered_df[pollutant],
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
        fig = px.scatter(filtered_df, x='DATETIMEDATA', y=selected_pollutant,
                        template="plotly_dark", title=selected_pollutant)
    return fig

@app.callback(
    Output('air-quality-graph', 'figure'),
    [Input('dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')]
)
def update_graph(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        traces = []
        for pollutant in pollutants:
            trace = go.Scatter(
                x=filtered_df['DATETIMEDATA'],
                y=filtered_df[pollutant],
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
            x=filtered_df['DATETIMEDATA'],
            y=filtered_df[selected_pollutant],
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
    [Input('dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')]
)
def update_pie_chart(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        fig = go.Figure(data=[go.Pie(labels=pollutants, values=[filtered_df[pollutant].sum() for pollutant in pollutants], hole=0.7)])
        layout = go.Layout(
            title='Total Concentration by Pollutant',
            template="plotly_dark"
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Pie(labels=[selected_pollutant], values=[filtered_df[selected_pollutant].sum()], hole=0.7)])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant}',
            template="plotly_dark"
        )
        fig.update_layout(layout)
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')]
)
def update_bar_chart(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        stats = {
            'Pollutant': [],
            'Average': [],
            'Maximum': [],
            'Minimum': []
        }
        for pollutant in pollutants:
            stats['Pollutant'].append(pollutant)
            stats['Average'].append(filtered_df[pollutant].mean())
            stats['Maximum'].append(filtered_df[pollutant].max())
            stats['Minimum'].append(filtered_df[pollutant].min())
        fig = go.Figure(data=[
            go.Bar(name='Average', x=stats['Pollutant'], y=stats['Average']),
            go.Bar(name='Maximum', x=stats['Pollutant'], y=stats['Maximum']),
            go.Bar(name='Minimum', x=stats['Pollutant'], y=stats['Minimum'])
        ])
        
        layout = go.Layout(
            title='Statistics by Pollutant (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Value'),
            barmode='group',
            template="plotly_dark"
        )
        
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[
            go.Bar(name='Average', x=[selected_pollutant], y=[filtered_df[selected_pollutant].mean()]),
            go.Bar(name='Maximum', x=[selected_pollutant], y=[filtered_df[selected_pollutant].max()]),
            go.Bar(name='Minimum', x=[selected_pollutant], y=[filtered_df[selected_pollutant].min()])
        ])
        
        layout = go.Layout(
            title=f'Statistics of {selected_pollutant} (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Value'),
            template="plotly_dark"
        )
        fig.update_layout(layout)
    return fig

@app.callback(
    Output('pm25-prediction-graph', 'figure'),
    [Input('dropdown', 'value'),
    Input('prediction-date-picker-range', 'start_date'),
    Input('prediction-date-picker-range', 'end_date')]
)
def update_pm25_prediction(start_date, end_date):
    prediction_df = pd.read_csv('data/predict_PM25.csv')
    
    filtered_prediction_df = prediction_df[(prediction_df['DATETIMEDATA'] >= start_date) & (prediction_df['DATETIMEDATA'] <= end_date)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=filtered_prediction_df['DATETIMEDATA'], y=filtered_prediction_df['prediction_label'],
                             mode='lines', name='Predicted PM25'))
    
    fig.update_layout(title='Predicted PM25 Concentration', xaxis_title='DATETIMEDATA', yaxis_title='PM25 Concentration',
            template="plotly_dark")
    
    return fig

@app.callback(
    Output('o3-prediction-graph', 'figure'),
    [Input('prediction-date-picker-range', 'start_date'),
    Input('prediction-date-picker-range', 'end_date')]
)
def update_o3_prediction(start_date, end_date):
    prediction_df = pd.read_csv('data/predict_O3.csv')
    
    filtered_prediction_df = prediction_df[(prediction_df['DATETIMEDATA'] >= start_date) & (prediction_df['DATETIMEDATA'] <= end_date)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=filtered_prediction_df['DATETIMEDATA'], y=filtered_prediction_df['prediction_label'],
                             mode='lines', name='Predicted O3'))
    
    fig.update_layout(title='Predicted O3 Concentrations', xaxis_title='DATETIMEDATA', yaxis_title='O3 Concentration',
            template="plotly_dark")
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, port = 6969)
