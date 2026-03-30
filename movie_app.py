from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def db_conn():
    return sqlite3.connect('movies_platform.db')

# UPDATED SEARCH: Handles 5,000+ movies with Filtering
@app.route('/search_movies', methods=['GET'])
def search_movies():
    query = request.args.get('q', '')
    genre = request.args.get('genre', '')
    conn = db_conn()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM Movies WHERE title LIKE ?"
    params = [f'%{query}%']
    
    if genre:
        sql += " AND description LIKE ?"
        params.append(f'%{genre}%')
    
    sql += " LIMIT 21"
    cursor.execute(sql, params)
    movies = cursor.fetchall()
    conn.close()
    return jsonify(movies)

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Reviews (movie_id, rating, comment) VALUES (?, ?, ?)",
                   (data['movie_id'], data['rating'], data['comment']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Review added!"}), 201

# ── NEW: Delete all reviews for a specific movie ──
@app.route('/delete_review/<int:movie_id>', methods=['DELETE'])
def delete_review(movie_id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reviews WHERE movie_id = ?", (movie_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Review deleted!"}), 200

# ── Clear all reviews (use once to reset stale data) ──
@app.route('/clear_all_reviews', methods=['DELETE'])
def clear_all_reviews():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reviews")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Reviews'")
    conn.commit()
    conn.close()
    return jsonify({"message": "All reviews cleared!"}), 200

@app.route('/movie_stats', methods=['GET'])
def get_movie_stats():
    conn = db_conn()
    cursor = conn.cursor()
    # Get the 5 most recently reviewed movies (by latest review ID)
    cursor.execute('''
        SELECT Movies.title, AVG(Reviews.rating), MAX(Reviews.id) as latest
        FROM Movies 
        JOIN Reviews ON Movies.id = Reviews.movie_id 
        GROUP BY Movies.id 
        ORDER BY latest DESC 
        LIMIT 5
    ''')
    data = cursor.fetchall()
    conn.close()
    return jsonify({"labels": [r[0] for r in data], "scores": [round(r[1], 1) for r in data]})

if __name__ == '__main__':
    app.run(debug=True, port=5001)