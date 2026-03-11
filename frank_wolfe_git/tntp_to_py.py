import pandas as pd
from network_import import _net_file2df, _demand_file2trips
from utils import PathUtils

def convert_tntp_to_py(net_file, demand_file, output_py_file):
    # 1. Load the data using existing logic from network_import.py
    net_df = _net_file2df(net_file)
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
        f.write("network_data = " + net_df.to_dict(orient='records').__repr__() + "\n\n")
        f.write("demand_data = " + str(demand_list))
        
    print(f"Successfully converted to {output_py_file}")

# --- WHERE TO PUT THE FILE PATHS ---
if __name__ == "__main__":
    # Reference the files using the paths defined in PathUtils
    net_path = str(PathUtils.sioux_falls_net_file)
    # Construct the trip file path manually or via PathUtils if defined
    trips_path = net_path.replace("_net.tntp", "_trips.tntp")
    
    # Call the conversion
    convert_tntp_to_py(
        net_file=net_path, 
        demand_file=trips_path, 
        output_py_file='sioux_falls_data.py'
    )