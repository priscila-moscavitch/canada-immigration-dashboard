import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Canada Immigration Dashboard",
    layout="wide"
)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("canadian_immigration_data.csv")
df.columns = df.columns.astype(str).str.strip()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("Filters")

continents = sorted(df["Continent"].dropna().unique().tolist())
selected_continents = st.sidebar.multiselect(
    "Select continent(s)",
    options=continents,
    default=continents
)

top_n = st.sidebar.slider(
    "Top countries in bar chart",
    min_value=5,
    max_value=20,
    value=10,
    step=1
)

show_data = st.sidebar.checkbox("Show dataset preview", value=False)
show_hist = st.sidebar.checkbox("Show histogram", value=True)
show_scatter = st.sidebar.checkbox("Show scatter plot", value=True)
show_bar = st.sidebar.checkbox("Show bar chart", value=True)

# -------------------------
# FILTER DATA
# -------------------------
filtered_df = df[df["Continent"].isin(selected_continents)].copy()

# -------------------------
# TITLE / INTRO
# -------------------------
st.title("Canada Immigration Dashboard")

st.write("""
This dashboard explores immigration to Canada using a country-level dataset
from 1980 to 2013.

I chose this topic because immigration is personally meaningful to me
and also connected to my background and interests.

Use the filters on the left to explore patterns by continent and compare
immigration trends across countries over time.
""")

# -------------------------
# DATASET PREVIEW
# -------------------------
if show_data:
    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head())

    # -------------------------
    # OVERVIEW METRICS
    # -------------------------
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Countries in selection", filtered_df["Country"].nunique())
    col2.metric("Continents selected", len(selected_continents))
    col3.metric("Total immigration sum",
                f"{int(filtered_df['Total'].sum()):,}")

    # -------------------------
    # HISTOGRAM
    # -------------------------
if show_hist:
    st.subheader("1. Distribution of Total Immigration by Country")
    st.write("""
This histogram shows how total immigration values are distributed across countries.
It helps identify concentration patterns and possible outliers.
""")

    fig_hist = px.histogram(
        filtered_df,
        x="Total",
        nbins=30,
        color="Continent",
        title="Distribution of Total Immigration to Canada by Country"
    )
    st.plotly_chart(fig_hist, width="stretch")

    # -------------------------
    # SCATTER PLOT
    # -------------------------
if show_scatter:
    st.subheader("2. Comparing Immigration in 1980 and 2013")
    st.write("""
This scatter plot compares immigration levels in 1980 and 2013.
It helps identify growth patterns and country trends over time.
""")

    fig_scatter = px.scatter(
        filtered_df,
        x="1980",
        y="2013",
        hover_name="Country",
        color="Continent",
        size="Total",
        title="Immigration to Canada: 1980 vs 2013"
    )
    st.plotly_chart(fig_scatter, width="stretch")

    # -------------------------
    # BAR CHART
    # -------------------------
if show_bar:
    st.subheader("3. Top Countries by Total Immigration")
    st.write("""
This bar chart highlights the countries with the highest total immigration
to Canada over the full period in the dataset.
""")

    top_countries = (
        filtered_df.sort_values(by="Total", ascending=False)
        .head(top_n)
    )

    fig_bar = px.bar(
        top_countries,
        x="Country",
        y="Total",
        color="Continent",
        title=f"Top {top_n} Countries by Total Immigration to Canada"
    )
    st.plotly_chart(fig_bar, width="stretch")

    # -------------------------
    # FINAL INSIGHT
    # -------------------------
if show_hist or show_scatter or show_bar:
    st.subheader("Final Insight")
    st.info("""
The data suggests that immigration to Canada is concentrated in a smaller number
of countries, while most countries contribute lower total volumes.

The filters make it easier to compare continents and observe how immigration
patterns changed over time.
""")
