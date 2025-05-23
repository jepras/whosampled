import streamlit as st
from typing import Optional

def initialize_state():
    """Initialize the application state"""
    if 'selected_song_id' not in st.session_state:
        st.session_state['selected_song_id'] = None

def get_selected_song_id() -> Optional[int]:
    """Get the currently selected song ID from state"""
    return st.session_state.get('selected_song_id')

def set_selected_song_id(song_id: Optional[int]):
    """Set the selected song ID in state"""
    st.session_state['selected_song_id'] = song_id

def clear_selected_song():
    """Clear the selected song from state"""
    st.session_state['selected_song_id'] = None 