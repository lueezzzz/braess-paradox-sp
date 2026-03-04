import csv
import osmnx as ox
import networkx as nx

intersections = []
with open("data/intersections.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        intersections.append(
            {
                "id": row["id"],
                "y": float(row["y"]),
                "x": float(row["x"]),
                "name": row["name"],
            }
        )

roads = []
with open("data/roads.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        roads.append(
            {
                "A": row["A"],
                "B": row["B"],
                "distance": float(row["distance"]),
                "lanes": int(row["lanes"]),
                "oneway": row["oneway"].strip().lower() == "true",
                "name": row["name"],
            }
        )


G = nx.MultiDiGraph()
G.graph["crs"] = "EPSG:4326"

for node in intersections:
    G.add_node(node["id"], x=node["x"], y=node["y"])

for road in roads:
    G.add_edge(road["A"], road["B"], length=road["distance"])
    if not road["oneway"]:
        G.add_edge(road["B"], road["A"], length=road["distance"])

iloilo_network = ox.plot_graph(G, show=True, close=False, edge_color="w")

# plt.savefig("iloilo_network_map.png", dpi=300, bbox_inches="tight")
# print("Plot saved as iloilo_network_map.png")
