from dash import dcc, html

def create_layout():
    """
    Creates the layout of the Dash application with a modern header font and organized graphs.

    Returns:
    html.Div: A Div containing the layout of the app.
    """
    layout = html.Div(style={'backgroundColor': '#1a1a1a', 'padding': '20px'}, children=[
        # Link to Google Fonts for a modern header font
        html.Link(
            href='https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap',
            rel='stylesheet'
        ),

        # Modern-looking header
        html.H1(
            "Strava Running Dashboard",
            style={
                'color': '#ffffff',
                'textAlign': 'center',
                'fontFamily': 'Roboto, sans-serif',
                'fontWeight': '300',
                'fontSize': '24px',
                'marginBottom': '20px'
            }
        ),

        # Interval component for updating the graphs
        dcc.Interval(
            id='interval-component',
            interval=60*60*1000,  # Update every hour
            n_intervals=0
        ),

        # First row of graphs: Distance and Time
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='distance-line-graph', style={'height': '30vh'}),
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

            html.Div(children=[
                dcc.Graph(id='time-bar-chart', style={'height': '30vh'}),
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ], style={'marginBottom': '30px', 'display': 'flex', 'justifyContent': 'space-between'}),

        # Second row of graphs: Geographical Map
        html.Div(children=[
            dcc.Graph(id='locations-heatmap', style={'height': '50vh'}),
        ], style={'marginBottom': '30px', 'padding': '10px'}),

        # Third row of graphs: Elevation Gain and Heart Rate Zones
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='elevation-bar-chart', style={'height': '30vh'}),
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

            html.Div(children=[
                dcc.Graph(id='heart-rate-pie-chart', style={'height': '30vh'}),
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ], style={'marginBottom': '30px', 'display': 'flex', 'justifyContent': 'space-between'}),
    ])

    return layout
