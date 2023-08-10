import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px 
from dash.dependencies import Input,Output

df = pd.read_csv("all_reviews_sentiments.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dropdown_name = set(df['Company_name'])

app.layout = html.Div([
    html.H1('Best in ATM Dash API', style={'textAlign': 'center', 'color': 'mediumturquoise'}),
    html.Div(dcc.Dropdown(id = 'Dropdown',
                          options=[{'label': k, 'value': k} for k in dropdown_name],
                          value=['Evergreen Credit Union'],
                          searchable=True,
                          multi=True)),
    dcc.Graph(id = "atm-graph")], 
    style = {'background' : 'beige'})

@app.callback(Output(component_id='atm-graph', component_property='figure'),
              Input(component_id='Dropdown', component_property='value'))
def update_figure(_):
    fig = px.line(df['Sentiment_score'][-50:], range_y=[-1,1])
    return fig

if __name__ == '__main__':
  app.run_server(debug=True, host='0.0.0.0')