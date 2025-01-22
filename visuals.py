import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

FLASK_API_URL = os.getenv('FLASK_API_URL') + '/get_behavior'

# Helper function to fetch data from the API
def fetch_behavior_data():
    try:
        response = requests.get(FLASK_API_URL)
        # Log the response status code and body for debugging
        st.write(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            st.write(f"Response Data: {data}")  # Log the data to Streamlit
            return pd.DataFrame(data), None
        else:
            error_message = response.json().get('error', 'Failed to fetch data from API.')
            st.write(f"Error Message: {error_message}")  # Log the error message
            return None, error_message
    except Exception as e:
        st.write(f"Error: {e}")  # Log the exception
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
    
    teachers = st.sidebar.multiselect("Filter by Teacher", data["teacher"].unique())
    classes = st.sidebar.multiselect("Filter by Class", data["class_name"].unique())
    sections = st.sidebar.multiselect("Filter by Section", data["section"].unique())
    subjects = st.sidebar.multiselect("Filter by Subject", data["subject"].unique())
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime(data["date"]).min())
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime(data["date"]).max())
    
    # Apply filters
    filtered_data = data.copy()
    
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
    st.dataframe(filtered_data)
    
    # Behavior Counts
    st.subheader("Behavior Analysis")
    behavior_counts = filtered_data["behavior"].value_counts()
    st.bar_chart(behavior_counts)
    
    # Feedback Analysis
    st.subheader("General Feedback")
    feedbacks = filtered_data[~filtered_data["feedback"].isnull()]["feedback"]
    if not feedbacks.empty:
        st.write("\n\n".join(feedbacks))
    else:
        st.write("No feedback available.")
    
if __name__ == "__main__":
    app()
