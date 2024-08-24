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

st.write("# Compare metrics accross the countries and draw a conclusion")

st.markdown(
    """
    This page is designed to compare the statistics of different features across the solar farm datasets for Benin, Sierra Leone, and Togo. 
    Evaluate and contrast the performance of key variables to identify similarities, differences, and trends between the countries, providing insights into their solar energy potential.
    """
    )

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
"Select which time frame you want to compare over:",
('Month' , 'Hour'), key='option-2'
)

# read the data
bennin_df = st.session_state["benin_df"]
sierraleone_df = st.session_state["sierraleone_df"]
togo_df = st.session_state["togo_df"]

# breakdown the timestamp into hours of the day and also month of the year
bennin_df['Timestamp'] = pd.to_datetime(bennin_df['Timestamp'])
bennin_df['Hour'] = bennin_df['Timestamp'].dt.hour
bennin_df['Month'] = bennin_df['Timestamp'].dt.month

sierraleone_df['Timestamp'] = pd.to_datetime(sierraleone_df['Timestamp'])
sierraleone_df['Hour'] = sierraleone_df['Timestamp'].dt.hour
sierraleone_df['Month'] = sierraleone_df['Timestamp'].dt.month

togo_df['Timestamp'] = pd.to_datetime(togo_df['Timestamp'])
togo_df['Hour'] = togo_df['Timestamp'].dt.hour
togo_df['Month'] = togo_df['Timestamp'].dt.month

# take average of ModA and ModB
bennin_df[option_one + 'avg'] = bennin_df[['ModA' , 'ModB']].mean(axis=1)
sierraleone_df[option_one + 'avg'] = sierraleone_df[['ModA' , 'ModB']].mean(axis=1)
togo_df[option_one + 'avg'] = togo_df[['ModA' , 'ModB']].mean(axis=1)

# the difference in ModA between Bennin , Sierraleone and Togo
fig , ax = plt.subplots(ncols=3 , nrows=1 , sharex=True ,  figsize=(20, 6) , squeeze=True)

# Bennin vs Sierraleone
data1 = bennin_df.groupby([option_two])[option_one + 'avg'].mean().reset_index()
data2 = sierraleone_df.groupby([option_two])[option_one + 'avg'].mean().reset_index()
sns.lineplot(data=data1 , x=option_two , y=option_one + 'avg' , ax=ax[0] , label='Bennin' , color='blue')
sns.lineplot(data=data2 ,  x=option_two , y=option_one + 'avg' , ax=ax[0] , label='Sierraleone' , color='red')
ax[0].fill_between(data1[option_two], data1[option_one + 'avg'], data2[option_one + 'avg'], where=(data2[option_one + 'avg'] <= data1[option_one + 'avg']), interpolate=True, color='blue', alpha=0.3, hatch='/')
ax[0].fill_between(data2[option_two], data1[option_one + 'avg'], data2[option_one + 'avg'], where=(data2[option_one + 'avg'] > data1[option_one + 'avg']), interpolate=True, color='red', alpha=0.3, hatch='\\')


# Benning vs Togo
data1 = bennin_df.groupby([option_two])[option_one + 'avg'].mean().reset_index()
data2 = togo_df.groupby([option_two])[option_one + 'avg'].mean().reset_index()
sns.lineplot(data=data1 , x=option_two , y=option_one + 'avg' , ax=ax[1] , label='Bennin' , color='blue')
sns.lineplot(data=data2 ,  x=option_two , y=option_one + 'avg' , ax=ax[1] , label='Togo' , color='red')
ax[1].fill_between(data1[option_two], data1[option_one + 'avg'], data2[option_one + 'avg'], where=(data2[option_one + 'avg'] <= data1[option_one + 'avg']), interpolate=True, color='blue', alpha=0.3, hatch='/')
ax[1].fill_between(data2[option_two], data1[option_one + 'avg'], data2[option_one + 'avg'], where=(data2[option_one + 'avg'] > data1[option_one + 'avg']), interpolate=True, color='red', alpha=0.3, hatch='\\')

# Sierraleone vs Togo
data1 = sierraleone_df.groupby([option_two])[option_one + 'avg'].mean().reset_index()
data2 = togo_df.groupby([option_two])[option_one + 'avg'].mean().reset_index()
sns.lineplot(data=data1 , x=option_two , y=option_one + 'avg' , ax=ax[2] , label='Sierraleone' , color='blue')
sns.lineplot(data=data2 ,  x=option_two , y=option_one + 'avg' , ax=ax[2] , label='Togo' , color='red')
ax[2].fill_between(data1[option_two], data1[option_one + 'avg'], data2[option_one + 'avg'], where=(data2[option_one + 'avg'] <= data1[option_one + 'avg']), interpolate=True, color='blue', alpha=0.3, hatch='/')
ax[2].fill_between(data2[option_two], data1[option_one + 'avg'], data2[option_one + 'avg'], where=(data2[option_one + 'avg'] > data1[option_one + 'avg']), interpolate=True, color='red', alpha=0.3, hatch='\\')

# Customize the x-axis to increment by 1
plt.xticks(ticks=range(bennin_df[option_two].min(), bennin_df[option_two].max() + 1, 1))

plt.legend()
st.pyplot(fig=fig)

st.markdown(
        """
        *  Here you can quantitatively see the differences among the countries over the selected field and time-frame:
        """
)

# difference between bennin and sierraleone
ben_sier_dif = (bennin_df.groupby(option_two)[option_one + 'avg'].mean() - sierraleone_df.groupby(option_two)[option_one + 'avg'].mean()).sum()

# difference between bennin and togo
ben_tog_dif = (bennin_df.groupby(option_two)[option_one + 'avg'].mean() - togo_df.groupby(option_two)[option_one + 'avg'].mean()).sum()

# difference between togo and sierraleone
tog_sier_dif = (togo_df.groupby(option_two)[option_one + 'avg'].mean() - sierraleone_df.groupby(option_two)[option_one + 'avg'].mean()).sum()

# Displaying the results in Streamlit
st.write(f"Bennin - Sierra Leone => {ben_sier_dif}")
st.write(f"Bennin - Togo => {ben_tog_dif}")
st.write(f"Togo - Sierra Leone => {tog_sier_dif}")