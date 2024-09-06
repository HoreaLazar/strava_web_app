from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import pandas as pd

def register_callbacks(app, strava_data):
    """
    Registers the callbacks for the Dash application.

    Parameters:
    app (Dash): The Dash application instance.
    strava_data (list): The list of activities fetched from Strava.
    """
    @app.callback(
        [Output('distance-line-graph', 'figure'),
         Output('time-bar-chart', 'figure'),
         Output('locations-heatmap', 'figure'),
         Output('elevation-bar-chart', 'figure'),
         Output('heart-rate-pie-chart', 'figure')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_graphs(n_intervals):
        """
        Updates the graphs with the latest Strava data.

        Parameters:
        n_intervals (int): The number of intervals passed (used to trigger the update).

        Returns:
        list: Updated figures for the line graph, bar chart, map, pace graph, elevation graph, and heart rate pie chart.
        """
        # Get the current year
        current_year = datetime.now().year

        # Convert Strava data into a DataFrame
        df = pd.DataFrame(strava_data)

        # Check for essential columns and handle missing data
        if 'start_date_local' not in df.columns or 'distance' not in df.columns or 'moving_time' not in df.columns:
            return [go.Figure()] * 6

        # Convert 'start_date_local' to datetime format
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])

        # Filter activities for the current year
        df = df[df['start_date_local'].dt.year == current_year]

        # Create a month column for aggregation
        df['month'] = df['start_date_local'].dt.to_period('M')

        # Aggregating data by month
        monthly_distance = df.groupby('month')['distance'].sum()
        monthly_time = df.groupby('month')['moving_time'].sum()
        monthly_elevation_gain = df.groupby('month')['total_elevation_gain'].sum()

        # Convert period index to string for plotting
        months = monthly_distance.index.strftime('%m-%y')
        distances = monthly_distance.values
        times = monthly_time.values
        elevations = monthly_elevation_gain.values

        # Line graph for total distance by month
        distance_fig = go.Figure(data=[
            go.Scatter(x=months, y=distances, mode='lines+markers', marker=dict(color='rgb(0, 204, 150)'))
        ])
        distance_fig.update_layout(
            template='seaborn', 
            title='YTD Total Distance by Month', 
            xaxis_title='Month', 
            yaxis_title='Total Distance (m)', 
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        # Bar chart for total time by month
        time_fig = go.Figure(data=[
            go.Bar(x=months, y=times, marker=dict(color='rgb(255, 99, 71)'))
        ])
        time_fig.update_layout(
            template='seaborn', 
            title='YTD Total Time by Month', 
            xaxis_title='Month', 
            yaxis_title='Total Time (s)', 
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        # Extract latitudes and longitudes with error handling
        run_latitudes = []
        run_longitudes = []
        for _, row in df.iterrows():
            if isinstance(row['start_latlng'], list) and len(row['start_latlng']) == 2:
                latlng = row['start_latlng']
                if pd.notna(latlng[0]) and pd.notna(latlng[1]):
                    run_latitudes.append(latlng[0])
                    run_longitudes.append(latlng[1])

        # Map visualization
        if run_latitudes and run_longitudes:
            map_fig = px.scatter_mapbox(
                lat=run_latitudes,
                lon=run_longitudes,
                center=dict(lat=54.5, lon=-3.5),  # Centered over the UK
                zoom=5,  # Zoom level appropriate for the UK
                mapbox_style="carto-positron",  # Use a simple map style
                title='Running Locations Map (YTD)'
            )
            map_fig.update_layout(
                template='seaborn',
                height=500,
                margin=dict(l=20, r=20, t=50, b=20)
            )
        else:
            # If no valid location data is found, display a placeholder figure
            map_fig = go.Figure()
            map_fig.update_layout(
                template='seaborn',
                title='No Location Data Available',
                height=500,
                margin=dict(l=20, r=20, t=50, b=20)
            )

        # Calculate average pace (time per km)
        df['pace'] = df['moving_time'] / (df['distance'] / 1000)

        # Bar chart for total elevation gain by month
        elevation_fig = go.Figure(data=[
            go.Bar(x=months, y=elevations, marker=dict(color='rgb(255, 99, 71)'))
        ])
        elevation_fig.update_layout(
            template='seaborn', 
            title='YTD Total Elevation Gain by Month', 
            xaxis_title='Month', 
            yaxis_title='Elevation Gain (m)', 
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        # Pie chart for heart rate zones
        if 'average_heartrate' in df.columns:
            hr_zones = {
                'Zone 1': len(df[df['average_heartrate'] < 130]),
                'Zone 2': len(df[(df['average_heartrate'] >= 130) & (df['average_heartrate'] < 150)]),
                'Zone 3': len(df[(df['average_heartrate'] >= 150) & (df['average_heartrate'] < 165)]),
                'Zone 4': len(df[(df['average_heartrate'] >= 165) & (df['average_heartrate'] < 180)]),
                'Zone 5': len(df[df['average_heartrate'] >= 180])
            }
            hr_fig = px.pie(
                names=list(hr_zones.keys()),
                values=list(hr_zones.values()),
                title='Heart Rate Zones Distribution'
            )
            hr_fig.update_layout(
                template='seaborn',
                height=300,
                margin=dict(l=20, r=20, t=50, b=20)
            )
        else:
            hr_fig = go.Figure()
            hr_fig.update_layout(
                template='seaborn',
                title='No Heart Rate Data Available',
                height=300,
                margin=dict(l=20, r=20, t=50, b=20)
            )

        return distance_fig, time_fig, map_fig, elevation_fig, hr_fig
