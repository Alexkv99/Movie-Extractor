import json

# Function to load a JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to clean BAFTA data
def clean_bafta(data):
    cleaned = []
    for year, awards in data.get("BAFTA", {}).items():
        for award, details in awards.items():
            if isinstance(details, dict):
                # Process winner only
                winner = details.get("winner", {})
                if winner:
                    if award in ["Leading Actor", "Leading Actress", "Supporting Actor", "Supporting Actress"]:
                        # Swap actor name and movie title
                        cleaned.append({
                            "Year": year,
                            "Film": winner.get("persons_invested", [None])[0],  # Movie title
                            "Details": {
                                "Award": award,
                                "Nominee(s)": [winner.get("title")],  # Actor's name
                            }
                        })
                    else:
                        cleaned.append({
                            "Year": year,
                            "Film": winner.get("title"),
                            "Details": {
                                "Award": award,
                                "Nominee(s)": winner.get("persons_invested", [])
                            }
                        })
    return cleaned

# Function to clean Golden Globe data
def clean_golden_globe(data):
    return [{
        "Year": entry["Year"],
        "Film": entry["Movie"],
        "Details": entry["Details"]
    } for entry in data]

# Function to clean Oscar data
def clean_oscar(data):
    cleaned = []
    for entry in data:
        year = entry["Year"]
        film = entry["Movie"]
        for detail in entry["Details"]:
            cleaned.append({
                "Year": year,
                "Film": film,
                "Details": detail
            })
    return cleaned

# Function to clean Palme data
def clean_palme(data):
    return [{
        "Year": entry["année"],
        "Film": entry["film"],
        "Details": {
            "Award": entry["prix"],
            "Nominee(s)": [entry["récipiendaire"]]
        }
    } for entry in data if entry.get("film")]

# Deduplicate and merge entries
def deduplicate_and_merge(data):
    seen = set()
    deduplicated = []
    for entry in data:
        key = (entry["Year"], entry["Film"], entry["Details"]["Award"])
        if key not in seen:
            deduplicated.append(entry)
            seen.add(key)
    return deduplicated

# Main function to process all files
def process_files(file_paths):
    merged_data = []
    
    # Process each file with its cleaning function
    for file_path, cleaner in file_paths:
        data = load_json(file_path)
        cleaned_data = cleaner(data)
        merged_data.extend(cleaned_data)
    
    # Deduplicate merged data
    merged_data = deduplicate_and_merge(merged_data)
    return merged_data

# File paths and corresponding cleaning functions
file_paths = [
    ("bafta_data.json", clean_bafta),
    ("golden_globe_data.json", clean_golden_globe),
    ("oscar_data.json", clean_oscar),
    ("Palme.json", clean_palme)
]

# Execute and save cleaned merged data
try:
    merged_data = process_files(file_paths)
    with open("merged_data.json", "w", encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2)
    print("Merged and cleaned data written to 'merged_data.json'.")
except Exception as e:
    print(f"An error occurred: {e}")
