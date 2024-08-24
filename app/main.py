import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)


pages = {
    "🏠 Home": [
        st.Page("pages/home.py", title="Welcome & Overview"),
    ],
    "Exploratory Data Analysis 🔍": [
        st.Page("pages/univariate.py", title="Univariate Analysis"),
        st.Page("pages/multivariate.py", title="Multivariate Analysis"),
    ],
    "Comparator Analysis 📊": [
        st.Page("pages/comparator.py", title="Country Comparison & Insights"),
    ]
}


pg = st.navigation(pages)
pg.run()

