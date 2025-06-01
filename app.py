import streamlit as st
from whosampled.components.search_components import (
    render_search_input,
    render_song_selector,
)
from whosampled.services.search_service import handle_search, handle_song_selection
from whosampled.state.app_state import initialize_state, get_selected_song_id
from whosampled.api.get_song_info import get_sampled_songs, generate_sample_description
from whosampled.utils.graph_utils import build_graph, plot_graph

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
        results=results, current_song_id=get_selected_song_id()
    )
    handle_song_selection(selected_song_display, selected_id)

    # If a song is selected, show its samples
    if selected_id:
        st.subheader("Sample Graph")

        # Add a loading spinner while fetching and processing data
        with st.spinner("Loading sample data and generating graph..."):
            song_data = get_sampled_songs(selected_id)

            if song_data:
                # Generate and display the sample description
                description = generate_sample_description(
                    selected_song_display, song_data["sampled_songs"]
                )
                st.write(description)
                st.write("---")  # Add a separator

                # Create nodes and edges for the graph
                nodes = [song["title"] for song in song_data["sampled_songs"]]
                edges = [
                    (selected_song_display, song["title"])
                    for song in song_data["sampled_songs"]
                ]

                # Build and plot the graph
                G = build_graph(song_data["main_song"], song_data["sampled_songs"])
                fig = plot_graph(G)  # Get the figure object
                st.plotly_chart(fig, use_container_width=True)  # Display in Streamlit
            else:
                st.write("No samples found for this song.")
else:
    if search_query:  # Only show "no results" if there was a search query
        st.write("No results found. Try a different search term.")
