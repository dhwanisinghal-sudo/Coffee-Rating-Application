from flask import Flask, render_template, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("coffee_votes.db")

COFFEES = [
    ("Ethiopian Yirgacheffe", "Bright, floral notes with a smooth citrus finish.", "☕"),
    ("Sumatra Mandheling", "Rich, earthy flavour with a deep and mellow body.", "🫘"),
    ("Cold Brew Nitro", "Silky, chilled coffee with a naturally sweet finish.", "🧋"),
    ("Vanilla Latte", "Espresso blended with steamed milk and vanilla.", "🥛"),
    ("Mexican Chiapas", "Balanced cocoa notes with a gentle nutty aroma.", "☕"),
    ("Classic Cold Brew", "Slow-steeped coffee served cool and refreshing.", "🧊"),
    ("Pav Bhaji Mocha", "A playful café special with a bold espresso base.", "🍫")
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS coffees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                emoji TEXT NOT NULL,
                votes INTEGER NOT NULL DEFAULT 0
            )
        """)
        for name, description, emoji in COFFEES:
            conn.execute(
                "INSERT OR IGNORE INTO coffees (name, description, emoji) VALUES (?, ?, ?)",
                (name, description, emoji)
            )

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/coffees")
def get_coffees():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, name, description, emoji, votes FROM coffees ORDER BY id"
        ).fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/api/coffees/<int:coffee_id>/vote")
def vote_for_coffee(coffee_id):
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE coffees SET votes = votes + 1 WHERE id = ?",
            (coffee_id,)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Coffee item not found."}), 404
        row = conn.execute(
            "SELECT id, name, votes FROM coffees WHERE id = ?",
            (coffee_id,)
        ).fetchone()
    return jsonify({
        "message": "Your vote has been recorded.",
        "coffee": dict(row)
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
