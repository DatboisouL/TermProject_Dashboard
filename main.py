from dash import Dash,html,dash_table
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('data/air4thai_44t_2024-01-01_2024-03-01.csv')

app.layout = html.Div([
    html.Div(children='First Deployed Dash App'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

if __name__ == "__main__":
    app.run(debug=True)