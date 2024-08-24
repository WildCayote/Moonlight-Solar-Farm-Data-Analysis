import streamlit as st
import pandas as pd

# check if the dataset is loaded if not return to home
try:
    uploaded_files = st.session_state["uploaded_files"]
except: 
    st.switch_page("pages/home.py")

st.write("# Exploring Feature Relationships")

st.markdown(
    """
    On this page, you can explore the relationships between multiple features across the solar farm datasets for Benin, Sierra Leone, and Togo. 
    Analyze how different variables interact with each other to uncover complex patterns and correlations that may impact solar energy potential.
    """
    )
