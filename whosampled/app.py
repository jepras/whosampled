from typing import Dict, List
import streamlit as st
import pandas as pd
from .utils.graph_utils import build_graph, plot_graph
from .api.get_song_info import get_sampled_songs, generate_sample_description
from .components.search_components import render_search_input, render_song_selector
from .services.search_service import handle_search, handle_song_selection
from .state.app_state import initialize_state, get_selected_song_id


def display_song_graph(song_data: Dict):
    """Display a chronological graph of the song and its samples."""
    main_song = song_data["main_song"]
    sampled_songs = song_data["sampled_songs"]

    if not sampled_songs:
        st.info("No samples found for this song.")
        return

    # Build and plot the graph
    G = build_graph(main_song, sampled_songs)
    fig = plot_graph(G)

    # Display the graph
    st.plotly_chart(fig, use_container_width=True)

    # Add a button to generate AI description
    if st.button("Generate AI Description of Samples"):
        with st.spinner("Generating description..."):
            description = generate_sample_description(main_song["title"], sampled_songs)
            if description:
                st.markdown(f"**Sample Description:** {description}")
            else:
                st.error("Could not generate description. Please try again.")

    # Display a table of samples below the graph
    st.subheader("Sample Details")
    samples_df = pd.DataFrame(
        [
            {
                "Song": song["title"],
                "Artist": song["artist"],
                "Year": song["year"] if song["year"] else "Unknown",
            }
            for song in sampled_songs
        ]
    )
    st.dataframe(samples_df, use_container_width=True)


def main():
    st.set_page_config(page_title="WhoSampled Explorer", page_icon="🎵", layout="wide")

    st.title("WhoSampled Explorer")
    st.markdown("""
    Explore song samples and their relationships. Enter a song title to see what songs it samples
    and get AI-generated descriptions of the sampling relationships.
    """)

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
            # Add a loading spinner while fetching and processing data
            with st.spinner("Loading sample data and generating graph..."):
                song_data = get_sampled_songs(selected_id)
                if song_data:
                    display_song_graph(song_data)
                else:
                    st.error("Could not find song details. Please try another song.")
    else:
        if search_query:  # Only show "no results" if there was a search query
            st.write("No results found. Try a different search term.")


if __name__ == "__main__":
    main()
