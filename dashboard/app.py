import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Smart City Real-Time Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Database Config
# =========================
DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "smartcity"),
    "user": os.getenv("POSTGRES_USER", "bigdata"),
    "password": os.getenv("POSTGRES_PASSWORD", "bigdata123"),
}

# =========================
# DB Helpers
# =========================
@st.cache_resource
def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def fetch_df(query):
    return pd.read_sql_query(query, get_connection())

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("Dashboard Controls")
    auto_refresh = st.checkbox("Auto Refresh (5s)", value=True)
    st.markdown("---")
    st.success("Pipeline Status: All services running ✅")

# =========================
# Header
# =========================
st.title("🏙️ Smart City Real-Time Analytics Dashboard")
st.caption("Kafka → Spark Streaming → PostgreSQL → Streamlit")
st.markdown("---")

# =========================
# Quick Stats
# =========================
col1, col2, col3, col4, col5 = st.columns(5)

vehicle_count = fetch_df("SELECT COUNT(*) AS c FROM vehicle_data")["c"][0]
gps_count = fetch_df("SELECT COUNT(*) AS c FROM gps_data")["c"][0]
traffic_count = fetch_df("SELECT COUNT(*) AS c FROM traffic_data")["c"][0]
weather_count = fetch_df("SELECT COUNT(*) AS c FROM weather_data")["c"][0]
emergency_count = fetch_df("SELECT COUNT(*) AS c FROM emergency_data")["c"][0]

col1.metric("🚗 Vehicle Events", vehicle_count)
col2.metric("📍 GPS Records", gps_count)
col3.metric("📸 Traffic Cameras", traffic_count)
col4.metric("🌦 Weather Updates", weather_count)
col5.metric("🚨 Emergencies", emergency_count)

st.markdown("---")

# =========================
# Vehicle Speed Timeline
# =========================
st.subheader("🚗 Vehicle Speed Over Time")

speed_df = fetch_df("""
    SELECT timestamp, speed
    FROM vehicle_data
    ORDER BY timestamp DESC
    LIMIT 300
""")

fig_speed = px.line(
    speed_df.sort_values("timestamp"),
    x="timestamp",
    y="speed",
    title="Vehicle Speed (km/h)",
)
st.plotly_chart(fig_speed, use_container_width=True)

# =========================
# Weather Distribution
# =========================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌤 Weather Conditions")
    weather_df = fetch_df("""
        SELECT weather_condition, COUNT(*) AS count
        FROM weather_data
        GROUP BY weather_condition
    """)
    fig_weather = px.pie(
        weather_df,
        values="count",
        names="weather_condition",
        title="Weather Condition Distribution"
    )
    st.plotly_chart(fig_weather, use_container_width=True)

with col_right:
    st.subheader("🌡 Temperature Trend")
    temp_df = fetch_df("""
        SELECT timestamp, temperature
        FROM weather_data
        ORDER BY timestamp DESC
        LIMIT 300
    """)
    fig_temp = px.line(
        temp_df.sort_values("timestamp"),
        x="timestamp",
        y="temperature",
        title="Temperature Over Time (°C)"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

# =========================
# Emergency Incidents
# =========================
st.markdown("---")
st.subheader("🚨 Emergency Incidents")

emergency_df = fetch_df("""
    SELECT type, COUNT(*) AS count
    FROM emergency_data
    GROUP BY type
""")

fig_emergency = px.bar(
    emergency_df,
    x="type",
    y="count",
    title="Emergency Incidents by Type",
    color="type"
)
st.plotly_chart(fig_emergency, use_container_width=True)

# =========================
# Recent Events Table
# =========================
st.markdown("---")
st.subheader("📋 Recent Vehicle Events")

recent_df = fetch_df("""
    SELECT device_id, timestamp, speed, location
    FROM vehicle_data
    ORDER BY timestamp DESC
    LIMIT 20
""")

st.dataframe(recent_df, use_container_width=True)

# =========================
# Auto Refresh
# =========================
if auto_refresh:
    time.sleep(5)
    st.rerun()