import sqlite3
import json

# Load the JSON file
file_path = "Final_Data.json"
with open(file_path, "r") as file:
    data = json.load(file)

# Connect to SQLite database (or create it if it doesn't exist)
db_path = "movies_awards.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year TEXT,
        film TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Awards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        award TEXT,
        nominees TEXT,
        FOREIGN KEY (movie_id) REFERENCES Movies (id)
    )
""")

# Insert data into tables
for movie in data:
    year = movie.get("Year", "")
    film = movie.get("Film", "")
    
    # Insert movie into Movies table
    cursor.execute("INSERT INTO Movies (year, film) VALUES (?, ?)", (year, film))
    movie_id = cursor.lastrowid  # Get the inserted movie's ID
    
    # Insert awards and nominees into Awards table
    for detail in movie.get("Details", []):
        award = detail.get("Award", "")
        nominees_list = detail.get("Nominee(s)", [])
        # Filter out None values from the nominees list and join them into a string
        nominees = ", ".join(filter(None, nominees_list))
        cursor.execute(
            "INSERT INTO Awards (movie_id, award, nominees) VALUES (?, ?, ?)",
            (movie_id, award, nominees)
        )

# Commit and close the connection
conn.commit()

# Query and display data from the database
print("Movies and Awards in the Database:")
cursor.execute("""
    SELECT m.year, m.film, a.award, a.nominees
    FROM Movies m
    JOIN Awards a ON m.id = a.movie_id
    ORDER BY m.year, m.film
""")
rows = cursor.fetchall()

for row in rows:
    print(f"Year: {row[0]}, Film: {row[1]}, Award: {row[2]}, Nominees: {row[3]}")

# Close the database connection
conn.close()

print(f"Data has been saved to the SQLite database: {db_path}")
