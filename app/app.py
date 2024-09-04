import dash
from layout import create_layout
from callbacks import register_callbacks
from strava_api import fetch_strava_data

# Initialize the Dash app
app = dash.Dash(__name__)

# Fetch data from Strava
strava_data = fetch_strava_data()

# Set the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app, strava_data)

if __name__ == '__main__':
    app.run_server(debug=True)
