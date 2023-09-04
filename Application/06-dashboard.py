import os
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

# Define the base directory based on where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

if 'DOCKER_ENV' in os.environ:
    # Running in Docker container
    csv_dir = '/app/output'
else:
    # Running locally
    csv_dir = os.path.join(base_dir, 'output')

# CSV data into DataFrames
df_words = pd.read_csv(os.path.join(csv_dir, 'word_analysis.csv'))
df_reviews = pd.read_csv(os.path.join(csv_dir, 'reviews_sentiments.csv'))


# get company names for dropdown options
company_options = [{'label': company, 'value': company} for company in df_words['CompanyName'].unique()]
company_options.append({'label': 'All', 'value': 'All'})  # Add "All" option

# get the list of word buckets
bucket_columns = df_words.columns[4:]  # Columns containing word bucket counts

# Initialize the Dash app
app = dash.Dash(__name__)

# layout of the app
app.layout = html.Div([
    # Total number of reviews frame
    html.Div([
        html.Div(id='total-reviews-frame', style={'font-size': '24px', 'margin-bottom': '20px'}),
    ]),
    
    # Dropdown and graphs
    html.Div([
        dcc.Dropdown(id='company-dropdown', options=company_options, value=['All'], multi=True),
        
        # Position graphs side by side using CSS styling
        html.Div([
            dcc.Graph(id='review-sentiment-bar-chart', style={'display': 'inline-block', 'width': '49%'}),
            dcc.Graph(id='review-count-distribution', style={'display': 'inline-block', 'width': '49%'}),
        ], style={'width': '100%', 'display': 'inline-block'}),

        
        html.Div([
            dcc.Graph(id='buckets-bar-chart', style={'display': 'inline-block', 'width': '49%'}),
            dcc.Graph(id='buckets-bar-chart-distr', style={'display': 'inline-block', 'width': '49%'}),
        ], style={'width': '100%', 'display': 'inline-block'}),

    ])
])

# color mappings for sentiment labels
color_discrete_map = {
    'Negative': 'red',
    'Neutral': 'blue',
    'Positive': 'green'
}



# REVIEW SENTIMENT BAR CHART
@app.callback(
    Output('review-sentiment-bar-chart', 'figure'),
    [Input('company-dropdown', 'value')]
)
def update_review_sentiment_bar_chart(selected_companies):
    if 'All' in selected_companies:
        filtered_df = df_reviews
    else:
        filtered_df = df_reviews[df_reviews['CompanyName'].isin(selected_companies)]
    
    sentiment_counts = (
        filtered_df.groupby(['CompanyName', 'SentimentLabel'])['ReviewID']
        .count()
    ).reset_index()
    
    fig = px.bar(
        sentiment_counts,
        x='CompanyName',  # Company names on x-axis
        y='ReviewID',      # Count of reviews on y-axis
        color='SentimentLabel',
        title='Companies per Sentiment Label',
        labels={'x': 'Company Name', 'y': 'Sum of Reviews'},
        color_discrete_map=color_discrete_map,
        barmode='group',   # Grouped bars
        orientation='v'    # Vertical bars
    )
    
    fig.update_layout(yaxis_title="Sum of Reviews")  # Update y-axis title
    
    return fig


# REVIEW COUNT DISTRIBUTION
@app.callback(
    Output('review-count-distribution', 'figure'),
    [Input('company-dropdown', 'value')]
)
def update_review_sentiment_bar_chart(selected_companies):
    if 'All' in selected_companies:
        filtered_df = df_reviews
    else:
        filtered_df = df_reviews[df_reviews['CompanyName'].isin(selected_companies)]
    
    sentiment_percentage = (
        filtered_df.groupby(['CompanyName', 'SentimentLabel'])['ReviewID']
        .count() / len(filtered_df) * 100
    ).reset_index()
    
    sentiment_percentage['ReviewPercentage'] = (
        sentiment_percentage.groupby('CompanyName')['ReviewID'].apply(lambda x: x / x.sum() * 100)
    )
    
    sorted_sentiment_percentage = (
        sentiment_percentage.sort_values(by='ReviewID', ascending=False)
    )
    
    fig = px.bar(
        sorted_sentiment_percentage,
        x='ReviewPercentage',  # Percentage of reviews
        y='CompanyName',
        color='SentimentLabel',
        title='Companies per Sentiment Label Distribution',
        labels={'x': 'Percentage of Reviews', 'y': 'Company Name'},
        color_discrete_map=color_discrete_map,
        barmode='stack',  # Stack bars
        orientation='h'  # Horizontal bars
    )
    
    fig.update_layout(xaxis_title="Percentage of Reviews (%)")  # Update x-axis title
    
    return fig

# BUCKETS BAR CHART
@app.callback(
    Output('buckets-bar-chart', 'figure'),
    [Input('company-dropdown', 'value')]
)
def update_sentiment_bar_chart(selected_companies):
    if 'All' in selected_companies:
        filtered_df = df_words
    else:
        filtered_df = df_words[df_words['CompanyName'].isin(selected_companies)]
    
    sentiment_scores = filtered_df.groupby('SentimentLabel')[bucket_columns].sum().T
    
    sorted_sentiment_scores = (
        sentiment_scores.sort_values(by=['Negative', 'Neutral', 'Positive'], ascending=False)
    )
    
    fig = px.bar(
        sorted_sentiment_scores,
        x=sorted_sentiment_scores.index,
        y=sorted_sentiment_scores.columns,
        title='Reviews by Word Buckets',
        labels={'x': 'Word Buckets', 'y': 'Word Count'},
        category_orders={"x": bucket_columns},  
        color_discrete_map=color_discrete_map,  
        barmode='group', 
    )
    
    fig.update_layout(xaxis_title="Word Buckets", yaxis_title="Word Count")  
    
    return fig

# BUCKETS BAR CHART DISTRIBUTION
@app.callback(
    Output('buckets-bar-chart-distr', 'figure'),
    [Input('company-dropdown', 'value')]
)
def update_buckets_bar_chart_distribution(selected_companies):
    if 'All' in selected_companies:
        filtered_df = df_words
    else:
        filtered_df = df_words[df_words['CompanyName'].isin(selected_companies)]
    
    sentiment_scores = filtered_df.groupby('SentimentLabel')[bucket_columns].sum().T
    
    sentiment_percentage = sentiment_scores.divide(sentiment_scores.sum(axis=1), axis=0) * 100
    
    fig = px.bar(
        sentiment_percentage,
        x=sentiment_percentage.columns,   
        y=sentiment_percentage.index,      
        title='Reviews by Word Buckets Distribution',
        labels={'x': 'Percentage of Reviews', 'y': 'Sentiment Label'},
        color_discrete_map=color_discrete_map,
        barmode='stack',                  
        orientation='h'                  
    )
    
    fig.update_layout(xaxis_title="Percentage of Reviews (%)", yaxis_title="Word Buckets")
    
    return fig


# TOTAL NUMBER OF REVIEWS
@app.callback(
    Output('total-reviews-frame', 'children'),
    [Input('company-dropdown', 'value')]
)
def update_total_reviews_frame(selected_companies):
    if 'All' in selected_companies:
        total_reviews = len(df_reviews)
    else:
        filtered_df = df_reviews[df_reviews['CompanyName'].isin(selected_companies)]
        total_reviews = len(filtered_df)
    
    return f"Total Reviews: {total_reviews}"



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)

print(dash. __version__)