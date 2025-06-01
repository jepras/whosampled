import os
import streamlit as st
from whosampled.api.genius_client import call_genius_api
from openai import OpenAI
from typing import List, Dict, Optional

# Constants for OpenAI
MAX_TOKENS_PER_REQUEST = 150
FALLBACK_MODEL = "gpt-3.5-turbo"  # Cheaper fallback model


def get_artist_name(song_id):
    data = call_genius_api("/songs/{song_id}", song_id=song_id)
    artist_name = data["response"]["song"]["artist_names"]
    print("Artist:", artist_name)
    return artist_name


def get_sampled_songs(song_id):
    data = call_genius_api("/songs/{song_id}", song_id=song_id)
    relationships = data["response"]["song"].get("song_relationships", [])
    sampled_songs = []

    # Get the release year of the main song
    main_song_year = None
    if "release_date" in data["response"]["song"]:
        # Try to extract year from release_date (format: "YYYY-MM-DD")
        try:
            main_song_year = int(data["response"]["song"]["release_date"].split("-")[0])
        except (ValueError, IndexError):
            pass

    for rel in relationships:
        if rel["type"] == "samples":
            for sampled in rel["songs"]:
                # The sampled song data already includes release_date_components
                sampled_year = sampled.get("release_date_components", {}).get("year")
                sampled_songs.append(
                    {
                        "id": sampled["id"],
                        "title": sampled["title"],
                        "artist": sampled["primary_artist"]["name"],
                        "year": sampled_year,
                    }
                )

    # Add the main song to the list with its year
    return {
        "main_song": {
            "id": song_id,
            "title": data["response"]["song"]["title"],
            "artist": data["response"]["song"]["primary_artist"]["name"],
            "year": main_song_year,
        },
        "sampled_songs": sampled_songs,
    }


def generate_sample_description(song_title: str, sampled_songs: List[Dict]) -> str:
    """
    Generate a natural language description of the samples used in a song using OpenAI.
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
