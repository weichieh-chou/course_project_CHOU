"""Streamlit dashboard to explore and filter the Forest Cover Type dataset."""
import pandas as pd
import streamlit as st

from src.data import filter_data, load_data

DATA_PATH = "data/train.csv"
WILDERNESS_AREAS = [1, 2, 3, 4]
COVER_TYPES = [1, 2, 3, 4, 5, 6, 7]


@st.cache_data
def get_data():
    return load_data(DATA_PATH)


st.set_page_config(page_title="Forest Cover Type Explorer", layout="wide")
st.title("Forest Cover Type Explorer")
st.caption(
    "Explore the Kaggle Forest Cover Type dataset: filter by wilderness area, "
    "cover type, and elevation."
)

df = get_data()

st.sidebar.header("Filters")
selected_areas = st.sidebar.multiselect(
    "Wilderness area", WILDERNESS_AREAS, default=WILDERNESS_AREAS
)
selected_cover_types = st.sidebar.multiselect(
    "Cover type", COVER_TYPES, default=COVER_TYPES
)
elevation_min, elevation_max = int(df["Elevation"].min()), int(df["Elevation"].max())
selected_elevation_range = st.sidebar.slider(
    "Elevation range",
    min_value=elevation_min,
    max_value=elevation_max,
    value=(elevation_min, elevation_max),
)

filtered_df = filter_data(
    df,
    wilderness_areas=selected_areas,
    cover_types=selected_cover_types,
    elevation_range=selected_elevation_range,
)

st.metric("Rows matching filters", len(filtered_df))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Cover type distribution")
    st.bar_chart(filtered_df["Cover_Type"].value_counts().sort_index())
with col2:
    st.subheader("Elevation distribution")
    elevation_bins = pd.cut(filtered_df["Elevation"], bins=15)
    counts = elevation_bins.value_counts().sort_index()
    counts.index = [f"{int(interval.left)}" for interval in counts.index]
    st.bar_chart(counts)

st.subheader("Filtered data")
st.dataframe(filtered_df, use_container_width=True)
