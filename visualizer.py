import osmnx as ox
import networkx as nx

G = nx.MultiDiGraph()
G.graph["crs"] = "EPSG:4326"

intersections = [
    {"id": "Molo - 3", "y": 10.697347, "x": 122.543396},
    {"id": "Molo - 4", "y": 10.695993, "x": 122.544452},
    {"id": "Molo - 5", "y": 10.694449, "x": 122.545638},
    {"id": "Molo - 6", "y": 10.692042, "x": 122.549359},
    {"id": "Molo - 7", "y": 10.699246, "x": 122.549446},
    {"id": "Molo - 8", "y": 10.699231, "x": 122.549295},
    {"id": "Molo - 9", "y": 10.698880, "x": 122.549361},
    {"id": "Molo - 10", "y": 10.698959, "x": 122.549522},
    {"id": "villa - 3", "y": 10.688897, "x": 122.516400},
    {"id": "Proper - 1", "y": 10.699766, "x": 122.554176},
]

for node in intersections:
    G.add_node(node["id"], x=node["x"], y=node["y"])

roads = [
    {"A": "Molo - 3", "B": "villa - 3", "distance": 2100, "oneway": False},
    {"A": "Molo - 3", "B": "Molo - 4", "distance": 190, "oneway": False},
    {"A": "Molo - 4", "B": "Molo - 5", "distance": 220, "oneway": False},
    {"A": "Molo - 4", "B": "Molo - 9", "distance": 550, "oneway": False},
    {"A": "Molo - 5", "B": "Molo - 6", "distance": 500, "oneway": False},
    {"A": "Molo - 8", "B": "Molo - 3", "distance": 700, "oneway": True},
    {"A": "Proper - 1", "B": "Molo - 7", "distance": 550, "oneway": True},
    {"A": "Molo - 7", "B": "Molo - 8", "distance": 16, "oneway": False},
    {"A": "Molo - 8", "B": "Molo - 3", "distance": 700, "oneway": True},
    {"A": "Molo - 8", "B": "Molo - 9", "distance": 42, "oneway": True},
    {"A": "Molo - 10", "B": "Proper - 1", "distance": 500, "oneway": True},
    {"A": "Molo - 9", "B": "Molo - 10", "distance": 20, "oneway": True},
    {"A": "Molo - 10", "B": "Molo - 7", "distance": 38, "oneway": True},
]


for road in roads:
    G.add_edge(road["A"], road["B"], length=road["distance"])
    if not road["oneway"]:
        G.add_edge(road["B"], road["A"], length=road["distance"])

molo_network = ox.plot_graph(G, show=True, close=False, edge_color="w")

# plt.savefig("molo_network_map.png", dpi=300, bbox_inches="tight")
# print("Plot saved as molo_network_map.png")
