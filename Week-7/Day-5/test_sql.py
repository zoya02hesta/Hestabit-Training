from src.utils.schema_loader import SchemaLoader
from src.generator.sql_generator import SQLGenerator
from src.pipelines.sql_pipeline import SQLPipeline

DB_PATH = "sample.db"

# Load schema
loader = SchemaLoader(DB_PATH)
schema = loader.get_schema()

# Init generator
generator = SQLGenerator()

# Pipeline
pipeline = SQLPipeline(DB_PATH, generator, schema)

# Query
question = "Show all users"

answer = pipeline.run(question)

print("\n🔹 Final Answer:\n", answer)