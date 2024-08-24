import streamlit as st
import pandas as pd

from utils.utils import upload_csv

st.write("# Welcome to Moonlight-Solar-Farm-Data-Analysis Dashboard👋")

st.markdown(
    """
    The Moonlight-Solar-Farm-Data-Analysis Dashboard is an interactive and user-friendly tool designed to provide comprehensive insights into solar farm data. 
    This dashboard leverages powerful data visualization techniques to analyze and interpret solar irradiation data, with a particular focus on identifying regions with high potential for solar energy farming.
    You can find the final reports of the analysis on the reports page, but inorder to use this dashboard you should upload the 3 csv files for each country.
"""
)

uploaded_files = st.file_uploader(
    "Choose a files to continue. Note: only 3 csv files are allowed. The order on which you upload them corresponds to the order the dashboard reads them. The order is Benin's, Sierraleone's then Togo's dataset.", accept_multiple_files=True,
    type='csv')

if len(uploaded_files) == 3:
    st.session_state["uploaded_files"] = uploaded_files
    st.session_state["benin_df"] = upload_csv(uploaded_files[0])
    st.session_state["sierraleone_df"] = upload_csv(uploaded_files[1])
    st.session_state["togo_df"] = upload_csv(uploaded_files[2])
    st.write(f"Successfuly uploaded files! Click the button below to start using the dashboard.")
    # Add a button here
    if st.button("Proceed to Analysis"):
        st.success("Loading your dashboard... Redirecting to the analysis page.")
        st.switch_page("pages/univariate.py")
else:
    try:
        files = st.session_state["uploaded_files"]
        st.write(f"{files[0].name} has already been uploaded for Benin.")
        st.write(f"{files[1].name} has already been uploaded for Sierraleone.")
        st.write(f"{files[2].name} has already been uploaded for Togo.")

        st.warning("If you want you can reupload new csv files inplace of the once you have already uploaded!")
        if st.button("Retrun to Analysis"):
            st.success("Loading your dashboard... Redirecting to the analysis page.")
            st.switch_page("pages/univariate.py")
    except:    
        st.warning('You need to upload exactly 3 datasets!')