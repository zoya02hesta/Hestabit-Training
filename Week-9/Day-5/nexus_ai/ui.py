import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stChatMessage {
            background-color: #1e222d;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border: 1px solid #2e3648;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #00d4ff;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #8892b0;
            text-align: center;
            margin-bottom: 2rem;
        }
        .agent-status {
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 5px;
        }
        .status-running {
            background-color: #ffd70033;
            color: #ffd700;
            border: 1px solid #ffd70066;
        }
        .status-done {
            background-color: #00ff0022;
            color: #00ff00;
            border: 1px solid #00ff0044;
        }
        .report-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        div[data-testid="stStatus"] label, .stExpander label, .stExpander p {
            color: #00d4ff !important;
        }
        div.stButton > button:first-child, div.stDownloadButton > button:first-child {
            background: linear-gradient(45deg, #00d4ff, #0055ff);
            color: white !important;
            border: none;
            padding: 0.6rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }
        div.stButton > button:hover, div.stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
            background: linear-gradient(45deg, #00e5ff, #0066ff);
            color: white !important;
        }
        .stButton button p, .stDownloadButton button p {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown('<div class="main-header">NEXUS AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Premium Multi-Agent Workspace</div>', unsafe_allow_html=True)
