import networkx as nx

class TrafficNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_intersection(self, node_id):
        self.graph.add_node(node_id)

    def add_road(self, u, v, weight):
        self.graph.add_edge(u, v, weight=weight)

net = TrafficNetwork()

net.add_intersection("A")
net.add_intersection("B")
net.add_intersection("C")
net.add_intersection("D")

net.add_road("A", "B", 3)
net.add_road("A", "C", 7)
net.add_road("B", "C", 1)
net.add_road("B", "D", 7)
net.add_road("C", "D", 3)

net.add_road("B", "A", 3)
net.add_road("C", "A", 7)
net.add_road("C", "B", 1)
net.add_road("D", "B", 7)
net.add_road("D", "C", 3)