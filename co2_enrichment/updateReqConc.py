import json
import sys

# Ensure a concentration value is provided
if len(sys.argv) != 2:
    print("Usage: python3 update_json.py <concentration>")
    sys.exit(1)

# Get the concentration value from the command-line argument
try:
    new_concentration = int(sys.argv[1])
except ValueError:
    print("Error: Concentration must be an integer.")
    sys.exit(1)

# Path to your JSON file
json_file_path = "/home/meso3/co2_enrichment/req_conc.json"

# Load the JSON data, modify it, and save it back
try:
    with open(json_file_path, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: File '{json_file_path}' not found.")
    sys.exit(1)

# Update the concentration parameter
data["concentration"] = new_concentration

# Write the updated data back to the file
with open(json_file_path, "w") as file:
    json.dump(data, file)

print(f"Concentration updated to {new_concentration}.")
