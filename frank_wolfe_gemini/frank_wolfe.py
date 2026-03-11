import csv
from collections import defaultdict

class RouteDecomposer:
    def __init__(self, links):
        """
        links: List of dictionaries [{'id': 'a', 'from': 1, 'to': 2}, ...]
        """
        self.links = links
        # Create an adjacency list for faster lookups in large networks
        self.adj = defaultdict(list)
        for link in links:
            self.adj[link['from']].append(link)

    def find_path_with_flow(self, start_node, end_node, flow_map):
        """
        Finds a path from start to end using only links with flow > 0 for a specific destination.
        """
        stack = [(start_node, [])]
        visited = set()
        
        while stack:
            current, path = stack.pop()
            if current == end_node:
                return path
            
            if current in visited:
                continue
            visited.add(current)
            
            for link in self.adj[current]:
                # Only follow links that have remaining flow for this destination
                if flow_map.get(link['id'], 0) > 1e-9:
                    stack.append((link['to'], path + [link['id']]))
        return None

    def decompose(self, od_demands, link_flows_by_dest):
        """
        Implements Algorithm 2.1[cite: 108].
        od_demands: List of {'origin': O, 'dest': D, 'demand': Q}
        link_flows_by_dest: Dict {dest_node: {link_id: flow}}
        """
        all_route_flows = []
        
        # Work on a local copy of flow data to avoid side effects
        remaining_flows = {
            d: {l_id: val for l_id, val in flows.items()} 
            for d, flows in link_flows_by_dest.items()
        }

        for i, od in enumerate(od_demands):
            origin = od['origin']
            dest = od['dest']
            q_hat = od['demand']
            
            # Destination-specific flow map [cite: 56, 100]
            dest_flows = remaining_flows.get(dest, {})
            
            while q_hat > 1e-8:
                path = self.find_path_with_flow(origin, dest, dest_flows)
                if not path:
                    break # No more flow-carrying paths found [cite: 119]
                
                # Step 2: Determine minimum flow on this route [cite: 110]
                min_link_flow = min(dest_flows[l_id] for l_id in path)
                flow_to_assign = min(q_hat, min_link_flow)
                
                all_route_flows.append({
                    'origin': origin,
                    'dest': dest,
                    'path': "->".join(path),
                    'flow': flow_to_assign
                })
                
                # Step 3: Update remaining demand and link flows [cite: 111, 116]
                q_hat -= flow_to_assign
                for link_id in path:
                    dest_flows[link_id] -= flow_to_assign
                    
        return all_route_flows

    def save_to_csv(self, route_flows, filename="route_outputs.csv"):
        """Formats the output into a CSV as requested."""
        keys = ['origin', 'dest', 'path', 'flow']
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(route_flows)
        print(f"Successfully saved {len(route_flows)} routes to {filename}")