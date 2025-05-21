from config import ACCESS_TOKEN
import requests



def get_artist_name(song_id):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{base_url}/songs/{song_id}", headers=headers)
    data = response.json()
    # Extract artist name
    artist_name = data["response"]["song"]["artist_names"]
    print("Artist:", artist_name)
    return artist_name

def get_sampled_songs(song_id):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{base_url}/songs/{song_id}", headers=headers)
    data = response.json()
    relationships = data["response"]["song"].get("song_relationships", [])
    sampled_songs = []
    for rel in relationships:
        if rel["type"] == "samples":
            for sampled in rel["songs"]:
                sampled_songs.append({
                    "id": sampled["id"],
                    "title": sampled["title"],
                    "artist": sampled["primary_artist"]["name"]
                })
    if sampled_songs:
        print("This song samples:")
        for song in sampled_songs:
            print(f"- {song['title']} by {song['artist']} (ID: {song['id']})")
    else:
        print("No samples found for this song.")
    return sampled_songs