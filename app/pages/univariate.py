import streamlit as st
import pandas as pd
import seaborn as sns
import pandas as pd
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

st.write("# Exploring Individual Features")

st.markdown(
    """
    This page allows you to explore individual features of the solar farm datasets for Benin, Sierra Leone, and Togo. 
    Visualize and analyze the distribution, central tendency, and variability of key variables to gain insights into the underlying data patterns.
    """
    )

tab1, tab2, tab3 = st.tabs(["Summary Stats", "Box Plot(Outlier Detection)" , "Timeseries Analysis"])

with tab1:
    # radio button for selecting the dataset
    chosen_dataset = st.radio(
        "Choose the dataset you want to obtain the summary statistics for", 
        ["Benin" , "Sierraleone" , "Togo"],
        horizontal=True , key='1')
    
    # obtain the dataset from the context
    if chosen_dataset == "Benin":
        df = st.session_state["benin_df"]
    elif chosen_dataset == "Sierraleone":
        df = st.session_state["sierraleone_df"]
    elif chosen_dataset == "Togo":
        df = st.session_state["togo_df"]
    
    
    ## write the type of data for every column
    st.markdown(
        """
        *  **The columns available in the dataset and their types:**
        """
        )
    # Assuming df is your DataFrame
    data_types = df.dtypes

    # Convert Series to a DataFrame with a single row
    data_types_df = pd.DataFrame([data_types.values], columns=data_types.index)

    # Set the index name for the row
    data_types_df.index = ['Data Types']

    # Use st.write to display the DataFrame horizontally
    st.write(data_types_df)

    ## Calculate the summary statistics
    st.markdown(
        """
        *  **The summary statistics like mean, q1 , q2 , q3 , min , max and standard deviation for every column in the dataset:**
        """
        )
    summary = df.describe()
    st.write(summary)

with tab2:
    # radio button for selecting the dataset
    chosen_dataset = st.radio(
        "Choose the dataset you want to obtain the summary statistics for", 
        ["Benin" , "Sierraleone" , "Togo"],
        horizontal=True, key='2')
    
    # obtain the dataset from the context
    if chosen_dataset == "Benin":
        df = st.session_state["benin_df"]
        name = 'Benin'
    elif chosen_dataset == "Sierraleone":
        df = st.session_state["sierraleone_df"]
        name = 'Sierraleone'
    elif chosen_dataset == "Togo":
        df = st.session_state["togo_df"]
        name = 'Togo'

    ## Show the histogram of every column
    st.markdown(
        """
        *  Below you can see the box plot of every column, which will highlight the skewness of the features and also help determine the presence of outliers:
        """
    )

    # subplot for df box plots
    fig , axes = plt.subplots(ncols=MAX_COLUMNS , nrows=num_rows , sharex=True , figsize=(25,4 * num_rows) , squeeze=True)
    fig.suptitle(f"Box plots for numerical columns of {name}'s data")

    axes = axes.flatten()

    for idx, col_name in enumerate(QUANTITATIVE_COLS):
        # Check if col_name exists in the DataFrame
        if col_name in df.columns:
            sns.boxplot(data=df[col_name].astype(float), ax=axes[idx], orient='v')
        else:
            print(f"Column {col_name} does not exist in the DataFrame.")

    # Adjust spacing between subplots
    plt.tight_layout(pad=2)

    st.pyplot(fig=fig)

with tab3:
    # radio button for selecting the dataset
    chosen_dataset = st.radio(
        "Choose the dataset you want to obtain the summary statistics for", 
        ["Benin" , "Sierraleone" , "Togo"],
        horizontal=True, key='3')
    
    # obtain the dataset from the context
    if chosen_dataset == "Benin":
        df = st.session_state["benin_df"]
        name = 'Benin'
    elif chosen_dataset == "Sierraleone":
        df = st.session_state["sierraleone_df"]
        name = 'Sierraleone'
    elif chosen_dataset == "Togo":
        df = st.session_state["togo_df"]
        name = 'Togo'

    # decompose the timestamp into months and hours
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Hour'] = df['Timestamp'].dt.hour
    df['Month'] = df['Timestamp'].dt.month

    ## Show the histogram of every column
    st.markdown(
        """
        **Below you can see line plots of features accross time, which will highlight trends.**
        """
    )

    # plot features against time
    st.markdown(
        """
        * In this plot the feautures are plotted alond hours of the day:
        """
    )

    # subplot for df line plots
    fig , axes = plt.subplots(ncols=MAX_COLUMNS , nrows=num_rows , sharex=True , figsize=(25,3 * num_rows) , squeeze=True)
    fig.suptitle("Line plots for numerical columns of Bennin's data accross hours of the day")

    axes = axes.flatten()

    for idx, col_name in enumerate(QUANTITATIVE_COLS):
        sns.lineplot(data=df , x='Hour' , y=col_name, label=col_name , ax=axes[idx])

    # Customize the x-axis to increment by 1
    plt.xticks(ticks=range(df['Hour'].min(), df['Hour'].max() + 1, 1))

    # show legend
    plt.legend(loc='upper left', fontsize='medium', title='Legend')

    plt.tight_layout(pad=2)
    st.pyplot(fig=fig)