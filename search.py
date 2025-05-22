from config import ACCESS_TOKEN
import requests

from get_song_info import get_artist_name, get_sampled_songs

def search_song(song_title, artist_name=None):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": song_title}
    response = requests.get(f"{base_url}/search", headers=headers, params=params)
    data = response.json()
    hits = data["response"]["hits"]
    for hit in hits:
        result = hit["result"]
        # Optionally filter by artist name
        if artist_name:
            if artist_name.lower() in result["primary_artist"]["name"].lower():
                print(f"Found: {result['full_title']} (ID: {result['id']})")
                get_artist_name(result['id'])
                return result["id"]
        else:
            print(f"Found: {result['full_title']} (ID: {result['id']})")
            return result["id"]
    print("No matching song found.")
    return None
