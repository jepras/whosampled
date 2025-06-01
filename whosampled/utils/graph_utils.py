import networkx as nx
import plotly.graph_objects as go
from typing import Dict, List, Tuple
import numpy as np


def calculate_node_positions(
    main_song: Dict, sampled_songs: List[Dict]
) -> Dict[str, Tuple[float, float]]:
    """
    Calculate node positions using a simple hierarchical layout.
    Returns a dictionary mapping song titles to (x, y) coordinates.
    """
    positions = {}

    # Position main song at the top
    positions[main_song["title"]] = (0, 1)

    # Position sampled songs below, spread horizontally
    for i, song in enumerate(sampled_songs):
        x_pos = (i - len(sampled_songs) / 2) / (
            len(sampled_songs) + 1
        )  # Center the nodes
        positions[song["title"]] = (x_pos, 0)

    return positions


def build_graph(main_song: Dict, sampled_songs: List[Dict]) -> nx.DiGraph:
    """
    Build a directed graph with chronological layout.
    """
    G = nx.DiGraph()

    # Add nodes with year information
    G.add_node(main_song["title"], year=main_song["year"], artist=main_song["artist"])

    for song in sampled_songs:
        G.add_node(song["title"], year=song["year"], artist=song["artist"])

    # Add edges from main song to sampled songs
    for song in sampled_songs:
        G.add_edge(main_song["title"], song["title"])

    return G


def plot_graph(G: nx.DiGraph) -> go.Figure:
    """
    Create a Plotly figure with a hierarchical layout.
    """
    # Calculate node positions
    main_song = next(
        (node for node in G.nodes(data=True) if G.in_degree(node[0]) == 0), None
    )
    sampled_songs = [node for node in G.nodes(data=True) if G.in_degree(node[0]) > 0]

    if main_song is None:
        return go.Figure()  # Return empty figure if no main song found

    positions = calculate_node_positions(
        {"title": main_song[0], **main_song[1]},
        [{"title": song[0], **song[1]} for song in sampled_songs],
    )

    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_colors = []

    for node in G.nodes(data=True):
        x, y = positions[node[0]]
        node_x.append(x)
        node_y.append(y)

        # Create hover text with song info
        year_str = f"Year: {node[1]['year']}" if node[1]["year"] else "Year: Unknown"
        node_text.append(f"{node[0]} by {node[1]['artist']}\n{year_str}")

        # Color nodes based on whether they're the main song or a sample
        node_colors.append("red" if G.in_degree(node[0]) == 0 else "blue")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=node_text,
        textposition="top center",
        marker=dict(showscale=False, color=node_colors, size=20, line_width=2),
    )

    # Create the figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Song Sampling Network",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
        ),
    )

    return fig
