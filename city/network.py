import osmnx as ox
import json
import networkx as nx

# filter_str = '["highway"~"trunk|primary|secondary|tertiary"]'

# # Download with the filter
# G = ox.graph_from_place(
#     'Iloilo City, Philippines',
#     custom_filter=filter_str,
#     simplify=True
# )

# # Plot to verify
# ox.plot_graph(G)

# Load json data
with open("city_network.json", "r") as f:
    data = json.load(f)

G = nx.DiGraph()

# Add intersections (nodes)
for node in data["nodes"]:
    G.add_node(node["id"], pos=node["pos"], name=node["name"])

# Add roads (edges)
for link in data["links"]:
    # Add forward edge
    G.add_edge(link["source"], link["target"], 
               weight=link["distance"], 
               name=link["name"], 
               lanes=link["lanes"])
    
    # Add reverse edge only if it is NOT one-way
    if not link["one_way"]:
        
        reverse_name = f"{link['name']} (Reverse)"

        G.add_edge(link["target"], link["source"], 
                   weight=link["distance"], 
                   name=reverse_name, 
                   lanes=link["lanes"])

print(f"Network created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")