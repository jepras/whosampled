import os
import streamlit as st
from whosampled.api.genius_client import call_genius_api
from openai import OpenAI
from typing import List, Dict, Optional
import time
from datetime import datetime, timedelta
import hashlib

# Constants for rate limiting and cost control
MAX_REQUESTS_PER_DAY = 50
MAX_TOKENS_PER_REQUEST = 150
CACHE_DURATION_HOURS = 24
FALLBACK_MODEL = "gpt-3.5-turbo"  # Cheaper fallback model


def get_cache_key(song_title: str, sampled_songs: List[Dict]) -> str:
    """Generate a unique cache key for the song and its samples."""
    # Sort sampled songs to ensure consistent cache keys
    sorted_samples = sorted(sampled_songs, key=lambda x: x["title"])
    content = f"{song_title}:{str(sorted_samples)}"
    return hashlib.md5(content.encode()).hexdigest()


def get_usage_today() -> int:
    """Get the number of API calls made today."""
    today = datetime.now().date().isoformat()
    if "openai_usage" not in st.session_state:
        st.session_state.openai_usage = {}
    return st.session_state.openai_usage.get(today, 0)


def increment_usage():
    """Increment the daily usage counter."""
    today = datetime.now().date().isoformat()
    if "openai_usage" not in st.session_state:
        st.session_state.openai_usage = {}
    st.session_state.openai_usage[today] = (
        st.session_state.openai_usage.get(today, 0) + 1
    )


@st.cache_data(ttl=timedelta(hours=CACHE_DURATION_HOURS))
def get_cached_description(
    _cache_key: str, song_title: str, sampled_songs: List[Dict]
) -> Optional[str]:
    """
    Get a cached description if it exists.
    The _cache_key parameter is used by Streamlit's caching mechanism.
    """
    try:
        client = OpenAI(api_key=st.secrets["openai_api_key"])

        # Prepare the sampled songs information
        samples_info = "\n".join(
            [
                f"- {song['title']} by {song['artist']} (ID: {song['id']})"
                for song in sampled_songs
            ]
        )

        messages = [
            {
                "role": "system",
                "content": "You are a music expert who writes concise, engaging descriptions of how songs sample other music. Focus on the historical context and significance of the samples.",
            },
            {
                "role": "user",
                "content": f"""Write a brief, engaging description of how the song "{song_title}" samples these songs:
                {samples_info}
                
                Keep it under 3 sentences and focus on the most interesting aspects of the sampling.""",
            },
        ]

        # Try GPT-4 first, fall back to GPT-3.5 if there's an error
        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=MAX_TOKENS_PER_REQUEST,
                temperature=0.7,
            )
        except Exception as e:
            st.warning(
                "Falling back to GPT-3.5-turbo due to GPT-4 availability or cost concerns."
            )
            completion = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS_PER_REQUEST,
                temperature=0.7,
            )

        return completion.choices[0].message.content

    except Exception as e:
        error_msg = f"Unable to generate description: {str(e)}"
        st.error(error_msg)
        return None


def get_artist_name(song_id):
    data = call_genius_api("/songs/{song_id}", song_id=song_id)
    artist_name = data["response"]["song"]["artist_names"]
    print("Artist:", artist_name)
    return artist_name


def get_sampled_songs(song_id):
    data = call_genius_api("/songs/{song_id}", song_id=song_id)
    relationships = data["response"]["song"].get("song_relationships", [])
    sampled_songs = []
    for rel in relationships:
        if rel["type"] == "samples":
            for sampled in rel["songs"]:
                sampled_songs.append(
                    {
                        "id": sampled["id"],
                        "title": sampled["title"],
                        "artist": sampled["primary_artist"]["name"],
                    }
                )
    if sampled_songs:
        print("This song samples:")
        for song in sampled_songs:
            print(f"- {song['title']} by {song['artist']} (ID: {song['id']})")
    else:
        print("No samples found for this song.")
    return sampled_songs


def generate_sample_description(song_title: str, sampled_songs: List[Dict]) -> str:
    """
    Generate a natural language description of the samples used in a song using OpenAI.
    Includes rate limiting, caching, and cost controls.
    """
    # Check rate limits
    if get_usage_today() >= MAX_REQUESTS_PER_DAY:
        return "Daily API request limit reached. Please try again tomorrow."

    # Get cache key
    cache_key = get_cache_key(song_title, sampled_songs)

    # Try to get cached description
    description = get_cached_description(cache_key, song_title, sampled_songs)

    if description:
        # Increment usage counter only for cache hits
        increment_usage()
        return description

    return "Unable to generate description. Please try again."
