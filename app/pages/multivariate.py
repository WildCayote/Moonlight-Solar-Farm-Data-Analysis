import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import math
from matplotlib import pyplot as plt

# check if the dataset is loaded if not return to home
try:
    uploaded_files = st.session_state["uploaded_files"]
    # max number of columns per subplot
    MAX_COLUMNS = 6
    QUANTITATIVE_COLS = ["GHI","DNI","DHI" , "ModA" ,"ModB","Tamb","RH"	,"WS" ,"WSgust"	,"WSstdev","WD","WDstdev","BP","Precipitation","TModA","TModB"]

    # calculate the number of rows
    num_rows = math.ceil(len(QUANTITATIVE_COLS) / MAX_COLUMNS)
except: 
    st.switch_page("pages/home.py")

st.write("# Exploring Feature Relationships")

st.markdown(
    """
    On this page, you can explore the relationships between multiple features across the solar farm datasets for Benin, Sierra Leone, and Togo. 
    Analyze how different variables interact with each other to uncover complex patterns and correlations that may impact solar energy potential.
    """
    )

tab1, tab2 = st.tabs(["Correlation Matrix - Heat Map" , "Scatter Plot"])

with tab1:
    # radio button for selecting the dataset
    chosen_dataset = st.radio(
        "Choose the dataset you want to obtain the summary statistics for", 
        ["Benin" , "Sierraleone" , "Togo"],
        horizontal=True , key='1')
    
    # obtain the dataset from the context
    if chosen_dataset == "Benin":
        df = st.session_state["benin_df"]
        name = 'benin_df'
    elif chosen_dataset == "Sierraleone":
        df = st.session_state["sierraleone_df"]
        name = 'sierraleone_df'
    elif chosen_dataset == "Togo":
        df = st.session_state["togo_df"]
        name = 'togo_df'


    st.markdown(
        """
        *  The plot below shows the correlation matrixs between numerical features:
        """
        )
    
    # calculate the correlation matrix
    
    correlation_matrix = df[QUANTITATIVE_COLS].corr(method='pearson')

    fig , ax = plt.subplots()
    fig.set_size_inches(20 , 10)
    cmap = sns.diverging_palette(220 , 20 , as_cmap=True)
    sns.heatmap(correlation_matrix , cmap=cmap , annot=True)
    st.pyplot(fig=fig)


    # now let us show the values that have a certain correlation provided by the user
    st.markdown(
        """
        *  Move the slider along the line to show you parameters that above/below your secified value:
        """
        )
    correlation_value = st.slider("Move the slider along the line to show you parameters that above/below your secified value:", 
                                   min_value=0.0, max_value=1.0, value=0.5,
                                   step=0.01, key='slider_1'
                                   )
    # Create a mask to ignore self-correlations (correlation of a variable with itself)
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

    # Filter correlations that are above 0.6 or below -0.6 and not on the diagonal
    filtered_corr = correlation_matrix.where(~mask & ((correlation_matrix > correlation_value) | (correlation_matrix < -1 * correlation_value)))

    # Drop NaN values to see the significant correlations
    significant_correlations = filtered_corr.stack().reset_index()

    st.write(significant_correlations)

with tab2:
    # radio button for selecting the dataset
    chosen_dataset = st.radio(
        "Choose the dataset you want to obtain the summary statistics for", 
        ["Benin" , "Sierraleone" , "Togo"],
        horizontal=True , key='2')
    
    # obtain the dataset from the context
    if chosen_dataset == "Benin":
        df = st.session_state["benin_df"]
        name = 'benin_df'
    elif chosen_dataset == "Sierraleone":
        df = st.session_state["sierraleone_df"]
        name = 'sierraleone_df'
    elif chosen_dataset == "Togo":
        df = st.session_state["togo_df"]
        name = 'togo_df'
    
    st.markdown(
        """
        *  The plot below shows the scatter plot between two numerical features:
        """
        )
    
    # option for x-axis
    option_one = st.selectbox(
    "Select feature to put on x-axis:",
    QUANTITATIVE_COLS, key='option-1'
    )

    # option for y-axis
    option_two = st.selectbox(
    "Select feature to put on y-axis:",
    QUANTITATIVE_COLS, key='option-2'
    )

    # Generate the scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=option_one, y=option_two, ax=ax)

    ax.set_title(f'Scatter Plot of {option_one} vs {option_two}')
    ax.set_xlabel(option_one)
    ax.set_ylabel(option_two)

    # Display the plot in Streamlit
    st.pyplot(fig)