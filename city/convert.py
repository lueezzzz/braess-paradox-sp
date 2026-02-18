import json
import re
import ast
import glob
import os

def strip_js_comments(text):
    # Removes JS-style comments (// line comments and /* block comments */)
    # while preserving strings that might contain '//' or '/*'.
    
    pattern = r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')|(\/\*[\s\S]*?\*\/)|(\/\/[^\n]*)'

    def replacer(match):
        # If the match is a string (Group 1), return it unchanged
        if match.group(1):
            return match.group(1)
        # Otherwise (it's a comment), return an empty string
        return ""

    return re.sub(pattern, replacer, text)

def extract_variable_block(content, var_name):
    # Robustly extracts a variable's content (e.g., 'intersections = [...]')
    # by counting brackets to handle nested lists.

    # Find the start of the variable assignment
    pattern = f"{var_name}\s*=\s*\["
    match = re.search(pattern, content)
    
    if not match:
        return None
    
    # Start looking from the opening bracket '['
    start_index = match.end() - 1 
    balance = 0
    
    for i in range(start_index, len(content)):
        char = content[i]
        if char == '[':
            balance += 1
        elif char == ']':
            balance -= 1
            # When balance returns to 0, we found the closing bracket
            if balance == 0:
                return content[start_index : i+1]
                
    return None

def parse_js_block(block_str):
    if not block_str:
        return []
        
    # Quote unquoted keys (e.g., id: -> "id":)
    block_str = re.sub(r'(?<!")(\b\w+)\s*:', r'"\1":', block_str)
    
    # Convert JS Booleans to Python
    block_str = re.sub(r'\bfalse\b', 'False', block_str)
    block_str = re.sub(r'\btrue\b', 'True', block_str)
    
    # Safely evaluate
    try:
        return ast.literal_eval(block_str)
    except Exception as e:
        print(f"    Error parsing block: {e}")
        return []

def convert_all_files(folder_path=".", output_filename="city_network.json"):
    all_nodes = []
    all_links = []
    
    files = glob.glob(os.path.join(folder_path, "*.js"))
    print(f"Found {len(files)} files. Processing...")

    for file_path in files:
        print(f"  Reading {os.path.basename(file_path)}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        # Strip comments
        clean_content = strip_js_comments(raw_content)

        # Extract and parse
        # Process 'intersections'
        inter_block = extract_variable_block(clean_content, "intersections")
        if inter_block:
            intersections = parse_js_block(inter_block)
            for node in intersections:
                all_nodes.append({
                    "id": node["id"],
                    "name": node["name"],
                    "pos": (node.get("longitude", 0), node.get("latitude", 0)),
                    "connections": node.get("connections", [])
                })
        
        # Process 'roads'
        road_block = extract_variable_block(clean_content, "roads")
        if road_block:
            roads = parse_js_block(road_block)
            for road in roads:
                all_links.append({
                    "source": road["A"],
                    "target": road["B"],
                    "name": road["name"],
                    "distance": road["distance"],
                    "lanes": road.get("lanes", 1),
                    "one_way": road.get("one_way", False)
                })

    # Save final output
    final_network = {
        "nodes": all_nodes,
        "links": all_links
    }

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_network, f, indent=2)

    print(f"\nSuccess! Saved to '{output_filename}'")
    print(f"Total Nodes: {len(all_nodes)}")
    print(f"Total Links: {len(all_links)}")

if __name__ == "__main__":
    convert_all_files()