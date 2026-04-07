from groq import Groq
import os
import re


class SQLGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_sql(self, query, schema):
        prompt = f"""
You are a strict SQL generator.

DATABASE SCHEMA:
{schema}

RULES:
- Use ONLY table: users
- Allowed columns: id, name, age, income
- NEVER invent columns
- ONLY output SQL
- NO explanation
- MUST end with semicolon

EXAMPLES:
Q: count users
A: SELECT COUNT(*) FROM users;

Q: list all users
A: SELECT * FROM users;

Q: average income
A: SELECT AVG(income) FROM users;

Q: users older than 30
A: SELECT * FROM users WHERE age > 30;

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
            sql = "SELECT * FROM users;"

        # 🔒 SAFETY FILTER
        if any(word in sql.lower() for word in ["drop", "delete", "update", "insert"]):
            return "SELECT * FROM users;"

        # 🔒 STRICT COLUMN CHECK
        allowed_columns = ["id", "name", "age", "income"]

        tokens = re.findall(r"\b[a-zA-Z_]+\b", sql.lower())

        allowed_keywords = [
            "select", "from", "where", "count", "avg", "min", "max", "sum",
            "and", "or", ">", "<", "=", "*"
        ]

        for token in tokens:
            if token not in allowed_columns and token not in allowed_keywords:
                if token != "users":
                    print(f"⚠️ Invalid token detected: {token}")
                    return "SELECT * FROM users;"

        return sql