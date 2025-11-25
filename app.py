"""
Streamlit Web Application for Face Recognition Attendance System
Suitable for AWS EC2 deployment
"""

import streamlit as st
import cv2
import pandas as pd
import os
import numpy as np
import csv
import datetime
import time
from PIL import Image
import tempfile

# Configure page
st.set_page_config(
    page_title="Face Recognition Attendance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup paths (relative to current directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HAARCASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_alt.xml")
TRAINIMAGE_PATH = os.path.join(BASE_DIR, "TrainingImage")
TRAINIMAGELABEL_PATH = os.path.join(BASE_DIR, "TrainingImageLabel", "Trainner.yml")
STUDENTDETAIL_PATH = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")
ATTENDANCE_PATH = os.path.join(BASE_DIR, "Attendance")

# Create necessary directories
os.makedirs(TRAINIMAGE_PATH, exist_ok=True)
os.makedirs(os.path.dirname(STUDENTDETAIL_PATH), exist_ok=True)
os.makedirs(ATTENDANCE_PATH, exist_ok=True)
os.makedirs(os.path.dirname(TRAINIMAGELABEL_PATH), exist_ok=True)

# Page styling
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {background-color: #4CAF50; color: white; width: 100%;}
    .header {text-align: center; color: #2c3e50;}
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 class='header'>🎓 Face Recognition Attendance System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Alliance University - Secure Face Recognition Based Attendance</p>", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Navigation")
menu_option = st.sidebar.radio(
    "Select an option:",
    ["🏠 Home", "👤 Register Student", "✅ Take Attendance", "📊 View Attendance"]
)

# Helper functions
def load_student_details():
    """Load student details from CSV"""
    if os.path.exists(STUDENTDETAIL_PATH):
        try:
            return pd.read_csv(STUDENTDETAIL_PATH)
        except:
            return pd.DataFrame(columns=["Enrollment", "Name"])
    return pd.DataFrame(columns=["Enrollment", "Name"])

def save_student_details(enrollment, name):
    """Save student details to CSV"""
    os.makedirs(os.path.dirname(STUDENTDETAIL_PATH), exist_ok=True)
    
    # Check if file exists and has content
    write_header = not os.path.isfile(STUDENTDETAIL_PATH) or os.path.getsize(STUDENTDETAIL_PATH) == 0
    
    with open(STUDENTDETAIL_PATH, "a+", newline="") as csvFile:
        writer = csv.writer(csvFile, delimiter=",")
        if write_header:
            writer.writerow(["Enrollment", "Name"])
        writer.writerow([enrollment, name])

def detect_faces(image, detector):
    """Detect faces in image"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    return faces, gray

def train_model():
    """Train LBPH Face Recognizer"""
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(HAARCASCADE_PATH)
        
        faces = []
        ids = []
        student_details = load_student_details()
        
        # Extract enrollment numbers
        enrollment_dict = {str(row['Name']).lower(): int(row['Enrollment']) 
                          for _, row in student_details.iterrows()}
        
        # Traverse training images
        for person_name in os.listdir(TRAINIMAGE_PATH):
            person_path = os.path.join(TRAINIMAGE_PATH, person_name)
            if not os.path.isdir(person_path):
                continue
            
            # Extract enrollment from folder name (format: enrollment_name)
            enrollment_id = enrollment_dict.get(person_name.split('_')[1].lower(), 0)
            
            if enrollment_id == 0:
                continue
            
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                try:
                    image = cv2.imread(image_path)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    face_crop = gray
                    
                    if face_crop.size > 0:
                        faces.append(face_crop)
                        ids.append(enrollment_id)
                except:
                    continue
        
        if len(faces) > 0:
            recognizer.train(faces, np.array(ids))
            recognizer.save(TRAINIMAGELABEL_PATH)
            return True, f"Model trained with {len(faces)} images"
        else:
            return False, "No training images found"
    except Exception as e:
        return False, str(e)

# Pages
if menu_option == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("UI_Image/0001.png" if os.path.exists("UI_Image/0001.png") else None, use_column_width=True)
    
    with col2:
        st.subheader("Welcome to FaceProof Attendance System")
        st.info("""
        This system uses advanced face recognition technology to:
        - ✅ Automate attendance marking
        - 🔒 Ensure secure verification
        - 📊 Generate real-time reports
        - 💾 Store attendance records safely
        """)
        
        st.subheader("Quick Stats")
        students_df = load_student_details()
        st.metric("Registered Students", len(students_df))
        
        # Display registered students
        if len(students_df) > 0:
            st.subheader("📋 Registered Students")
            st.dataframe(students_df, use_container_width=True)

elif menu_option == "👤 Register Student":
    st.subheader("Register New Student")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enrollment = st.text_input("Enrollment Number", key="enroll_reg")
        name = st.text_input("Student Name", key="name_reg")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("Register Student", key="register_btn"):
            if enrollment and name:
                try:
                    save_student_details(enrollment, name)
                    st.success(f"✅ Student {name} (ER: {enrollment}) registered successfully!")
                    
                    # Create directory for training images
                    student_dir = os.path.join(TRAINIMAGE_PATH, f"{enrollment}_{name}")
                    os.makedirs(student_dir, exist_ok=True)
                    st.info(f"📁 Training image directory created: {student_dir}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter both Enrollment Number and Name")
    
    st.markdown("---")
    st.subheader("Registered Students")
    students_df = load_student_details()
    if len(students_df) > 0:
        st.dataframe(students_df, use_container_width=True)
    else:
        st.info("No students registered yet")

elif menu_option == "✅ Take Attendance":
    st.subheader("Mark Attendance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input("Subject Name", key="subject")
        duration = st.slider("Recognition Duration (seconds)", 10, 120, 30)
    
    with col2:
        st.write("")
        if st.button("Start Face Recognition", key="start_recognition"):
            if subject:
                st.info("🎥 Starting face recognition... (Make sure your camera is enabled)")
                
                # Simulate attendance process
                st.write("Camera would start here in a desktop application")
                
                # For demo, create a sample attendance record
                col_names = ["Enrollment", "Name"]
                attendance_df = pd.DataFrame(columns=col_names)
                
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.now().strftime("%H:%M:%S")
                attendance_df[date] = 1
                
                hour, minute, second = timeStamp.split(":")
                path = os.path.join(ATTENDANCE_PATH, subject)
                os.makedirs(path, exist_ok=True)
                
                fileName = os.path.join(
                    path,
                    f"{subject}_{date}_{hour}-{minute}-{second}.csv"
                )
                
                st.success(f"✅ Attendance file would be saved to: {fileName}")
            else:
                st.warning("⚠️ Please enter Subject Name")

elif menu_option == "📊 View Attendance":
    st.subheader("View Attendance Records")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input("Subject Name", key="subject_view")
    
    with col2:
        st.write("")
        if st.button("View Attendance", key="view_btn"):
            if subject:
                subject_path = os.path.join(ATTENDANCE_PATH, subject)
                
                if os.path.isdir(subject_path):
                    csv_files = [f for f in os.listdir(subject_path) if f.endswith('.csv')]
                    
                    if csv_files:
                        st.success(f"Found {len(csv_files)} attendance record(s)")
                        
                        # Load and display attendance files
                        dfs = []
                        for csv_file in csv_files:
                            try:
                                df = pd.read_csv(os.path.join(subject_path, csv_file))
                                st.subheader(f"📄 {csv_file}")
                                st.dataframe(df, use_container_width=True)
                                dfs.append(df)
                            except Exception as e:
                                st.error(f"Error reading {csv_file}: {str(e)}")
                        
                        # Summary attendance
                        if dfs:
                            st.subheader("📊 Attendance Summary")
                            merged_df = dfs[0]
                            for df in dfs[1:]:
                                merged_df = merged_df.merge(df, on=["Enrollment", "Name"], how="outer")
                            
                            merged_df.fillna(0, inplace=True)
                            date_cols = [col for col in merged_df.columns if col not in ["Enrollment", "Name"]]
                            
                            if date_cols:
                                merged_df["Attendance %"] = (
                                    (merged_df[date_cols].mean(axis=1) * 100)
                                    .round()
                                    .astype(int)
                                    .astype(str) + "%"
                                )
                                st.dataframe(merged_df, use_container_width=True)
                    else:
                        st.warning(f"No attendance records found for {subject}")
                else:
                    st.warning(f"No attendance folder found for {subject}")
            else:
                st.warning("⚠️ Please enter Subject Name")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #95a5a6; font-size: 12px;'>
    <p>🔒 Secure Face Recognition Attendance System | Alliance University</p>
    <p>Deployed with AWS EC2 | Streamlit Application</p>
    </div>
    """, unsafe_allow_html=True)
