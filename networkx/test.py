import pandas as pd
import networkx as nx
import numpy as np
from scipy.optimize import minimize_scalar

class TrafficAssignment:
    def __init__(self, nodes_csv, roads_csv, alpha=0.2, beta=10, default_speed=40, lane_capacity=1400):
        self.nodes_df = pd.read_csv(nodes_csv)
        self.roads_df = pd.read_csv(roads_csv)
        self.alpha = alpha
        self.beta = beta
        self.default_speed = default_speed
        self.lane_capacity = lane_capacity
        self.G = self._build_graph()
        self.edges = list(self.G.edges())
        self.num_edges = len(self.edges)
        self.t0 = np.array([self.G[u][v]['t0'] for u, v in self.edges])
        self.caps = np.array([self.G[u][v]['cap'] for u, v in self.edges])

    def _build_graph(self):
        G = nx.DiGraph()
        for _, r in self.roads_df.iterrows():
            free_flow_time = r['distance'] / (self.default_speed * 1000 / 60)  # Convert to m/min 
            
            total_capacity = self.lane_capacity * r['lanes']
            
            G.add_edge(r['A'], r['B'], t0=free_flow_time, cap=total_capacity, name=r['name'])
            
            if not r['oneway']:
                G.add_edge(r['B'], r['A'], t0=free_flow_time, cap=total_capacity, name=r['name'] + " (Reverse)")
        return G

    def bpr_latency(self, flow):
        """Standard BPR function for User Equilibrium."""
        return self.t0 * (1 + self.alpha * (flow / self.caps)**self.beta)

    def marginal_social_cost(self, flow):
        """Marginal cost function for System Optimum."""
        return self.t0 * (1 + self.alpha * (self.beta + 1) * (flow / self.caps)**self.beta)

    def beckmann_integral(self, flow, mode='UE'):
        """Objective function for the line search."""
        if mode == 'UE':
            return np.sum(self.t0 * (flow + (self.alpha * flow**(self.beta + 1)) / 
                          (self.caps**self.beta * (self.beta + 1))))
        else:
            return np.sum(flow * self.bpr_latency(flow))

    def _all_or_nothing(self, costs, od_matrix):
        nx.set_edge_attributes(self.G, {self.edges[i]: costs[i] for i in range(self.num_edges)}, 'cost')
        new_flow = np.zeros(self.num_edges)
        for (orig, dest), demand in od_matrix.items():
            try:
                path = nx.shortest_path(self.G, orig, dest, weight='cost')
                for i in range(len(path)-1):
                    idx = self.edges.index((path[i], path[i+1]))
                    new_flow[idx] += demand
            except nx.NetworkXNoPath:
                continue
        return new_flow

    def solver(self, od_matrix, mode='UE', max_iter=100, tol=1e-6):
        # Initialization
        x = self._all_or_nothing(self.t0, od_matrix)
        
        for i in range(max_iter):
            # Update Costs based on Mode
            if mode == 'UE':
                costs = self.bpr_latency(x)
            else:
                costs = self.marginal_social_cost(x)
            
            # Direction Finding (AoN)
            y = self._all_or_nothing(costs, od_matrix)
            
            # Line Search for Step Size (Alpha)
            def obj(a):
                return self.beckmann_integral(x + a * (y - x), mode)
            
            res = minimize_scalar(obj, bounds=(0, 1), method='bounded')
            step = res.x
            
            # Update and Convergence
            new_x = x + step * (y - x)
            if np.linalg.norm(new_x - x) / (np.linalg.norm(x) + 1e-9) < tol:
                break
            x = new_x
            
        return x

    def calculate_poa(self, od_matrix):
        flow_ue = self.solver(od_matrix, mode='UE')
        tstt_ue = np.sum(flow_ue * self.bpr_latency(flow_ue))

        flow_so = self.solver(od_matrix, mode='SO')
        tstt_so = np.sum(flow_so * self.bpr_latency(flow_so))

        poa = tstt_ue / tstt_so
        return poa, tstt_ue, tstt_so

G = TrafficAssignment('intersections.csv', 'roads.csv')

iloilo_od_weights = {
    ("villa - 1", "Proper - 14"): 0.40,   # 40% of all traffic
    ("jaro - 4", "Proper - 1"): 0.35,    # 35% of all traffic
    ("mandurriao - 2", "Proper - 13"): 0.25  # 25% of all traffic
}

def get_scaled_demand(weights, total_volume):
    return {pair: weight * total_volume for pair, weight in weights.items()}

results = []
for v in range(500, 10001, 500):
    current_demand = get_scaled_demand(iloilo_od_weights, v)
    
    # Calculate UE and SO to get PoA
    poa, ue_time, so_time = G.calculate_poa(current_demand)
    
    results.append({
        'volume': v,
        'poa': poa,
        'ue_time': ue_time
    })

df_results = pd.DataFrame(results)
peak_volume = df_results.loc[df_results['poa'].idxmax()]['volume']
print(df_results)
print(f"Peak Anarchy occurs at a total volume of: {peak_volume}")