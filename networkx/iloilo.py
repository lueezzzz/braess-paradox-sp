import networkx as nx

# Default BPR function parameters
ALPHA = 0.15
BETA = 4

class TrafficNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_intersection(self, node_id, name):
        # Add a node representing an intersection
        self.graph.add_node(node_id, name=name)

    def add_road(self, u, v, name, free_flow_time, capacity=1000, one_way=False):
        # Add a directed edge representing a road with attributes
        self.graph.add_edge(u, v, 
                            name = name,
                            free_flow_time = free_flow_time,
                            capacity = capacity,
                            flow = 0)
        
        if not one_way:
            self.graph.add_edge(v, u,
                                name = name + " (Reverse)", 
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

    def simulate_traffic(self, start, end, demand=5000):
        # Reset flows before simulation
        self.reset_flows()
    
        # For each driver, assign traffic based on shortest path
        for _ in range(demand):
            path = nx.shortest_path(self.graph, 
                                    source=start, 
                                    target=end, 
                                    weight=self.get_road_cost)
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.graph[u][v]['flow'] += 1

        # Calculate total travel time after all drivers have chosen their paths
        final_time = nx.shortest_path_length(self.graph, 
                                               source=start, 
                                               target=end, 
                                               weight=self.get_road_cost)
    
        return final_time

    def print_network_state(self):
        # Print the flow and cost on each road
        for u, v in self.graph.edges():
            edge = self.graph[u][v]
            cost = self.calculate_bpr_cost(edge['flow'], 
                                           edge['free_flow_time'], 
                                           edge['capacity'])
            print(f"{edge['name']}: \nFlow = {edge['flow']}, \tCost = {cost:.2f}")

net = TrafficNetwork()

# Intialize intersections
intersections = [("1", "Gen Luna St - Infante St"),
                 ("2", "Gen Luna St - Ybernias St"),
                 ("3", "Gen Luna St - Jalandoni St"),
                 ("4", "Gen Luna St - Mabini St"),
                 ("5", "Gen Luna St - Quezon St"),
                 ("6", "Gen Luna St - Valeria St"),
                 ("7", "Gen Luna St - Ruperto Montinola St"),
                 ("8", "Delgado St - Infante St"),
                 ("9", "Delgado St - Ybernias St"),
                 ("10", "Delgado St - Jalandoni St"),
                 ("11", "Delgado St - Mabini St"),
                 ("12", "Delgado St - Quezon St"),
                 ("13", "Delgado St - Valeria St"),
                 ("14", "Delgado St - Ruperto Montinola St")]

for intersection, name in intersections:
    net.add_intersection(intersection, name)

# Initialize roads (MODIFY FFT AND CAPACITY AS NEEDED)
roads = [("1", "2", "Gen Luna St 1", 2, 500, True),
         ("2", "3", "Gen Luna St 2", 2, 500, True),
         ("3", "1", "Gen Luna St 1 2 (Reverse)", 2, 500, True),
         ("3", "4", "Gen Luna St 3", 2, 500, False),
         ("4", "5", "Gen Luna St 4", 2, 500, True),
         ("5", "6", "Gen Luna St 5", 2, 500, True),
         ("6", "7", "Gen Luna St 6", 2, 500, True),
         ("7", "4", "Gen Luna St 4 5 6 (Reverse)", 2, 500, True),
         ("8", "9", "Delgado St 1", 2, 500, False),
         ("9", "10", "Delgado St 2", 2, 500, False),
         ("10", "11", "Delgado St 3", 2, 500, False),
         ("11", "12", "Delgado St 4", 2, 500, False),
         ("12", "13", "Delgado St 5", 2, 500, False),
         ("13", "14", "Delgado St 6", 2, 500, False),
         ("1", "8", "Infante St", 1, 300, False),
         ("2", "9", "Ybernias St", 1, 300, False),
         ("3", "10", "Jalandoni St", 1, 300, False),
         ("4", "11", "Mabini St", 1, 300, False),
         ("5", "12", "Quezon St", 1, 300, False),
         ("13", "6", "Valeria St", 1, 300, True),
         ("7", "14", "Ruperto Montinola St", 1, 300, False)]

for u, v, name, fft, cap, one_way in roads:
    net.add_road(u, v, name, fft, cap, one_way=one_way)

time_before = net.simulate_traffic(start="1", end="14", demand=5000)
print("Before Road Removal")
net.print_network_state()

# Remove a road to simulate closure (CHANGE TO DESIRED ROAD)
net.remove_road("7", "14")
net.remove_road("14", "7")

time_after = net.simulate_traffic(start="1", end="14", demand=5000)
print("\n\nAfter Road Removal")
net.print_network_state()

print(f"\n\nTotal travel time before road removal: {time_before}")
print(f"Total travel time after road removal: {time_after}")