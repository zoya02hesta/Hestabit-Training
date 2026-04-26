import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="My LLM Chat", page_icon="🤖", layout="centered")

# 🔥 Custom CSS (premium look)
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 My Local LLM")
st.caption("Your own Techie Friend")

# 🔹 Session memory
if "history" not in st.session_state:
    st.session_state.history = []

# 🔹 Display chat history
for chat in st.session_state.history:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(chat["user"])

    if "assistant" in chat:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(chat["assistant"])

# 🔹 Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message instantly
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    st.session_state.history.append({"user": user_input})

    payload = {
        "system_prompt": "You are a helpful and friendly AI assistant",
        "user_prompt": user_input,
        "history": st.session_state.history[:-1]
    }

    # 🔥 Assistant response with streaming effect
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(API_URL, json=payload).json()
            bot_reply = response["response"]

            for word in bot_reply.split():
                full_response += word + " "
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.02)

            message_placeholder.markdown(full_response)

        except:
            message_placeholder.markdown("⚠️ Backend not running")

    st.session_state.history[-1]["assistant"] = full_response