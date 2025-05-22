from get_song_info import get_artist_name, get_sampled_songs
from search import search_song
from whosampled.utils.graph_utils import build_graph, plot_graph

import plotly.graph_objects as go
import networkx as nx


def main():
    # artist = get_artist_name(SONG_ID)
    # print("Artist:", artist)

    # song_id = search_song("The World Is Yours", artist_name="Nas")
    # print("Song ID:", song_id)

    nodes = ["The World Is Yours", "Sampled Song 1", "Sampled Song 2"]
    edges = [("The World Is Yours", "Sampled Song 1"), ("The World Is Yours", "Sampled Song 2")]

    G = build_graph(nodes, edges)
    plot_graph(G)
    

if __name__ == "__main__":
    main() 