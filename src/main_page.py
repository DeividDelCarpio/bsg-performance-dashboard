# main_page.py
# Orquestador visual principal para el dashboard


import streamlit as st
from src.visualization.live.section.live_section import render_live_section
from src.visualization.compare.section.compare_section import render_compare_section

def render_dashboard():
    render_live_section()
    st.write("---")
    render_compare_section()
