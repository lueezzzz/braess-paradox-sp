import osmnx as ox
import networkx as nx

G = nx.MultiDiGraph()
G.graph["crs"] = "EPSG:4326"

intersections = [
    {"id": "lapaz - 1", "y": 10.707804, "x": 122.567107},
    {"id": "lapaz - 2", "y": 10.708378, "x": 122.567858},
    {"id": "lapaz - 3", "y": 10.709233, "x": 122.566694},
    {"id": "lapaz - 4", "y": 10.710460, "x": 122.570379},
    {"id": "lapaz - 5", "y": 10.711606, "x": 122.571909},
    {"id": "lapaz - 6", "y": 10.713029, "x": 122.570879},
    {"id": "lapaz - 7", "y": 10.711777, "x": 122.569511},
    {"id": "lapaz - 8", "y": 10.714306, "x": 122.575493},
    {"id": "lapaz - 9", "y": 10.713908, "x": 122.581449},
    {"id": "lapaz - 10", "y": 10.706364, "x": 122.567494},
]

for node in intersections:
    G.add_node(node["id"], x=node["x"], y=node["y"])

roads = [
    {"A": "lapaz - 3", "B": "lapaz - 1", "distance": 170, "lanes": 2, "oneway": False},
    {"A": "lapaz - 1", "B": "lapaz - 10", "distance": 160, "lanes": 2, "oneway": False},
    {"A": "lapaz - 2", "B": "lapaz - 3", "distance": 160, "lanes": 4, "oneway": True},
    {"A": "lapaz - 1", "B": "lapaz - 2", "distance": 110, "lanes": 4, "oneway": True},
    {"A": "lapaz - 2", "B": "lapaz - 4", "distance": 350, "lanes": 2, "oneway": False},
    {"A": "lapaz - 4", "B": "lapaz - 5", "distance": 210, "lanes": 4, "oneway": True},
    {"A": "lapaz - 5", "B": "lapaz - 6", "distance": 200, "lanes": 4, "oneway": True},
    {"A": "lapaz - 6", "B": "lapaz - 7", "distance": 210, "lanes": 3, "oneway": True},
    {"A": "lapaz - 7", "B": "lapaz - 4", "distance": 180, "lanes": 4, "oneway": True},
    {"A": "lapaz - 5", "B": "lapaz - 8", "distance": 500, "lanes": 2, "oneway": False},
    {"A": "lapaz - 8", "B": "lapaz - 9", "distance": 650, "lanes": 2, "oneway": False},
]

for road in roads:
    G.add_edge(road["A"], road["B"], length=road["distance"])
    if not road["oneway"]:
        G.add_edge(road["B"], road["A"], length=road["distance"])

molo_network = ox.plot_graph(G, show=True, close=False, edge_color="w")

# plt.savefig("molo_network_map.png", dpi=300, bbox_inches="tight")
# print("Plot saved as molo_network_map.png")
