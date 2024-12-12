import sqlite3
import csv

def connect_to_db(db_path):
    """Connect to the SQLite database."""
    return sqlite3.connect(db_path)

def get_schema(conn):
    """Print the schema of the database."""
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Database Schema:")
    for table in tables:
        print(f"Table: {table[0]}")
        cur.execute(f"PRAGMA table_info({table[0]})")
        columns = cur.fetchall()
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
        print()

def filter_by_year(conn, year, output_csv=False):
    """Filter movies by year."""
    cur = conn.cursor()
    cur.execute("""
        SELECT m.year, m.film, GROUP_CONCAT(DISTINCT a.award || ' (' || a.nominees || ')') AS awards_and_nominees
        FROM Movies m
        LEFT JOIN Awards a ON m.id = a.movie_id
        WHERE m.year = ?
        GROUP BY m.year, m.film
        ORDER BY m.film;
    """, (year,))
    movies = cur.fetchall()

    print(f"Movies from the year {year}:")
    for movie in movies:
        print(movie)

    if output_csv:
        with open(f"movies_{year}.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Year", "Film", "Awards and Nominees"])
            writer.writerows(movies)
        print(f"Data exported to movies_{year}.csv")
    print()

def filter_by_film(conn, film, output_csv=False):
    """Filter movies by film title."""
    cur = conn.cursor()
    cur.execute("""
        SELECT m.year, m.film, GROUP_CONCAT(DISTINCT a.award || ' (' || a.nominees || ')') AS awards_and_nominees
        FROM Movies m
        LEFT JOIN Awards a ON m.id = a.movie_id
        WHERE m.film LIKE ?
        GROUP BY m.year, m.film
        ORDER BY m.film;
    """, (f'%{film}%',))
    movies = cur.fetchall()

    print(f"Movies with '{film}' in title:")
    for movie in movies:
        print(movie)

    if output_csv:
        with open(f"movies_{film}.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Year", "Film", "Awards and Nominees"])
            writer.writerows(movies)
        print(f"Data exported to movies_{film}.csv")
    print()

if __name__ == "__main__":
    db_path = 'movies_awards.db'  # Update with actual path
    conn = connect_to_db(db_path)

    # Get database schema
    get_schema(conn)

    # Filter movies by year and export to CSV
    filter_by_year(conn, '2022', output_csv=True)

    # Filter movies by film title (e.g., Avatar) and export to CSV
    filter_by_film(conn, 'Avatar', output_csv=True)

    # Close the database connection
    conn.close()
