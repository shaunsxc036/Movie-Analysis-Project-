import pandas as pd
import sqlite3

# 1. Load the full dataset
df = pd.read_csv('tmdb_5000_movies.csv')

# 2. Clean the data (remove movies with no description)
df['overview'] = df['overview'].fillna("No description available.")

# 3. Connect and Insert
conn = sqlite3.connect('movies_platform.db')
cursor = conn.cursor()

# Clear existing movies to avoid duplicates if you want a fresh start
cursor.execute("DELETE FROM Movies")

print(f"Starting migration of {len(df)} movies...")

for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO Movies (title, description, poster_url) VALUES (?, ?, ?)",
        (row['title'], row['overview'], "https://via.placeholder.com/500x750?text=No+Poster")
    )

conn.commit()
conn.close()
print("Migration Complete! Your pantry is now fully stocked.")