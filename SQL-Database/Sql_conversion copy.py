import sqlite3
import json

# Step 1: Load JSON and Insert into Database
def load_and_insert_data(json_file, db_file):
    # Load the JSON data from file
    with open(json_file, "r") as file:
        data = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT,
            film TEXT UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Awards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            award TEXT,
            nominees TEXT,
            FOREIGN KEY (movie_id) REFERENCES Movies(id)
        )
    """)

    # Insert data into the database
    for movie in data:
        year = movie.get("Year", "")
        film = movie.get("Film", "")

        # Insert or ignore if movie already exists
        cursor.execute("INSERT OR IGNORE INTO Movies (year, film) VALUES (?, ?)", (year, film))
        cursor.execute("SELECT id FROM Movies WHERE film = ?", (film,))
        movie_id = cursor.fetchone()[0]

        # Insert awards details
        for detail in movie.get("Details", []):
            award = detail.get("Award", "")
            nominees_list = detail.get("Nominee(s)", [])
            # Ensure all elements are strings and filter out None values
            nominees = ", ".join([nom for nom in nominees_list if nom is not None])

            # Insert award details ensuring uniqueness for each movie-award combination
            cursor.execute("""
                INSERT INTO Awards (movie_id, award, nominees) 
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM Awards WHERE movie_id = ? AND award = ? AND nominees = ?
                )
            """, (movie_id, award, nominees, movie_id, award, nominees))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Step 2: Query and Format Data
def query_and_format_data(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch movies and their associated awards
    cursor.execute("""
        SELECT m.year, m.film, a.award, a.nominees
        FROM Movies m
        LEFT JOIN Awards a ON m.id = a.movie_id
        ORDER BY m.year, m.film
    """)

    # Data structure to hold the formatted results
    results = {}

    # Organize data into the desired format
    for row in cursor.fetchall():
        year, film, award, nominees = row
        key = (year, film)
        if key not in results:
            results[key] = []
        if award and nominees:
            results[key].append((award, nominees))

    # Close the database connection
    conn.close()

    # Print the results in the specified format
    for key, awards in results.items():
        year, film = key
        awards_str = ', '.join(f"({a}, {n})" for a, n in awards)
        print(f"{year}, {film} {{{awards_str}}}")

# Main Execution
if __name__ == "__main__":
    json_file = "Final_Data.json"  # Path to your JSON file
    db_file = "movies_awards.db"  # Path to your SQLite database

    # Load and insert data into the database
    load_and_insert_data(json_file, db_file)

    # Query and format the data
    query_and_format_data(db_file)
