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

    query = st.text_input("Describe the image")

    if st.button("Search"):
        if query:
            app = load_app()

            result = app.ask_image(query)

            st.write(result["data"])  # ✅ NOW result exists

            for r in result["data"]:
                if not isinstance(r, dict):
                    continue

                img = r.get("image")

                if img:
                    import os
                    img_path = os.path.join(os.path.dirname(__file__), img)

                    if os.path.exists(img_path):
                        st.image(img_path, width=300)

                st.write(f"Caption: {r.get('caption', '')}")
                st.write(f"Score: {r.get('score', 0)}")
                st.write("---")
# ================= SQL =================
elif mode == "SQL Query":
    st.header("🗄️ Ask Database")

    query = st.text_input("Enter SQL question")

    if st.button("Run Query"):
        app = load_app()  # ✅ LOAD ONLY WHEN USED

        result = app.ask_sql(query)
        st.write(result)