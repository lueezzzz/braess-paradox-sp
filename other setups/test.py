import pandas as pd
import networkx as nx
import math
import scipy.optimize
import numpy as np
import os

def bpr_cost(fft, alpha, flow, capacity, beta):
    if capacity < 1e-3: return np.finfo(np.float32).max
    return fft * (1 + alpha * math.pow((flow / capacity), beta))

def marginal_cost(fft, alpha, flow, capacity, beta):
    if capacity < 1e-3: return np.finfo(np.float32).max
    return fft * (1 + alpha * (beta + 1) * math.pow((flow / capacity), beta))

def update_travel_times(graph, is_so=False):
    for u, v, d in graph.edges(data=True):
        if is_so:
            d['weight'] = marginal_cost(d['fft'], d['alpha'], d['flow'], d['capacity'], d['beta'])
        else:
            d['weight'] = bpr_cost(d['fft'], d['alpha'], d['flow'], d['capacity'], d['beta'])

def load_aon(graph, demands):
    x_bar = {edge: 0.0 for edge in graph.edges()} 
    SPTT = 0.0 
    dropped_vol = 0.0 
    
    for demand in demands:
        try:
            path = nx.shortest_path(graph, demand['origin'], demand['destination'], weight='weight')
            path_cost = sum(graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
            SPTT += path_cost * demand['volume']
            for i in range(len(path)-1):
                x_bar[(path[i], path[i+1])] += demand['volume']
        except nx.NetworkXNoPath:
            dropped_vol += demand['volume']
            
    return SPTT, x_bar, dropped_vol

def find_alpha(graph, x_bar, is_so=False):
    def df(alpha):
        sum_deriv = 0.0
        for u, v, d in graph.edges(data=True):
            tmp_flow = alpha * x_bar.get((u, v), 0.0) + (1 - alpha) * d['flow']
            tmp_cost = marginal_cost(d['fft'], d['alpha'], tmp_flow, d['capacity'], d['beta']) if is_so else bpr_cost(d['fft'], d['alpha'], tmp_flow, d['capacity'], d['beta'])
            sum_deriv += (x_bar.get((u, v), 0.0) - d['flow']) * tmp_cost
        return sum_deriv
    
    val_0, val_1 = df(0.0), df(1.0)
    if val_0 >= 0.0: return 0.0 
    if val_1 <= 0.0: return 1.0 
    
    sol = scipy.optimize.root_scalar(df, x0=0.5, bracket=(0.0, 1.0))
    return max(0.0, min(1.0, sol.root))

def solve_equilibrium(graph, demands, is_so=False, accuracy=0.001, max_iter=50):
    for u, v, d in graph.edges(data=True): d['flow'] = 0.0
    gap = np.inf
    iteration = 1
    TSTT = 0.0
    
    while gap > accuracy and iteration <= max_iter:
        update_travel_times(graph, is_so)
        SPTT, x_bar, dropped_vol = load_aon(graph, demands)
        if dropped_vol > 0: return float('inf'), dropped_vol 
        
        alpha = 1.0 if iteration == 1 else find_alpha(graph, x_bar, is_so)
        for u, v, d in graph.edges(data=True):
            d['flow'] = alpha * x_bar.get((u, v), 0.0) + (1 - alpha) * d['flow']
        
        update_travel_times(graph, is_so)
        SPTT, _, _ = load_aon(graph, demands)
        TSTT = sum(d['flow'] * bpr_cost(d['fft'], d['alpha'], d['flow'], d['capacity'], d['beta']) for u, v, d in graph.edges(data=True))
        gap = (TSTT / SPTT) - 1.0 if SPTT > 0 else 0.0
        iteration += 1
    
    return TSTT, 0.0

print("Loading CSV network data...")
nodes_df = pd.read_csv('intersections.csv')
edges_df = pd.read_csv('roads_updated.csv')
edges_df['oneway'] = edges_df['oneway'].astype(str).str.strip().str.lower().isin(['true', '1', 'yes', 't'])

G = nx.DiGraph()
CAP_PER_LANE = 1100 

for _, row in nodes_df.iterrows():
    G.add_node(str(row['id']).strip(), name=row['name'])

for _, row in edges_df.iterrows():
    u, v = str(row['A']).strip(), str(row['B']).strip()
    if u not in G.nodes or v not in G.nodes: continue
    
    dist_km = float(row['distance']) / 1000.0
    speed = float(row.get('speed', 40.0))
    fft = dist_km / speed 
    cap = int(row.get('lanes', 1)) * CAP_PER_LANE
    base_name = str(row.get('name', '')).strip()
    link_attrs = {'fft': fft, 'flow': 0.0, 'weight': fft, 'name': base_name, 'alpha': 0.15, 'beta': 4.0, 'capacity': cap}
    
    if row['oneway']:
        G.add_edge(u, v, **link_attrs)
    else:
        G.add_edge(u, v, **link_attrs)
        rev_attrs = link_attrs.copy()
        rev_attrs['name'] = f"{base_name} (Rev)"
        G.add_edge(v, u, **rev_attrs)

node_list = list(G.nodes)
total_nodes = len(node_list)
total_pairs = total_nodes * (total_nodes - 1)

print(f"\nINITIATING EXHAUSTIVE ALL-PAIRS PoA AUDIT")
print(f"Total possible Origin-Destination combinations to test: {total_pairs}")

output_filename = "All_Pairs_True_PoA_Results.csv"
volumes_to_test = np.arange(500, 10500, 500) 
candidate_edges = [(u, v, d.get('name', 'Unnamed Road')) for u, v, d in G.edges(data=True)]

if not os.path.exists(output_filename):
    pd.DataFrame(columns=['Origin Node', 'Origin Name', 'Destination Node', 'Destination Name', 'Critical Volume', 'Max PoA', 'Road Name', 'Closed Edge From', 'Closed Edge To', 'Baseline TSTT (hrs)', 'New TSTT (hrs)', 'Time Saved (mins)']).to_csv(output_filename, index=False)
pair_count = 0
found_braess_count = 0

for origin_node in node_list:
    for destination_node in node_list:
        if origin_node == destination_node: continue
        pair_count += 1
        
        if pair_count % 10 == 0:
            print(f"--- Progress: Tested {pair_count} / {total_pairs} pairs. Found {found_braess_count} Braess traps so far. ---")
            
        if not nx.has_path(G, origin_node, destination_node): continue

        origin_name = G.nodes[origin_node].get('name', 'N/A')
        dest_name = G.nodes[destination_node].get('name', 'N/A')

        # POA VOLUME SWEEP
        poa_results = []
        network_failed = False

        for vol in volumes_to_test:
            single_demand = [{'origin': origin_node, 'destination': destination_node, 'volume': vol}]
            
            # Calculate UE (Selfish)
            tstt_ue, dropped = solve_equilibrium(G, single_demand, is_so=False)
            if dropped > 0:
                network_failed = True
                break 
                
            # Calculate SO (Altruistic)
            tstt_so, _ = solve_equilibrium(G, single_demand, is_so=True)
            
            poa = tstt_ue / tstt_so if tstt_so > 0 else 1.0
            poa_results.append({'Volume': vol, 'Price of Anarchy': poa})

        if not poa_results: continue # Skip if failed on 500 volume
        
        df_poa = pd.DataFrame(poa_results)
        highest_vol_tested = df_poa['Volume'].max()
        max_poa_row = df_poa.loc[df_poa['Price of Anarchy'].idxmax()]
        optimal_volume = max_poa_row['Volume']
        max_poa_value = max_poa_row['Price of Anarchy']

        # print(f"Pair {pair_count}/{total_pairs} | {origin_node} -> {destination_node} | Max PoA: {max_poa_value:.4f} | Max Volume: {highest_vol_tested}")

        # If PoA is basically 1.0 everywhere, skip to save hours of processing time
        if max_poa_value < 1.01:
            continue

        # PERTURBATION AUDIT AT CRITICAL VOLUME
        locked_demand = [{'origin': origin_node, 'destination': destination_node, 'volume': optimal_volume}]
        baseline_tstt_ph2, _ = solve_equilibrium(G, locked_demand, is_so=False)
        
        pair_results = []
        
        for u, v, road_name in candidate_edges:
            edge_data = G[u][v].copy()
            
            G.remove_edge(u, v)
            new_tstt, dropped_vol = solve_equilibrium(G, locked_demand, is_so=False)
            G.add_edge(u, v, **edge_data) 
                
            if dropped_vol > 0: continue 
                
            time_diff_mins = (new_tstt - baseline_tstt_ph2) * 60
            
            # Save if the closure saves > 0.5 minutes
            if time_diff_mins < -0.5: 
                
                print(f"  [!] BRAESS FOUND IN {origin_node} -> {destination_node}: Closing {road_name} ({u}->{v}) saves {abs(time_diff_mins):.2f} mins!")

                pair_results.append({
                    'Origin Node': origin_node,
                    'Origin Name': origin_name,
                    'Destination Node': destination_node,
                    'Destination Name': dest_name,
                    'Critical Volume': optimal_volume,
                    'Max PoA': round(max_poa_value, 4),
                    'Road Name': road_name,
                    'Closed Edge From': u,
                    'Closed Edge To': v,
                    'Baseline TSTT (hrs)': round(baseline_tstt_ph2, 2),
                    'New TSTT (hrs)': round(new_tstt, 2),
                    'Time Saved (mins)': round(abs(time_diff_mins), 2)
                })

        # Append immediately to CSV
        if pair_results:
            found_braess_count += len(pair_results)
            pd.DataFrame(pair_results).to_csv(output_filename, mode='a', header=False, index=False)

print(f"\nEXHAUSTIVE AUDIT COMPLETE.")
print(f"Total Braess Candidates Found: {found_braess_count}")
print(f"Results saved to {output_filename}")