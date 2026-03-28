import re

def update_network_file():
    input_file = 'final_network.py'
    output_file = 'final_network_updated.py'
    default_speed = 40

    try:
        with open(input_file, 'r') as f:
            content = f.read()

        # Split content to isolate the 'roads' list 
        # (This prevents adding speed to the 'intersections' list by mistake)
        parts = content.split("roads = [")
        if len(parts) < 2:
            print("Error: Could not find the 'roads' list in the file.")
            return

        header = parts[0] + "roads = ["
        roads_body = parts[1]

        # This regex finds the closing brace '},' of each road entry.
        # It captures the newline and spaces (\1) to match your indentation.
        # It then inserts the speed value right above the closing brace.
        updated_body = re.sub(
            r'(\n\s+)(},)', 
            fr'\1    "speed": {default_speed},\1\2', 
            roads_body
        )

        with open(output_file, 'w') as f:
            f.write(header + updated_body)
        
        print(f"Success! The updated file has been saved as: {output_file}")

    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Please ensure it is in the same folder.")

if __name__ == "__main__":
    update_network_file()