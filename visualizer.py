import osmnx as ox
import networkx as nx
from city.final_network import intersections, roads

G = nx.MultiDiGraph()
G.graph["crs"] = "EPSG:4326"

for node in intersections:
    G.add_node(node["id"], x=node["x"], y=node["y"])


for road in roads:
    G.add_edge(road["A"], road["B"], length=road["distance"])
    if not road["oneway"]:
        G.add_edge(road["B"], road["A"], length=road["distance"])

molo_network = ox.plot_graph(G, show=True, close=False, edge_color="w")

# plt.savefig("molo_network_map.png", dpi=300, bbox_inches="tight")
# print("Plot saved as molo_network_map.png")
