import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px 
from dash.dependencies import Input,Output

df = pd.read_csv("all_reviews_sentiments.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = px.line(df['Sentiment_score'][-50:])

app.layout = html.Div([
    html.H1('Best in ATM Dash API', style={'textAlign': 'center', 'color': 'mediumturquoise'}),
    dcc.Graph(id = "interval-graph", figure = fig),
    dcc.Interval(id="interval-component", interval = 0.3 *1000, n_intervals=1)],
    style = {'background' : 'beige'})

@app.callback(Output(component_id='interval-graph', component_property='figure'),
              Input(component_id='interval-component', component_property='n_intervals'))
def update_figure(_):
    fig = px.line(df['Sentiment_score'][-50:], range_y=[-1,1])
    return fig

if __name__ == '__main__':
  app.run_server(debug=True, host='0.0.0.0')