import sqlite3


class SQLPipeline:
    def __init__(self, db_path, generator, schema):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.generator = generator
        self.schema = schema

    
    def validate_sql(self, sql):
        sql_lower = sql.lower()

        blocked = ["drop", "delete", "update", "insert"]

        for word in blocked:
            if word in sql_lower:
                raise ValueError("Unsafe SQL detected")

        return True

    
    def execute(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            return f"SQL Error: {str(e)}"

    
    def summarize(self, question, results):
        if not results:
            return "No results found."

        try:
            from groq import Groq
            import os
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            prompt = f"Given the user question '{question}' and the following dataset returned from the database query: {results[:5]}, provide a natural language response answering the question. Be concise."
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except:
            return f"Returned {len(results)} rows: {results[:5]}"

    
    def run(self, question):
        sql = self.generator.generate_sql(question, self.schema)

        print("\n🔹 Generated SQL:\n", sql)

        self.validate_sql(sql)

        results = self.execute(sql)

        summary = self.summarize(question, results)

        return {
            "sql": sql,
            "raw": results,
            "summary": summary
        }