import pandas as pd
from network_import import _net_file2df, _demand_file2trips
import os

def convert_tntp_to_py(net_file, demand_file, output_py_file):
    # 1. Load the data using existing logic from network_import.py
    print(f"Reading {net_file}...")
    net_df = _net_file2df(net_file)
    
    print(f"Reading {demand_file}...")
    trip_set = _demand_file2trips(demand_file)
    
    # 2. Convert Demand dictionary to a list of records
    demand_list = []
    for orig in trip_set:
        for dest, demand in trip_set[orig].items():
            demand_list.append({
                "init_node": orig, 
                "term_node": dest, 
                "demand": demand
            })
            
    # 3. Format as a Python file string
    with open(output_py_file, 'w') as f:
        f.write("# Auto-generated from TNTP source\n\n")
        # Use repr to ensure the dictionary structure is preserved as valid Python code
        f.write("network_data = " + net_df.to_dict(orient='records').__repr__() + "\n\n")
        f.write("demand_data = " + str(demand_list))
        
    print(f"--- Success! Created {output_py_file} ---")

if __name__ == "__main__":
    # --- TYPING THE NAME STARTS HERE ---
    file_prefix = input("Enter the network name (e.g., SiouxFalls or Iloilo): ").strip()
    
    # Construct paths based on the name provided
    net_path = f"{file_prefix}_net.tntp"
    trips_path = f"{file_prefix}_trips.tntp"
    output_name = f"{file_prefix}_data.py"

    # Check if files exist before running to avoid crashes
    if os.path.exists(net_path) and os.path.exists(trips_path):
        convert_tntp_to_py(
            net_file=net_path, 
            demand_file=trips_path, 
            output_py_file=output_name
        )
    else:
        print(f"Error: Could not find '{net_path}' or '{trips_path}' in the current folder.")