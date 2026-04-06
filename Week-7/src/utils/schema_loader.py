import sqlite3

class SchemaLoader:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def get_schema(self):
        cursor = self.conn.cursor()

        tables = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()

        schema = ""

        for table in tables:
            table_name = table[0]
            columns = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()

            schema += f"\nTable: {table_name}\n"
            for col in columns:
                schema += f"{col[1]} ({col[2]})\n"

        return schema