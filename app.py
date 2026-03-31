import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
df = pd.read_csv('canadian_immigration_data.csv')

# App title
st.header('Canada Immigration Dashboard')

st.write(
    'This web app explores immigration to Canada using an interactive dataset '
    'with country-level immigration records from 1980 to 2013.'
)

st.write(
    'I chose this topic because immigration is both personally meaningful to me '
    'and professionally connected to my background.'
)

# Histogram button
hist_button = st.button('Build histogram')

if hist_button:
    st.write('Distribution of total immigration by country')
    fig_hist = px.histogram(
        df,
        x='Total',
        title='Distribution of Total Immigration to Canada by Country'
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Scatter plot button
    scatter_button = st.button('Build scatter plot')

    if scatter_button:
        st.write('Comparing immigration values between 1980 and 2013')
        fig_scatter = px.scatter(
            df,
            x='1980',
            y='2013',
            hover_name='Country',
            color='Continent',
            title='Immigration to Canada: 1980 vs 2013'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
