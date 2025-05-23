from whosampled.api.get_song_info import get_artist_name, get_sampled_songs
from whosampled.api.search import search_song
from whosampled.utils.graph_utils import build_graph, plot_graph

def main():
    song_id = search_song("The World Is Yours", artist_name="Nas")
    sampled_songs = get_sampled_songs(song_id)

    # Create nodes and edges
    nodes = [song["title"] for song in sampled_songs]  # (or use song["artist"] if you prefer)
    edges = [(sampled_songs[0]["title"], song["title"]) for song in sampled_songs[1:]]

    original_song = "The World Is Yours"  # (or fetch it from your API)
    nodes.insert(0, original_song)
    edges = [(original_song, song["title"]) for song in sampled_songs]

    G = build_graph(nodes, edges)
    plot_graph(G)
    

if __name__ == "__main__":
    main() 