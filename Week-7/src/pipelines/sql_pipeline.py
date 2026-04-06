import sqlite3

class SQLPipeline:
    def __init__(self, db_path, generator, schema):
        self.conn = sqlite3.connect(db_path)
        self.generator = generator
        self.schema = schema

    def validate_sql(self, sql):
        sql = sql.lower()

        # Block dangerous queries
        blocked = ["drop", "delete", "update", "insert"]

        for word in blocked:
            if word in sql:
                raise ValueError("Unsafe SQL detected")

        return True

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def summarize(self, results):
        if not results:
            return "No results found."

        return f"Returned {len(results)} rows: {results[:5]}"

    def run(self, question):
        sql = self.generator.generate_sql(question, self.schema)

        print("\n🔹 Generated SQL:\n", sql)

        self.validate_sql(sql)

        results = self.execute(sql)

        summary = self.summarize(results)

        return summary