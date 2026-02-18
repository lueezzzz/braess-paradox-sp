import json
import matplotlib.pyplot as plt

def visualize_network(json_file="city_network.json"):
    # Load Data
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{json_file}' not found. Please run the conversion script first.")
        return

    # Setup Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')  # Keep lat/long scaling correct
    ax.set_title("City Road Network", fontsize=15)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Dictionary for quick coordinate lookup: id -> (lon, lat)
    node_pos = {node["id"]: node["pos"] for node in data["nodes"]}

    # Draw Roads (Edges)
    print(f"Plotting {len(data['links'])} roads...")
    for link in data["links"]:
        u, v = link["source"], link["target"]
        
        if u in node_pos and v in node_pos:
            x1, y1 = node_pos[u]
            x2, y2 = node_pos[v]
            
            # Style: 
            # Blue = Two-way
            # Red/Dashed = One-way
            color = 'red' if link.get("one_way") else 'blue'
            style = '--' if link.get("one_way") else '-'
            alpha = 0.6
            
            ax.plot([x1, x2], [y1, y2], c=color, ls=style, alpha=alpha, linewidth=1)

            # Optional: Add small arrows for one-way streets
            if link.get("one_way"):
                # Calculate mid-point for arrow
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                dx = (x2 - x1) * 0.05 # Shorten arrow vector
                dy = (y2 - y1) * 0.05
                ax.arrow(mid_x, mid_y, dx, dy, shape='full', lw=0, 
                         length_includes_head=True, head_width=0.0001, color='red')

    # Draw Intersections (Nodes)
    print(f"Plotting {len(data['nodes'])} intersections...")
    x_coords = [pos[0] for pos in node_pos.values()]
    y_coords = [pos[1] for pos in node_pos.values()]
    
    ax.scatter(x_coords, y_coords, c='black', s=10, zorder=5)

    # Optional: Label some nodes (e.g., just the IDs)
    # Be careful, if you have 100+ nodes, this will look messy!
    # for node_id, (x, y) in node_pos.items():
    #     ax.text(x, y, node_id, fontsize=6)

    # Show
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_network()