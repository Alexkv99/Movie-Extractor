import json
from collections import defaultdict

# Load the JSON file
file_path = "merged_data.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Dictionary to store consolidated movie data
consolidated_movies = defaultdict(lambda: {"Years": set(), "Details": []})

# Process each record in the JSON
for record in data:
    film = record.get("Film")
    year = record.get("Year")
    details = record.get("Details", {})

    # Add the year if present, otherwise it will be set later
    if year:
        consolidated_movies[film]["Years"].add(year)

    # Append details for the movie
    consolidated_movies[film]["Details"].append(details)

# Resolve missing years
for film, info in consolidated_movies.items():
    if "" in info["Years"]:  # If there's an entry with no year
        info["Years"].remove("")
        if info["Years"]:  # Assign the most common or any existing year
            resolved_year = next(iter(info["Years"]))
            info["Years"].add(resolved_year)

# Convert years back to a single representative year (e.g., the earliest year)
for film, info in consolidated_movies.items():
    if info["Years"]:  # Ensure the set is not empty before calling min()
        info["Years"] = min(info["Years"])
    else:
        info["Years"] = "Unknown"  # Assign a default value if no year is available

# Convert the defaultdict to a regular dictionary for JSON output
output_data = [
    {
        "Year": info["Years"],
        "Film": film,
        "Details": info["Details"]
    }
    for film, info in consolidated_movies.items()
]

# Save the consolidated data back to a JSON file
output_file_path = "consolidated_movies.json"
with open(output_file_path, 'w') as file:
    json.dump(output_data, file, indent=4)

print(f"Consolidated data saved to {output_file_path}")
