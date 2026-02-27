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
    (4, "Copper", 220, 8960, 15, 400, 6, 7),
    (5, "Brass", 350, 8500, 12, 350, 7, 6),
    (6, "Bronze", 400, 8800, 18, 300, 8, 5),
    (7, "Nickel", 600, 8900, 25, 500, 9, 4),
    (8, "Magnesium", 250, 1800, 7, 150, 5, 8),
    (9, "Zinc", 200, 7100, 8, 250, 6, 6),
    (10, "Chromium", 700, 7200, 28, 550, 10, 3),
    (11, "Cobalt", 650, 8900, 32, 500, 9, 4),
    (12, "Titanium Alloy", 950, 4600, 35, 650, 10, 9)
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
