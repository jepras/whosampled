from typing import List, Tuple, Optional
from whosampled.api.search import get_search_results
from whosampled.state.app_state import get_selected_song_id, set_selected_song_id, clear_selected_song
import streamlit as st

def handle_search(query: str) -> List[Tuple[str, int]]:
    """Handle the search process and return results"""
    if not query:
        clear_selected_song()
        return []
    
    results = get_search_results(query)
    return results

def handle_song_selection(selected_song_display: str, selected_id: Optional[int]):
    """Handle song selection and update state"""
    set_selected_song_id(selected_id)
    
    # Display the selected song ID if one is selected
    if selected_id:
        st.write(f"Selected song ID: {selected_id}") 