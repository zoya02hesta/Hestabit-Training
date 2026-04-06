from transformers import pipeline
import re


class SQLGenerator:
    def __init__(self):
        # Initialize lightweight LLM (demo purpose)
        self.llm = pipeline("text-generation", model="gpt2")

    def generate_sql(self, question, schema):
        prompt = f"""
You are a SQL expert.

Schema:
{schema}

Rules:
- Return ONLY a valid SQL query
- No explanation
- No repetition
- Must include FROM clause
- End query with ;

Question: {question}

SQL:
"""

        # Generate response
        result = self.llm(prompt, max_new_tokens=100, do_sample=False)
        raw_output = result[0]["generated_text"]

        # 🔥 Extract only first valid SQL query
        match = re.search(r"(SELECT .*?;)", raw_output, re.IGNORECASE | re.DOTALL)

        if match:
            sql = match.group(1)
        else:
            # fallback if model fails
            sql = "SELECT * FROM users;"

        return sql.strip()