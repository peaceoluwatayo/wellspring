import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import altair as alt
import warnings

# Suppress specific warning related to Altair
warnings.filterwarnings("ignore", message="I don't know how to infer vegalite type")

# Load environment variables from the .env file
load_dotenv()

FLASK_API_URL = os.getenv('FLASK_API_URL') + '/get_behavior'

# Helper function to fetch data from the API
def fetch_behavior_data():
    try:
        response = requests.get(FLASK_API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json()), None
        else:
            error_message = response.json().get('error', 'Failed to fetch data from API.')
            return None, error_message
    except Exception as e:
        return None, str(e)

# Streamlit app
def app():
    st.title("Student Behavior Dashboard")
    
    # Fetch data
    data, error = fetch_behavior_data()
    
    if error:
        st.error(f"Error fetching data: {error}")
        return
    
    if data.empty:
        st.warning("No data available to display.")
        return
    
    # Data Filters
    st.sidebar.header("Filters")
    
    students = st.sidebar.multiselect("Filter by Student", data["students"].unique())
    teachers = st.sidebar.multiselect("Filter by Teacher", data["teacher"].unique())
    classes = st.sidebar.multiselect("Filter by Class", data["class_name"].unique())
    sections = st.sidebar.multiselect("Filter by Section", data["section"].unique())
    subjects = st.sidebar.multiselect("Filter by Subject", data["subject"].unique())
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime(data["date"]).min())
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime(data["date"]).max())
    
    # Apply filters
    filtered_data = data.copy()
    
    if students:
        filtered_data = filtered_data[filtered_data["students"].str.contains('|'.join(students), na=False)]
    if teachers:
        filtered_data = filtered_data[filtered_data["teacher"].isin(teachers)]
    if classes:
        filtered_data = filtered_data[filtered_data["class_name"].isin(classes)]
    if sections:
        filtered_data = filtered_data[filtered_data["section"].isin(sections)]
    if subjects:
        filtered_data = filtered_data[filtered_data["subject"].isin(subjects)]
    filtered_data = filtered_data[(
        pd.to_datetime(filtered_data["date"]) >= pd.to_datetime(start_date)) & 
        (pd.to_datetime(filtered_data["date"]) <= pd.to_datetime(end_date))
    ]
    
    # Display filtered data
    st.subheader("Filtered Behavior Data")
    if filtered_data.empty:
        st.warning("No matching data found.")
    else:
        st.dataframe(filtered_data)
    
    # Behavior Counts
    st.subheader("Behavior Analysis")
    if "behavior" in filtered_data.columns:
        # Clean behavior column
        filtered_data['behavior'] = filtered_data['behavior'].fillna('No Behavior')

        # Generate bar chart for behavior counts
        behavior_counts = filtered_data['behavior'].value_counts().reset_index()
        behavior_counts.columns = ['Behavior', 'Count']
        
        chart = alt.Chart(behavior_counts).mark_bar().encode(
            x='Behavior:N',
            y='Count:Q'
        )
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No behavior data available for analysis.")
    
    # Feedback Analysis
    st.subheader("General Feedback")
    feedbacks = filtered_data[~filtered_data["feedback"].isnull()]["feedback"]
    if not feedbacks.empty:
        st.write("\n\n".join(feedbacks))
    else:
        st.write("No feedback available.")
    
if __name__ == "__main__":
    app()
