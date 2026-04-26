# Day 4 — SQL Question Answering System

## Architecture Overview
The SQL-QA Engine allows users to interrogate raw database formats (SQLite databases, CSVs, and extracted PDF tabular layouts) natively using natural language. 

The pipeline structure flows strictly from:
**NL Question → Prompt Injection → SQL Construction → Security Token Validation → DB Query → Summary Extradition.**

## Core Components
### 1. The Schema Loader (`/utils/schema_loader.py`)
Intercepts the uploaded `.db` or `.csv` layout dynamically and parses out table names alongside respective nested column strings so the LLM comprehends the spatial parameters it can execute operations inside.

### 2. The SQL Generator (`/generator/sql_generator.py`)
Utilizes the `llama-3.1-8b-instant` Groq API. It takes our Schema context + User prompt to write an exact syntactical SQL statement. 
* Contains a **Security Validator Loop** that systematically parses generated tokens to block malicious injection keywords (`DROP`, `DELETE`) or hallucinatory unmapped schema column references prior to executing. 

### 3. The Execution Pipeline (`/pipelines/sql_pipeline.py`)
Interfaces directly with SQLite dynamically loading the tabular dataset. It takes the secure SQL string and executes `.fetchall()`. The raw returned relational data is then passed back to an LLM instruction string instructing it to summarize the numerical/categorical output naturally.

## PDF Parsing Addition 
We've extended the basic SQL logic to dynamically extract nested grids inside raw `.pdf` documents using `pdfplumber`, mapping them silently via `pandas` into dynamic database tables (e.g. `pdf_table_p1_idx1`) allowing true unstructured-to-structured analytical querying!
