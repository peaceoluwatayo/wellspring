import streamlit as st
import pandas as pd
from datetime import datetime
import os
import psycopg2 
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


engine = create_engine("postgresql://student_behaviour_user:GVLnZuwUCelhFhfvRSzDZ3yzHKMB2XQ3@dpg-cu4ij0ogph6c739pa3m0-a.oregon-postgres.render.com/student_behaviour") 
metadata = MetaData()
student_behaviour = Table( 
                          'student_behaviour', metadata, Column('id', Integer, primary_key=True), 
                          Column('student_name', String, nullable=False), 
                          Column('comment', String, nullable=True) 
                          )


# Predefined data for the app with students per class and their full names
TEACHERS = ["Mr. John", "Mrs. Smith", "Ms. Emily"]
STUDENTS = {
    "JSS1": {
        "A": ["Alice Smith", "Bob Johnson", "Charlie Williams", "David Brown", "Eva Taylor", 
              "Frank Miller", "Grace Anderson", "Hannah Moore", "Ian Thomas", "John Jackson", 
              "Kate White", "Leo Harris", "Mia Clark", "Noah Lewis", "Olivia Walker", "Peter Hall", 
              "Quincy Allen", "Rachel Young", "Sophia King", "Tom Scott"],
        "B": ["Ursula Adams", "Victor Nelson", "Wendy Carter", "Xander Perez", "Yvonne Robinson", 
              "Zane Mitchell", "Anna Davis", "Ben Gonzalez", "Clara Lee", "Daniel Martinez", 
              "Eve Perez", "Fay Harris", "Grace Walker", "Henry Scott", "Isabel Moore", "Jake Lee", 
              "Liam Evans", "Mia King", "Nina White", "Oscar Green"],
        "C": ["Paul Davis", "Quinn Harris", "Rose Thomas", "Sam Martinez", "Tina Lopez", 
              "Umar Clark", "Vera Allen", "Will Jackson", "Xander Taylor", "Yvonne Lee", 
              "Zane King", "Anna Scott", "Ben Adams", "Clara Green", "Daniel Thomas", "Eve White", 
              "Fay Gonzalez", "Grace King", "Henry Brown", "Isabel Young"],
        "D": ["Grace Harris", "Henry Walker", "Isabel Clark", "Jake Thomas", "Liam Scott", 
              "Mia Lee", "Nina White", "Oscar Evans", "Paul King", "Quinn Brown", 
              "Rose Lopez", "Sam Martinez", "Tina Green", "Umar Adams", "Vera White", "Will King", 
              "Quincy Scott", "Rachel White", "Sophia Walker", "Tom White"]
    },
    "JSS2": {
        "A": ["James Carter", "Ella Watson", "Ryan Murphy", "Ava Morgan", "Lucas Ward", 
              "Emma Evans", "Daniel Lewis", "Sophia Brooks", "Michael Turner", "Lily Foster", 
              "Jacob Simmons", "Chloe Hill", "Ethan Kelly", "Mia Long", "Matthew Peterson"],
        "B": ["Olivia Reed", "Ethan Young", "Isabella Hall", "Liam Collins", "Emily Baker", 
              "Oliver Nelson", "Charlotte Rivera", "Noah James", "Amelia Adams", "Elijah Rogers", 
              "Mason Price", "Harper Cooper", "Logan Perry", "Sofia Diaz", "Benjamin Barnes"],
        "C": ["Aiden Gray", "Scarlett Russell", "Eliana King", "William Patterson", "Gabriel Howard", 
              "Zoe Hughes", "Caleb Scott", "Savannah Richardson", "Henry Watson", "Layla Bennett", 
              "Jackson Sanders", "Hannah Rivera", "Samuel Foster", "Aubrey Henderson", "Anthony Moore"],
        "D": ["Levi Hayes", "Victoria Jenkins", "Nathan Hughes", "Ella Cook", "Lucas Perez", 
              "Gabriella Stewart", "Julian Butler", "Lucy Bell", "Wyatt Ross", "Violet Edwards", 
              "Andrew Jenkins", "Stella Powell", "Aaron Parker", "Alice Wood", "Isaac Myers"]
    },
    "JSS3": {
        "A": ["Joshua Thompson", "Emily Bennett", "Nathan Carter", "Lily Turner", "Benjamin Scott", 
              "Sophia James", "Jacob Martinez", "Olivia Harris", "Daniel Rivera", "Emma Gray", 
              "Michael Lewis", "Ava Sanders", "Christopher Walker", "Chloe Ward", "Andrew Baker"],
        "B": ["Gabriel Price", "Scarlett Hill", "Mason Long", "Amelia Foster", "Liam Kelly", 
              "Hannah Wood", "Lucas Barnes", "Ella Cooper", "Elijah Hall", "Victoria Adams", 
              "Caleb Perry", "Zoe Hughes", "Samuel Reed", "Layla Ross", "Aiden Powell"],
        "C": ["Oliver Richardson", "Mia Diaz", "William Bennett", "Harper Bell", "Ethan Rogers", 
              "Aubrey Stewart", "Henry Edwards", "Isabella Jenkins", "Logan Perez", "Charlotte Cook", 
              "Wyatt Patterson", "Gabriella Watson", "Levi Parker", "Lily Hughes", "Julian Myers"],
        "D": ["Nathan King", "Lucy Butler", "Aaron Moore", "Savannah Hayes", "Jackson Martinez", 
              "Eliana Ross", "Anthony Walker", "Stella Price", "Andrew Diaz", "Ella Martinez", 
              "Isaac Sanders", "Layla Powell", "Gabriel Hill", "Violet Parker", "Caleb Watson"]
    }
}

