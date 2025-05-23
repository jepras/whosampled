import streamlit as st
from whosampled.components.search_components import render_search_input, render_song_selector
from whosampled.services.search_service import handle_search, handle_song_selection
from whosampled.state.app_state import initialize_state, get_selected_song_id

# Set up the Streamlit page
st.title("Who Sampled - Song Search")
st.write("Search for a song to find its samples and covers")

# Initialize application state
initialize_state()

# Render search input and get query
search_query = render_search_input()

# Handle search and get results
results = handle_search(search_query)

# If we have results, render the song selector
if results:
    selected_song_display, selected_id = render_song_selector(
        results=results,
        current_song_id=get_selected_song_id()
    )
    handle_song_selection(selected_song_display, selected_id)
else:
    if search_query:  # Only show "no results" if there was a search query
        st.write("No results found. Try a different search term.")

# You can now use st.session_state['selected_song_id'] elsewhere in your app
# For example, to fetch sampled songs or build the graph when a button is clicked.
