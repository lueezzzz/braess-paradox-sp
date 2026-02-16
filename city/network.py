import osmnx as ox
import networkx as nx

filter_str = '["highway"~"trunk|primary|secondary|tertiary"]'

# Download with the filter
G = ox.graph_from_place(
    'Iloilo City, Philippines',
    custom_filter=filter_str,
    simplify=True
)

# Plot to verify
ox.plot_graph(G)