import streamlit as st
from whosampled.config import ACCESS_TOKEN
import requests

from whosampled.api.get_song_info import get_artist_name, get_sampled_songs

def search_song(song_title, artist_name=None):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": song_title}
    response = requests.get(f"{base_url}/search", headers=headers, params=params)
    data = response.json()
    hits = data["response"]["hits"]
    for hit in hits:
        result = hit["result"]
        # Optionally filter by artist name
        if artist_name:
            if artist_name.lower() in result["primary_artist"]["name"].lower():
                print(f"Found: {result['full_title']} (ID: {result['id']})")
                get_artist_name(result['id'])
                return result["id"]
        else:
            print(f"Found: {result['full_title']} (ID: {result['id']})")
            return result["id"]
    print("No matching song found.")
    return None

def get_search_results(query):
    """Get search results from Genius API"""
    if not query: # Added check for empty query
        return [] # Return empty list if query is empty
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": query}
    try: # Added error handling for the API call
        response = requests.get(f"{base_url}/search", headers=headers, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        hits = data["response"]["hits"]

        # Create a list of tuples with (display_text, song_id)
        results = []
        for hit in hits:
            result = hit["result"]
            display_text = f"{result['full_title']} by {result['primary_artist']['name']}"
            results.append((display_text, result['id']))
        return results
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching search results: {e}")
        return []
    except KeyError: # Handle potential KeyError if API response structure is unexpected
        st.error("Unexpected API response format.")
        return []