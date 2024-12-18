import json

def correct_awards_data(file_path):
    # Load the data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Correct the mistakes
    for entry in data:
        film_title = entry.get('Film', '')
        if film_title:  # Ensure there's a film title to check against
            for detail in entry['Details']:
                award = detail['Award'].lower()
                nominees = detail.get('Nominee(s)', [])
                
                # Conditions to identify awards where the film name might have been placed in nominees
                if 'film' in award or 'director' in award or 'screenplay' in award:
                    # Check if the film title matches any nominee's entry and swap if needed
                    if len(nominees) == 1 and film_title in nominees:
                        # Swap the entries
                        detail['Nominee(s)'] = [film_title]
                        entry['Film'] = nominees[0]

    # Save the corrected data to a new file
    corrected_file_path = file_path.replace('.json', '_corrected.json')
    with open(corrected_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return corrected_file_path

# Path to the data file, adjust to your file's location
file_path = 'Final_Data.json'  # Replace with the actual file path

# Correct the data and get the path to the corrected file
corrected_file_path = correct_awards_data(file_path)
print(f"Corrected data saved to {corrected_file_path}")
