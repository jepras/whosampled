import streamlit as st
from search import search_song
import requests
from config import ACCESS_TOKEN

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


# Set up the Streamlit page
st.title("Who Sampled - Song Search")
st.write("Search for a song to find its samples and covers")

# Create a search box
search_query = st.text_input("Enter song title:", key="search")

# Initialize session state for selected song ID if it doesn't exist
if 'selected_song_id' not in st.session_state:
    st.session_state['selected_song_id'] = None

# When the search query changes or on initial load if query is not empty
results = []
if search_query:
    results = get_search_results(search_query)

    if results:
        # Create a list of display options for the selectbox
        options = [r[0] for r in results]
        # Find the index of the currently selected song in the new results, if it exists
        try:
            current_index = options.index(next((r[0] for r in results if r[1] == st.session_state['selected_song_id']), options[0]))
        except (ValueError, StopIteration):
             # If previously selected song is not in new results or no previous selection, default to the first option
             current_index = 0


        selected_song_display = st.selectbox(
            "Select a song:",
            options=options,
            index=current_index, # Set the default index
            key="song_select"
        )

        # Find the ID for the currently selected song display text
        selected_id = next((r[1] for r in results if r[0] == selected_song_display), None)

        # Store the selected ID in session state
        st.session_state['selected_song_id'] = selected_id

        # Display the selected song ID
        if st.session_state['selected_song_id']:
            st.write(f"Selected song ID: {st.session_state['selected_song_id']}")

        # You can add more functionality here...
    else:
        st.write("No results found. Try a different search term.")
else:
    # If search query is empty, clear the selected song ID
    st.session_state['selected_song_id'] = None


# You can now use st.session_state['selected_song_id'] elsewhere in your app
# For example, to fetch sampled songs or build the graph when a button is clicked.
