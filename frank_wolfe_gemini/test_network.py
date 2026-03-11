from frank_wolfe import RouteDecomposer

# 1. Simulate a larger grid-like network links [cite: 267]
# In a real scenario, you'd load this from a file.
links = []
for i in range(1, 50):
    links.append({'id': f'L{i}', 'from': i, 'to': i+1})
    links.append({'id': f'B{i}', 'from': i, 'to': i+5}) # Example cross-links

# 2. Define OD Demands [cite: 53]
od_pairs = [
    {'origin': 1, 'dest': 10, 'demand': 100},
    {'origin': 2, 'dest': 15, 'demand': 50},
    {'origin': 5, 'dest': 20, 'demand': 75}
]

# 3. Simulate Link Flows by Destination (x_a^n) [cite: 56]
# For testing, we assign flow to paths manually to verify decomposition.
mock_flows = {
    10: {'L1': 100, 'L2': 100, 'L3': 100, 'L4': 100, 'L5': 100, 'L6': 100, 'L7': 100, 'L8': 100, 'L9': 100},
    15: {'L2': 50, 'L3': 50, 'L4': 50, 'L5': 50, 'L6': 50, 'L7': 50, 'L8': 50, 'L9': 50, 'L10': 50, 'L11': 50, 'L12': 50, 'L13': 50, 'L14': 50},
    20: {'B5': 75, 'L10': 75, 'L11': 75, 'L12': 75, 'L13': 75, 'L14': 75, 'L15': 75, 'L16': 75, 'L17': 75, 'L18': 75, 'L19': 75}
}

def main():
    decomposer = RouteDecomposer(links)
    
    print("Decomposing link flows into routes...")
    route_data = decomposer.decompose(od_pairs, mock_flows)
    
    # Save output
    decomposer.save_to_csv(route_data, "traffic_assignment_results.csv")

if __name__ == "__main__":
    main()