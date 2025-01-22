import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

API_URL = os.getenv('FLASK_API_URL')


def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Error fetching data!")
        return pd.DataFrame()

# Dashboard Layout
def dashboard():
    st.title("Student Behavior Tracker Dashboard")

    # Fetch Data
    data = fetch_data()

    if not data.empty:
        # Filters
        st.sidebar.header("Filters")
        classes = st.sidebar.multiselect("Select Classes", data["class"].unique())
        date_range = st.sidebar.date_input("Select Date Range", [])
        
        # Apply Filters
        if classes:
            data = data[data["class"].isin(classes)]
        if len(date_range) == 2:
            data = data[(data["date"] >= date_range[0]) & (data["date"] <= date_range[1])]

        # Summary Statistics
        st.subheader("Summary Statistics")
        st.metric("Total Students", len(data["student_id"].unique()))
        st.metric("Total Behaviors Logged", len(data))
        st.metric("Average Attendance", round(data["attendance"].mean(), 2))

        # Visualizations
        st.subheader("Visualizations")
        if not data.empty:
            # Attendance Trend
            attendance_trend = data.groupby("date")["attendance"].mean().reset_index()
            fig = px.line(attendance_trend, x="date", y="attendance", title="Attendance Trend")
            st.plotly_chart(fig)

            # Behavior Breakdown
            behavior_counts = data["behavior"].value_counts().reset_index()
            fig = px.bar(behavior_counts, x="index", y="behavior", title="Behavior Breakdown", labels={"index": "Behavior", "behavior": "Count"})
            st.plotly_chart(fig)

        # Table
        st.subheader("Detailed Data")
        st.dataframe(data)
    else:
        st.warning("No data available to display!")

if __name__ == "__main__":
    dashboard()
