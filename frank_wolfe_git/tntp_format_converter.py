# Have to change every file name
import arevalo
import sys

def convert_to_tntp():
    # Gather all unique nodes
    nodes = set()
    for item in arevalo.intersections: nodes.add(item['id'])
    for r in arevalo.roads:
        nodes.add(r['A'])
        nodes.add(r['B'])
    
    node_map = {name: i + 1 for i, name in enumerate(sorted(list(nodes)))}
    
    network_data = []
    for r in arevalo.roads:
        # Strict logic implementation
        link = {
            'init_node': node_map[r['A']],
            'term_node': node_map[r['B']],
            'capacity': float(r['lanes'] * 1800), 
            'length': round(r['distance'] / 1000.0, 3),
            'free_flow_time': 0.0,
            'b': 0.15,
            'power': 4,
            'speed': 0,
            'toll': 0,
            'link_type': 1
        }
        network_data.append(link)
        
        if not r.get('one_way', False):
            rev = link.copy()
            rev['init_node'], rev['term_node'] = link['term_node'], link['init_node']
            network_data.append(rev)

    demand_data = []
    ids = sorted(node_map.values())
    for o in ids:
        for d in ids:
            demand_data.append({'init_node': o, 'term_node': d, 'demand': 0.0})

    with open('arevalo_tntp.py', 'w') as f:
        f.write("# Auto-generated TNTP-style data from arevalo.py\n\n")
        f.write("# Node Mapping Reference:\n")
        for name, idx in node_map.items(): f.write(f"# {idx}: {name}\n")
        f.write("\nnetwork_data = [\n")
        for item in network_data: f.write(f"    {item},\n")
        f.write("]\n\ndemand_data = [\n")
        for item in demand_data: f.write(f"    {item},\n")
        f.write("]\n")

if __name__ == "__main__":
    convert_to_tntp()