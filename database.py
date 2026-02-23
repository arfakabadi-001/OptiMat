import sqlite3
from models import Material

DB_NAME = "optimat.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        material_id INTEGER PRIMARY KEY,
        name TEXT,
        strength REAL,
        density REAL,
        cost REAL,
        max_temp REAL,
        corrosion INTEGER,
        sustainability INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_materials():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    materials = [
        (1, "Aluminum", 310, 2700, 5, 200, 7, 8),
        (2, "Steel", 550, 7850, 10, 500, 9, 5),
        (3, "Titanium", 900, 4500, 30, 600, 10, 9),
        (4, "Copper", 220, 8960, 15, 400, 6, 7)
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO materials
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, materials)

    conn.commit()
    conn.close()


def fetch_materials():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM materials")
    rows = cursor.fetchall()

    conn.close()

    return [Material(*row) for row in rows]
