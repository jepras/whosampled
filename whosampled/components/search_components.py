import streamlit as st
from typing import List, Tuple, Optional

def render_search_input() -> str:
    """Render the search input component and return the search query"""
    return st.text_input("Enter song title:", key="search")

def render_song_selector(
    results: List[Tuple[str, int]],
    current_song_id: Optional[int]
) -> Tuple[str, Optional[int]]:
    """Render the song selector component and return the selected song display and ID"""
    if not results:
        return None, None
        
    options = [r[0] for r in results]
    
    # Find the index of the currently selected song in the new results
    try:
        current_index = options.index(next((r[0] for r in results if r[1] == current_song_id), options[0]))
    except (ValueError, StopIteration):
        current_index = 0

    selected_song_display = st.selectbox(
        "Select a song:",
        options=options,
        index=current_index,
        key="song_select"
    )

    # Find the ID for the currently selected song display text
    selected_id = next((r[1] for r in results if r[0] == selected_song_display), None)
    
    return selected_song_display, selected_id 