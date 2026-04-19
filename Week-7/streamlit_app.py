import streamlit as st
import os


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="RAG System", layout="wide")

st.title("🧠 Multi-Modal RAG System")

# ---------------- LAZY LOAD APP ----------------
@st.cache_resource
def load_app():
    from src.deployment.app import App   # ✅ IMPORT INSIDE FUNCTION
    return App()

# Load only when needed
app = None

# Sidebar
mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Text RAG", "Image Search", "SQL Query"]
)

# ================= TEXT =================
if mode == "Text RAG":
    st.header("💬 Ask Questions")

    query = st.text_input("Enter your question")

    if st.button("Ask"):
        if query:
            app = load_app()  # ✅ LOAD ONLY HERE

            result = app.ask(query)

            if result["type"] == "text":
                st.subheader("Text Answer")
                st.write(result["data"])

            elif result["type"] == "image":
                st.subheader("Image Results")

                for r in result["data"]:
                    if r.get("image"):
                        st.image(r["image"], width=300)

                    st.write(f"Caption: {r.get('caption', '')}")
                    st.write(f"Score: {r.get('score', 0):.4f}")
                    st.write("---")

            elif result["type"] == "sql":
                st.subheader("SQL Result")
                st.write(result["data"])

            st.subheader("Confidence")
            st.write(result["confidence"])

            st.subheader("Hallucination")
            st.write(result["hallucination"])

            feedback = st.radio("Feedback", ["Good", "Bad"])
            if st.button("Submit Feedback"):
                app.feedback(query, feedback)
                st.success("Feedback recorded!")

# ================= IMAGE =================
elif mode == "Image Search":
    st.header("🖼️ Image Search")

    query = st.text_input("Describe the image (Text-to-Image)")
    uploaded_image = st.file_uploader("Or upload an image (Image-to-Image / Image-to-Text)", type=["png", "jpg", "jpeg"])

    if st.button("Search"):
        if query or uploaded_image:
            app = load_app()

            if uploaded_image:
                from PIL import Image
                query_image = Image.open(uploaded_image).convert("RGB")
                result = app.ask_image(query=None, image_input=query_image)
            else:
                result = app.ask_image(query=query)

            st.write(result["data"])  # ✅ NOW result exists

            for r in result["data"]:
                if not isinstance(r, dict):
                    continue

                img = r.get("image")

                if img:
                    import os
                    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img)

                    if os.path.exists(img_path):
                        st.image(img_path, width=300)

                st.write(f"Caption: {r.get('caption', '')}")
                st.write(f"OCR: {r.get('ocr', '')}")
                st.write(f"Score: {r.get('score', 0):.4f}")
                st.write("---")
# ================= SQL =================
elif mode == "SQL Query":
    st.header("🗄️ Ask Database")

    uploaded_db = st.file_uploader("Upload dataset (.csv, .db, .pdf)", type=["csv", "db", "sqlite", "pdf"])
    query = st.text_input("Enter SQL question")

    if st.button("Run Query"):
        if query and uploaded_db:
            app = load_app()

            import tempfile
            import sqlite3
            import pandas as pd
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_db.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_db.getbuffer())
                tmp_path = tmp.name

            db_path = tmp_path
            if uploaded_db.name.endswith(".csv"):
                db_path = tmp_path + ".db"
                df = pd.read_csv(tmp_path)
                conn = sqlite3.connect(db_path)
                table_name = uploaded_db.name.replace(".csv", "").replace("-", "_")
                df.columns = [c.replace(" ", "_") for c in df.columns]
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                conn.close()
            elif uploaded_db.name.endswith(".pdf"):
                import pdfplumber
                db_path = tmp_path + ".db"
                conn = sqlite3.connect(db_path)
                
                with pdfplumber.open(tmp_path) as pdf:
                    table_count = 0
                    for page_i, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        for table_i, table in enumerate(tables):
                            if not table or len(table) < 2:
                                continue
                            
                            # Clean empty rows
                            cleaned_table = []
                            for row in table:
                                if any(cell and str(cell).strip() for cell in row):
                                    cleaned_table.append([(str(cell).strip().replace("\n", " ") if cell else "") for cell in row])
                            
                            if len(cleaned_table) < 2:
                                continue
                                
                            headers = cleaned_table[0]
                            # Make valid sql headers
                            clean_headers = []
                            for c_i, h in enumerate(headers):
                                h_clean = str(h).strip().replace(" ", "_").replace("\n", "_").replace("-", "_")
                                if not h_clean:
                                    h_clean = f"col_{c_i}"
                                clean_headers.append(h_clean)
                                
                            df = pd.DataFrame(cleaned_table[1:], columns=clean_headers)
                            table_name = f"pdf_table_p{page_i+1}_idx{table_i+1}"
                            df.to_sql(table_name, conn, if_exists="replace", index=False)
                            table_count += 1
                            
                conn.close()
                if table_count == 0:
                    st.warning("No tabular data could be extracted from this PDF.")

            from src.utils.schema_loader import load_schema
            from src.pipelines.sql_pipeline import SQLPipeline
            schema = load_schema(db_path)
            app.sql_pipeline = SQLPipeline(
                db_path=db_path,
                generator=app.sql_generator,
                schema=schema
            )

            result = app.ask_sql(query)
            
            st.subheader("Generated SQL:")
            st.code(result.get("sql", "N/A"), language="sql")
            
            st.subheader("Raw Results:")
            st.write(result.get("raw", "N/A"))
            
            st.subheader("Natural Response:")
            st.write(result.get("data", "N/A"))
            
        elif not uploaded_db:
            st.warning("Please upload a database or CSV file first.")