import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

haarcasecade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_alt.xml")
trainimagelabel_path = os.path.join(BASE_DIR, "TrainingImageLabel", "Trainner.yml")
trainimage_path = os.path.join(BASE_DIR, "TrainingImage")
studentdetail_path = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")
attendance_path = os.path.join(BASE_DIR, "Attendance")
os.makedirs(attendance_path, exist_ok=True)
# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get().strip()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                Subject = sub
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                    return
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)

                if not os.path.exists(studentdetail_path):
                    msg = "Student details not found. Please register a student first."
                    text_to_speech(msg)
                    return

                df = pd.read_csv(studentdetail_path)
                if "Enrollment" not in df.columns or "Name" not in df.columns:
                    if df.shape[1] >= 2:
                        df = df.iloc[:, :2]
                        df.columns = ["Enrollment", "Name"]
                    else:
                        msg = "Student details file is corrupted. Please register again."
                        text_to_speech(msg)
                        return
                df = df.dropna(subset=["Enrollment", "Name"])
                try:
                    df["Enrollment"] = df["Enrollment"].astype(int)
                except ValueError:
                    msg = "Enrollment IDs must be numeric. Please re-register students."
                    text_to_speech(msg)
                    return
                cam = cv2.VideoCapture(0)
                if not cam.isOpened():
                    text_to_speech("Unable to access camera.")
                    return
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    if not ret:
                        continue
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            Subject = sub
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            name_series = df.loc[df["Enrollment"] == Id]["Name"]
                            if name_series.empty:
                                name = "Unknown"
                            else:
                                name = str(name_series.iloc[0])
                            captured_name = name
                            attendance.loc[len(attendance)] = [
                                Id,
                                name,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im,
                                f"{Id}-{name}",
                                (x + h, y),
                                font,
                                1,
                                (255, 255, 0),
                                4,
                            )
                        else:
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, "Unknown", (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                if attendance.empty:
                    cam.release()
                    cv2.destroyAllWindows()
                    f = "No Face found for attendance"
                    text_to_speech(f)
                    return

                date = datetime.datetime.now().strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.now().strftime("%H:%M:%S")
                attendance[date] = 1
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                os.makedirs(path, exist_ok=True)
                fileName = os.path.join(
                    path,
                    f"{Subject}_{date}_{Hour}-{Minute}-{Second}.csv",
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")
                print(fileName)
                with open(fileName, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except Exception as err:
                print(f"Attendance error: {err}")
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    ###windo is frame for subject chooser
    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            target_dir = os.path.join(attendance_path, sub)
            if not os.path.isdir(target_dir):
                t = f"No attendance folder found for {sub}."
                text_to_speech(t)
            else:
                os.startfile(target_dir)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()