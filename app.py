
import streamlit as st
from src.main_page import render_dashboard

st.set_page_config(page_title="BSG Performance Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 4rem !important; }
    header { margin-bottom: 0 !important; }
    .top-bar {
        background-color: #1db954;
        color: white;
        padding: 0.9rem 1.2rem 0.9rem 1.2rem;
        font-size: 2.1rem;
        font-weight: bold;
        border-radius: 10px 10px 10px 10px;
        margin-bottom: 1.5rem;
        margin-top: 2 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    </style>
    <div class="top-bar">BSG Performance Dashboard</div>
    """,
    unsafe_allow_html=True
)

render_dashboard()