SUBJECTS = {
    "JSS1": ["Mathematics", "English", "Science", "Social Studies", "ICT"],
    "JSS2": ["Mathematics", "English", "Physics", "Chemistry", "Biology"],
    "JSS3": ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Geography"]
}

# # MySQL Database Configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'Ibukun@17',
#     'database': 'student_behavior'
# }

# # Data management functions
# def connect_to_db():
#     return mysql.connector.connect(**db_config)

# def save_data_to_db(data):
#     conn = connect_to_db()
#     cursor = conn.cursor()
    
#     insert_query = """
#         INSERT INTO behavior_data 
#         (teacher, class, section, behavior, students, subject, date, timestamp, feedback) 
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
    
#     cursor.executemany(insert_query, data)
#     conn.commit()
#     cursor.close()
#     conn.close()

# App function
def app():
    st.title("Student Behavior Tracker")

    teacher = st.selectbox("Select Teacher", TEACHERS)
    class_ = st.selectbox("Select Class", list(STUDENTS.keys()))
    section = st.selectbox("Select Section", list(STUDENTS[class_].keys()))
    subject = st.selectbox("Select Subject", SUBJECTS[class_])
    date = st.date_input("Select Date")
    students = STUDENTS[class_][section]

    behaviors = [
        "Assignment Defaulting", "Lateness to Class", "Absent from Class", "Classroom Disturbance", 
        "Forgot Note", "Pen/Pencil/Math Set/Calculator", "Forgot Tabs", "Sleeping", 
        "Active Class Participation", "General Feedback on Student Behavior"
    ]

    selected_students_for_behaviors = {}
    for behavior in behaviors:
        if behavior == "General Feedback on Student Behavior":
            selected_students_for_behaviors[behavior] = st.text_area(f"Enter General Feedback for {behavior}")
        else:
            selected_students_for_behaviors[behavior] = st.multiselect(f"Select Students for {behavior} (or select 'None')", ["None"] + students)

    # Validation to ensure no behavior section is left empty
    all_filled = True
    for behavior, selected_students in selected_students_for_behaviors.items():
        if behavior != "General Feedback on Student Behavior" and not selected_students:
            all_filled = False

    if st.button("Submit"):
        general_feedback = selected_students_for_behaviors["General Feedback on Student Behavior"]

        if not all_filled:
            st.error("Please ensure all behavior sections are filled out before submitting.")
        elif general_feedback.strip() == "":
            st.error("General Feedback cannot be empty. Please provide feedback or type 'None'.")
        else:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_to_save = []

            for behavior, selected_students in selected_students_for_behaviors.items():
                if behavior == "General Feedback on Student Behavior":
                    new_data = (
                        teacher, class_, section, behavior, "N/A", subject, date.strftime('%Y-%m-%d'),
                        timestamp, general_feedback.strip()
                    )
                    data_to_save.append(new_data)
                elif selected_students and "None" not in selected_students:
                    new_data = (
                        teacher, class_, section, behavior, ", ".join(selected_students), subject,
                        date.strftime('%Y-%m-%d'), timestamp, "N/A"
                    )
                    data_to_save.append(new_data)

            save_data_to_db(data_to_save)
            st.success("Data successfully submitted!")
            st.write(data_to_save)

if __name__ == "__main__":
    app()
