import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv('https://api.statbank.dk/v1/data/mpk100/CSV?valuePresentation=Value&timeOrder=Ascending&LAND=*&Tid=*', sep=';')
df = df[df['INDHOLD'] != '..']
df['rate'] = df['INDHOLD'].str.replace(',', '.').astype(float)
available_countries = df['LAND'].unique()

app = dash.Dash()
app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': k, 'value': k} for k in available_countries],
        value=['Danmark', 'USA'],
        multi=True
    ),

    html.Hr(),
    dcc.Graph(id='display-selected-values'),

])

@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    ts = df[df["LAND"].isin(value)]
    fig = px.line(ts, x="TID", y="rate", color="LAND")
    return fig


if __name__ == '__main__':
    app.run_server()