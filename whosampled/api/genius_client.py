# genius_client.py
import requests
from whosampled.config import ACCESS_TOKEN

BASE_URL = "https://api.genius.com"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def call_genius_api(endpoint, **kwargs):
    """
    A helper function to call the Genius API.
    endpoint: (str) The API endpoint (e.g., "/songs/{song_id}" or "/artists/{artist_id}/songs/{song_id}").
    **kwargs: Format parameters for the endpoint and query parameters.
    """
    # Separate format parameters from query parameters
    format_params = {}
    query_params = {}
    
    # Check if endpoint has format placeholders
    if '{' in endpoint:
        # Extract format parameters from kwargs
        for key, value in kwargs.items():
            if f"{{{key}}}" in endpoint:
                format_params[key] = value
            else:
                query_params[key] = value
        
        # Format the URL with the parameters
        url = f"{BASE_URL}{endpoint.format(**format_params)}"
    else:
        url = f"{BASE_URL}{endpoint}"
        query_params = kwargs
    
    try:
        response = requests.get(url, headers=HEADERS, params=query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API Error: {str(e)}")