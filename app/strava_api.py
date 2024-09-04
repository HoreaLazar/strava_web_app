import requests
import pandas as pd
import os

def fetch_strava_data():
    """
    Fetches Strava activity data using the Strava API and returns it as a list of dictionaries.
    """
    # Fetch environment variables
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

    # Check if environment variables are set
    if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
        raise ValueError("Strava API credentials are not set in environment variables.")

    # Define API endpoints and headers
    token_url = 'https://www.strava.com/oauth/token'
    activities_url = 'https://www.strava.com/api/v3/athlete/activities'

    # Get access token
    token_response = requests.post(token_url, data={
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN
    })

    # Check if token response is successful
    if token_response.status_code != 200:
        raise Exception(f"Failed to get access token: {token_response.json()}")

    access_token = token_response.json().get('access_token')
    
    if not access_token:
        raise Exception("No access token found in response.")

    # Initialize empty list for activities
    all_activities = []
    page = 1
    per_page = 100  # Fetch 100 activities per page
    max_pages = 5   # Limit to 5 pages

    while page <= max_pages:
        response = requests.get(activities_url, headers={'Authorization': f'Bearer {access_token}'}, params={
            'page': page,
            'per_page': per_page
        })

        # Check if activities response is successful
        if response.status_code != 200:
            raise Exception(f"Failed to get activities: {response.json()}")

        data = response.json()
        if not data:
            break

        all_activities.extend(data)
        page += 1

    # Debug: Print the number of activities fetched
    print(f"Fetched {len(all_activities)} activities.")

    return all_activities
