import streamlit as st
from whosampled.api.genius_client import call_genius_api

def search_song(song_title):
    """Search for a song and return its ID"""
    try:
        data = call_genius_api("/search", q=song_title)
        hits = data["response"]["hits"]
        
        if hits:
            result = hits[0]["result"]
            print(f"Found: {result['full_title']} (ID: {result['id']})")
            return result["id"]
        
        print("No matching song found.")
        return None
    except Exception as e:
        print(f"Error searching for song: {e}")
        return None

def get_search_results(query):
    """Get search results from Genius API for the dropdown menu"""
    if not query:
        return []
    
    try:
        data = call_genius_api("/search", q=query)
        hits = data["response"]["hits"]

        # Create a list of tuples with (display_text, song_id)
        results = []
        for hit in hits:
            result = hit["result"]
            display_text = result['full_title']
            results.append((display_text, result['id']))
        return results
    except Exception as e:
        st.error(f"Error fetching search results: {e}")
        return []