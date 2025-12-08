import networkx as nx

# Default BPR function parameters
ALPHA = 0.15
BETA = 4

class TrafficNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_intersection(self, node_id):
        # Add a node representing an intersection
        self.graph.add_node(node_id)

    def add_road(self, u, v, free_flow_time, capacity=1000):
        # Add a directed edge representing a road with attributes
        self.graph.add_edge(u, v, 
                            free_flow_time = free_flow_time,
                            capacity = capacity,
                            flow = 0)
    
    def remove_road(self, u, v):
        # Remove a directed edge representing a road
        if self.graph.has_edge(u, v):
            self.graph.remove_edge(u, v)

    def calculate_bpr_cost(self, flow, free_flow_time, capacity):
        # Calculate travel time using the BPR function
        if capacity is None or capacity == 0:
            return free_flow_time
        return free_flow_time * (1 + ALPHA * (flow / capacity) ** BETA)
    
    def get_road_cost(self, u, v, d):
        # Get the cost of traveling on a road considering current flow
        return self.calculate_bpr_cost(d['flow'] + 1,
                                       d['free_flow_time'],
                                       d['capacity'])

    def reset_flows(self):
        # Reset all road flows to zero
        for u, v in self.graph.edges():
            self.graph[u][v]['flow'] = 0

    def simulate_traffic(self, demand=5000):
        # Reset flows before simulation
        self.reset_flows()
    
        # For each driver, assign traffic based on shortest path
        for _ in range(demand):
            path = nx.shortest_path(self.graph, 
                                    source="start", 
                                    target="end", 
                                    weight=self.get_road_cost)
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.graph[u][v]['flow'] += 1

        # Calculate total travel time after all drivers have chosen their paths
        final_time = nx.shortest_path_length(self.graph, 
                                               source="start", 
                                               target="end", 
                                               weight=self.get_road_cost)
    
        return final_time

    def print_network_state(self):
        # Print the flow and cost on each road
        for u, v in self.graph.edges():
            edge = self.graph[u][v]
            cost = self.calculate_bpr_cost(edge['flow'], 
                                           edge['free_flow_time'], 
                                           edge['capacity'])
            print(f"Road from {u} to {v}: Flow = {edge['flow']}, Cost = {cost:.2f}")

net = TrafficNetwork()

intersections = ["start", 
                 "A", 
                 "B", 
                 "end"]
for intersection in intersections:
    net.add_intersection(intersection)

roads = [("start", "A", 15, 2000),
         ("start", "B", 30, 10000),
         ("A", "end", 30, 10000),
         ("B", "end", 15, 2000),
         ("A", "B", 5, 100000)]
for u, v, fft, cap in roads:
    net.add_road(u, v, fft, cap)

time_before = net.simulate_traffic(demand=5000)
print("Before Road Removal")
net.print_network_state()

net.remove_road("A", "B")

time_after = net.simulate_traffic(demand=5000)
print("\n\nAfter Road Removal")
net.print_network_state()

print(f"\n\nTotal travel time before road removal: {time_before}")
print(f"Total travel time after road removal: {time_after}")