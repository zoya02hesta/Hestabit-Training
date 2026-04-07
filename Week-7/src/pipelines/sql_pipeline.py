import sqlite3


class SQLPipeline:
    def __init__(self, db_path, generator, schema):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.generator = generator
        self.schema = schema

    # 🔒 Validate SQL
    def validate_sql(self, sql):
        sql_lower = sql.lower()

        blocked = ["drop", "delete", "update", "insert"]

        for word in blocked:
            if word in sql_lower:
                raise ValueError("Unsafe SQL detected")

        return True

    # 🗄 Execute SQL
    # def execute(self, sql):
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql)
    #     return cursor.fetchall()

    def execute(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            return f"SQL Error: {str(e)}"

    # 📊 Summarize results
    def summarize(self, results):
        if not results:
            return "No results found."

        return f"Returned {len(results)} rows: {results[:5]}"

    # 🚀 Main pipeline
    def run(self, question):
        sql = self.generator.generate_sql(question, self.schema)

        print("\n🔹 Generated SQL:\n", sql)

        self.validate_sql(sql)

        results = self.execute(sql)

        summary = self.summarize(results)

        return summary