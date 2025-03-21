import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from mplsoccer import Pitch

# Define paths
SHOT_DATA_PATH = "data/processed_shots.csv"
PASSING_DATA_PATH = "data/processed_passing_data.csv"

# Load shot data
@st.cache_data
def load_shot_data():
    if os.path.exists(SHOT_DATA_PATH):
        return pd.read_csv(SHOT_DATA_PATH)
    return None

# Load passing data
@st.cache_data
def load_passing_data():
    if os.path.exists(PASSING_DATA_PATH):
        return pd.read_csv(PASSING_DATA_PATH)
    return None

# Function to visualize shots
def plot_shot_map(df):
    pitch = Pitch(pitch_type="statsbomb", pitch_color="white", line_color="black")
    fig, ax = pitch.draw(figsize=(8, 5))
    
    if df is not None:
        scatter = ax.scatter(df["x"] * 120, df["y"] * 80, c=df["xG"], cmap="Reds", edgecolors="black", s=80)
        plt.colorbar(scatter, ax=ax, label="Expected Goals (xG)")
    
    st.pyplot(fig)

# Function to visualize passing network
def plot_passing_network(df):
    if df is None or not set(["passer", "receiver", "x", "y"]).issubset(df.columns):
        st.warning("Passing data is missing required columns: 'passer', 'receiver', 'x', 'y'")
        return

    pitch = Pitch(pitch_type="statsbomb", pitch_color="white", line_color="black")
    fig, ax = pitch.draw(figsize=(8, 5))

    G = nx.DiGraph()
    
    for _, row in df.iterrows():
        G.add_edge(row["passer"], row["receiver"], weight=row.get("pass_count", 1))

    pos = {player: (row["x"] * 120, row["y"] * 80) for _, row in df.iterrows()}

    node_sizes = [G.degree(n) * 100 for n in G.nodes()]
    edge_widths = [G[u][v]["weight"] / 2 for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="blue", alpha=0.6, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color="black", alpha=0.7, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_color="black", ax=ax)

    st.pyplot(fig)

# Streamlit Dashboard
st.title("⚽ Football Analytics Dashboard")

st.subheader("Shot Data")
shot_data = load_shot_data()
plot_shot_map(shot_data)

st.subheader("Passing Network")
passing_data = load_passing_data()
plot_passing_network(passing_data)

st.success("Dashboard Loaded Successfully!")
