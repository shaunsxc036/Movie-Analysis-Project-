import sqlite3

connection = sqlite3.connect('movies_platform.db')
cursor = connection.cursor()

# Table 1: Movies (The catalog)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    poster_url TEXT,
    description TEXT
)
''')

# Table 2: Reviews (What users say)
# 'movie_id' links this review to a specific movie in the first table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 10),
    comment TEXT,
    FOREIGN KEY (movie_id) REFERENCES Movies (id)
)
''')

connection.commit()
connection.close()
print("Movie database and tables created!")