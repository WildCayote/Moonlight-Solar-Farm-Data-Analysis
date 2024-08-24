import pandas as pd
import streamlit as st
from typing import List

def upload_csv(uploaded_file: any):
    '''
    A function that will upload a csv and return a pandas DataFrame provided the path of the csv file.
    '''
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error(f"The file {uploaded_file.name} contains no data!")
        else:
            return df
    except Exception as e:
        st.error(f"Error reading {uploaded_file.name}: {e}")