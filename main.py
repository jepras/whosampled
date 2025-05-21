from get_song_info import get_artist_name, get_sampled_songs
from search import search_song

def main():
    # artist = get_artist_name(SONG_ID)
    # print("Artist:", artist)

    song_id = search_song("The World Is Yours", artist_name="Nas")
    print("Song ID:", song_id)

if __name__ == "__main__":
    main() 