import json
from collections import defaultdict
import unicodedata

# Function to normalize and clean film titles
def normalize_title(title):
    if not title:
        return "Unknown"
    # Normalize unicode characters and remove extra spaces
    return unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii').strip()

# Load the JSON file
file_path = "consolidated_movies.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Dictionary to store consolidated movie data
consolidated_movies = defaultdict(lambda: {"Years": set(), "Details": defaultdict(list)})

# Process each record in the JSON
for record in data:
    film = normalize_title(record.get("Film"))
    year = record.get("Year", "")
    details = record.get("Details", [])

    # Validate and clean up the year
    if not year.isnumeric():
        # Add invalid year to an "Uncategorized" award
        year_added = False
        for detail in details:
            if isinstance(detail, dict) and "Nominee(s)" in detail and not detail["Nominee(s)"]:
                detail["Nominee(s)"].append(year)
                year_added = True
                break
        if not year_added:
            details.append({
                "Award": "Uncategorized",
                "Nominee(s)": [year]
            })
        year = ""  # Set year to blank if invalid

    # Add the year if present
    if year:
        consolidated_movies[film]["Years"].add(year)

    # Append details for the movie, merging duplicate awards
    for detail in details:
        award = detail.get("Award", "Unknown")
        nominees = detail.get("Nominee(s)", [])
        consolidated_movies[film]["Details"][award].extend(nominees)

# Resolve missing years and normalize data
output_data = []
for film, info in consolidated_movies.items():
    # Resolve missing years
    if "" in info["Years"]:  # If there's an entry with no year
        info["Years"].remove("")
        if info["Years"]:  # Assign the most common or any existing year
            resolved_year = next(iter(info["Years"]))
            info["Years"].add(resolved_year)

    # Convert years back to a single representative year (e.g., the earliest year)
    year = min(info["Years"]) if info["Years"] else "Unknown"

    # Merge duplicate awards by removing duplicate nominees
    details = []
    for award, nominees in info["Details"].items():
        unique_nominees = list(set(nominees))  # Remove duplicate nominees
        details.append({
            "Award": award,
            "Nominee(s)": unique_nominees
        })

    output_data.append({
        "Year": year,
        "Film": film,
        "Details": details
    })

# Save the consolidated data back to a JSON file
output_file_path = "Final_Data.json"
with open(output_file_path, 'w') as file:
    json.dump(output_data, file, indent=4)

print(f"Fixed and consolidated data saved to {output_file_path}")
