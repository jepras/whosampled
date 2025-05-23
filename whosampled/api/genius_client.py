# genius_client.py
import requests
from whosampled.config import ACCESS_TOKEN

BASE_URL = "https://api.genius.com"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def call_genius_api(endpoint, song_id=None, **kwargs):
    """
    A helper function to call the Genius API.
    endpoint: (str) The API endpoint (e.g., "/songs/{song_id}").
    song_id: (int, optional) The song ID (if endpoint requires it).
    **kwargs: (optional) Extra query parameters.
    """
    if song_id is not None:
        url = f"{BASE_URL}{endpoint.format(song_id=song_id)}"
    else:
        url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=kwargs)
    return response.json()