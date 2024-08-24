import streamlit as st
import pandas as pd

# check if the dataset is loaded if not return to home
try:
    uploaded_files = st.session_state["uploaded_files"]
except: 
    st.switch_page("pages/home.py")

st.write("# Compare metrics accross the countries and draw a conclusion")

st.markdown(
    """
    This page is designed to compare the statistics of different features across the solar farm datasets for Benin, Sierra Leone, and Togo. 
    Evaluate and contrast the performance of key variables to identify similarities, differences, and trends between the countries, providing insights into their solar energy potential.
    """
    )
