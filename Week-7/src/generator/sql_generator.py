from groq import Groq
import os
import re


class SQLGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_sql(self, query, schema):
        schema_text = "\n".join([f"Table: {k}, Columns: {', '.join(v)}" for k, v in schema.items()])
        table_names = list(schema.keys())
        first_table = table_names[0] if table_names else "users"

        prompt = f"""
You are a strict SQL generator.

DATABASE SCHEMA:
{schema_text}

RULES:
- Use ONLY tables from the schema: {', '.join(table_names)}
- Allowed columns are strictly those present in the schema.
- NEVER invent columns or tables.
- ONLY output SQL
- NO explanation
- MUST end with semicolon

EXAMPLES:
Q: count all records
A: SELECT COUNT(*) FROM {first_table};

Q: list all records
A: SELECT * FROM {first_table};

Now generate SQL.

Q: {query}
A:
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        # ✅ Extract SQL
        match = re.search(r"(SELECT .*?;)", result, re.IGNORECASE | re.DOTALL)

        if match:
            sql = match.group(1).strip()
        else:
            sql = f"SELECT * FROM {first_table};"

        # 🔒 SAFETY FILTER
        if any(word in sql.lower() for word in ["drop", "delete", "update", "insert"]):
            return f"SELECT * FROM {first_table};"

        # 🔒 STRICT COLUMN CHECK
        allowed_columns = []
        for cols in schema.values():
            allowed_columns.extend([c.lower() for c in cols])
        
        allowed_tables = [t.lower() for t in schema.keys()]

        # Remove string literals to avoid flagging valid user query values like 'China'
        sql_no_literals = re.sub(r"'.*?'|\".*?\"", "", sql)
        tokens = re.findall(r"\b[a-zA-Z_]+\b", sql_no_literals.lower())

        allowed_keywords = [
            "select", "from", "where", "count", "avg", "min", "max", "sum",
            "and", "or", ">", "<", "=", "*", "like", "in", "order", "by", "limit", "group", "join", "on", "asc", "desc", "as", "is", "null", "not", "outer", "inner", "left", "right"
        ]

        for token in tokens:
            if token not in allowed_columns and token not in allowed_keywords:
                if token not in allowed_tables:
                    print(f"⚠️ Invalid token detected: {token}")
                    return f"SELECT * FROM {first_table};"

        return sql