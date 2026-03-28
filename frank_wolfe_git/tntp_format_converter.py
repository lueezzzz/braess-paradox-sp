import arevalo as network # Updated to import the provided arevalo.py
import sys

def convert_to_tntp():
    # 1. Gather all unique nodes from intersections, roads, and connection strings
    nodes = set()
    for item in network.intersections:
        nodes.add(item['id'])
        for conn in item.get('connections', []):
            nodes.add(conn)
            
    for r in network.roads:
        nodes.add(r['A'])
        nodes.add(r['B'])
    
    # Create numeric mapping (1-based index) for TNTP format
    node_map = {name: i + 1 for i, name in enumerate(sorted(list(nodes)))}
    
    # 2. Generate network link data
    network_data = []
    for r in network.roads:
        # Note: arevalo.py currently lacks a 'speed' field; using 30 as a default 
        speed = r.get('speed', 30) 
        
        link = {
            'init_node': node_map[r['A']],
            'term_node': node_map[r['B']],
            'capacity': float(r['lanes'] * 1800), 
            'length': round(r['distance'] / 1000.0, 3),
            'free_flow_time': round(r['distance'] / speed if speed > 0 else 0, 3),
            'b': 0.15, # Standard BPR alpha
            'power': 4, # Standard BPR beta
            'speed': speed,
            'toll': 0,
            'link_type': 1
        }
        network_data.append(link)
        
        # Handle two-way roads
        if not r.get('one_way', False):
            rev = link.copy()
            rev['init_node'], rev['term_node'] = link['term_node'], link['init_node']
            network_data.append(rev)

    # 3. Generate demand data (OD Matrix) based on connections
    demand_data = []
    seen_pairs = set()
    
    for item in network.intersections:
        origin_idx = node_map[item['id']]
        for conn_id_str in item.get('connections', []):
            dest_idx = node_map[conn_id_str]
            
            # Create a sorted tuple: (min, max). 
            # This ensures (1, 2) and (2, 1) result in the same key.
            pair = tuple(sorted((origin_idx, dest_idx)))
            
            # Only add if the pair hasn't been seen and isn't a self-loop
            if pair not in seen_pairs and origin_idx != dest_idx:
                seen_pairs.add(pair)
                demand_data.append({
                    'init_node': pair[0], 
                    'term_node': pair[1], 
                    'demand': 0.0
                })

    # 4. Output to final_network_tntp.py
    with open('final_network_tntp.py', 'w') as f:
        f.write("# Auto-generated TNTP-style data from arevalo.py\n\n")
        f.write("# Node Mapping Reference:\n")
        for name, idx in node_map.items(): 
            f.write(f"# {idx}: {name}\n")
            
        f.write("\nnetwork_data = [\n")
        for item in network_data: 
            f.write(f"    {item},\n")
        f.write("]\n\ndemand_data = [\n")
        for item in demand_data: 
            f.write(f"    {item},\n")
        f.write("]\n")

if __name__ == "__main__":
    convert_to_tntp()