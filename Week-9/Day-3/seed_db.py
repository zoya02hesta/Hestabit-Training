"""
seed_db.py — Creates and seeds the SQLite database for Day 3 exercises.
Run once before using the DB Agent.
"""
import sqlite3, csv, os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "sales.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "sales.csv")

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS sales")
    cur.execute("""
        CREATE TABLE sales (
            order_id   INTEGER PRIMARY KEY,
            product    TEXT,
            category   TEXT,
            quantity   INTEGER,
            unit_price REAL,
            total_sales REAL,
            region     TEXT,
            date       TEXT,
            salesperson TEXT
        )
    """)
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        rows = [(
            int(r["order_id"]), r["product"], r["category"],
            int(r["quantity"]), float(r["unit_price"]), float(r["total_sales"]),
            r["region"], r["date"], r["salesperson"]
        ) for r in reader]
    cur.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    conn.close()
    print(f"Database seeded at {DB_PATH} with {len(rows)} rows.")

if __name__ == "__main__":
    seed()
