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
        dcc.Graph(id='buckets-bar-chart'),

    ])
])