import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Tamil Nadu Offshore Wind Dashboard",
    layout="wide"
)

st.title("🌊 Tamil Nadu Offshore Wind Dashboard")
st.markdown("### Combined December + August Dataset")

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------

selected_date = st.sidebar.selectbox(
    "Select Dataset",
    [
        "2025-12-02",
        "2025-08-15"
    ]
)

# --------------------------------------------------
# API URL
# --------------------------------------------------

API_URL = (
    f"http://127.0.0.1:8001/api/wind"
    f"?date={selected_date}"
    f"&lat_min=9"
    f"&lat_max=13"
    f"&lon_min=78"
    f"&lon_max=82"
)

# --------------------------------------------------
# FETCH DATA
# --------------------------------------------------

try:

    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error(f"API Error: {response.status_code}")
        st.stop()

    api_data = response.json()

    data = api_data.get("data", [])

    if len(data) == 0:
        st.warning("No data returned from API")
        st.stop()

    df = pd.DataFrame(data)

    # --------------------------------------------------
    # SPEED FILTER
    # --------------------------------------------------

    min_speed_filter = st.sidebar.slider(
        "Minimum Wind Speed (m/s)",
        min_value=0,
        max_value=20,
        value=0
    )

    df = df[df["speed_ms"] >= min_speed_filter]

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Wind Vectors",
            len(df)
        )

    with col2:
        st.metric(
            "Average Speed",
            f"{df['speed_ms'].mean():.2f} m/s"
        )

    with col3:
        st.metric(
            "Maximum Speed",
            f"{df['speed_ms'].max():.2f} m/s"
        )

    st.markdown("---")

    # --------------------------------------------------
    # MAP
    # --------------------------------------------------

    st.subheader("Wind Vector Spatial Distribution")

    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="speed_ms",
        size="speed_ms",
        hover_data=[
            "speed_ms",
            "direction_deg"
        ],
        zoom=7,
        height=700,
        color_continuous_scale="Jet"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # DATA TABLE
    # --------------------------------------------------

    st.subheader("Wind Vector Data")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error: {e}")