import logging
import warnings
import os

# Absolute Silence: Must happen before other imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("autogen").setLevel(logging.ERROR)
logging.getLogger("streamlit").setLevel(logging.ERROR)

import streamlit as st
import sys
from dotenv import load_dotenv
from nexus_ai.orchestrator import NexusOrchestrator
from nexus_ai.ui import apply_custom_styles, render_header
from nexus_ai.config import REPORTS_DIR

# Page Configuration
st.set_page_config(
    page_title="Nexus AI Workspace",
    page_icon="[N]",
    layout="wide",
)

apply_custom_styles()
load_dotenv()

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "running" not in st.session_state:
    st.session_state.running = False
if "current_report" not in st.session_state:
    st.session_state.current_report = None

def ui_callback(agent_name, output):
    """Callback function to update the UI from the orchestrator."""
    st.session_state.messages.append({"role": agent_name, "content": output})

# Sidebar Configuration
with st.sidebar:
    st.title("Nexus History")
    reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".md")]
    reports.sort(reverse=True)
    
    selected_report = st.selectbox("Past Reports", ["None"] + reports)
    if selected_report != "None":
        with open(os.path.join(REPORTS_DIR, selected_report), "r") as f:
            st.session_state.current_report = f.read()

    st.divider()
    st.info("Nexus AI uses AutoGen to orchestrate specialist agents in a sequential pipeline.")

# Main Application UI
render_header()

# Goal Input Section
with st.container():
    goal = st.text_area("What is your goal?", placeholder="e.g., Plan a sustainable tech startup in the vertical farming industry...", height=100)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        start_btn = st.button("RUN NEXUS PIPELINE", use_container_width=True, type="primary")

if start_btn and goal:
    st.session_state.running = True
    st.session_state.messages = []
    st.session_state.current_report = None
    
    # Progress Management
    status_placeholder = st.empty()
    
    with status_placeholder.status("Initializing agents and memory layer...", expanded=True) as status:
        orchestrator = NexusOrchestrator()
        
        # Callback for UI progress updates
        def live_callback(name, content):
            status.update(label=f"Processing: {name} specialist is active...", state="running")

        report_path, session_id = orchestrator.run(goal, callback=live_callback)
        
        with open(report_path, "r") as f:
            st.session_state.current_report = f.read()
        
        status.update(label="Pipeline Complete", state="complete", expanded=False)
    
    st.session_state.running = False

# Final Deliverable Presentation
if st.session_state.current_report:
    st.divider()
    st.markdown('<div class="main-header" style="font-size: 1.5rem;">Final Deliverable</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown(st.session_state.current_report)
        st.download_button("Download Report (.md)", st.session_state.current_report, file_name="nexus_report.md")
