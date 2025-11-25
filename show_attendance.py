import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTENDANCE_ROOT = os.path.join(BASE_DIR, "Attendance")


def subjectchoose(text_to_speech):
    def show_table(csv_path, subject_name):
        root = tkinter.Tk()
        root.title("Attendance of " + subject_name)
        root.configure(background="black")
        with open(csv_path, newline="") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(
                        root,
                        width=15,
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

    def calculate_attendance():
        subject_name = tx.get().strip()
        if subject_name == "":
            t = "Please enter the subject name."
            text_to_speech(t)
            return

        subject_dir = os.path.join(ATTENDANCE_ROOT, subject_name)
        if not os.path.isdir(subject_dir):
            t = f"No attendance folder found for {subject_name}."
            text_to_speech(t)
            return

        pattern = os.path.join(subject_dir, f"{subject_name}_*.csv")
        filenames = glob(pattern)
        if not filenames:
            t = f"No attendance files found for {subject_name}."
            text_to_speech(t)
            return

        session_frames = []
        base_cols = ["Enrollment", "Name"]

        for file in filenames:
            try:
                df = pd.read_csv(file)
            except Exception:
                continue
            date_cols = [col for col in df.columns if col not in base_cols]
            if not date_cols:
                continue
            session_col = date_cols[0]
            session_name = os.path.splitext(os.path.basename(file))[0]
            frame = df[base_cols + [session_col]].rename(
                columns={session_col: session_name}
            )
            session_frames.append(frame)

        if not session_frames:
            t = f"Attendance data is corrupted for {subject_name}."
            text_to_speech(t)
            return

        merged = session_frames[0]
        for frame in session_frames[1:]:
            merged = merged.merge(frame, on=base_cols, how="outer")
        merged.fillna(0, inplace=True)

        session_cols = [col for col in merged.columns if col not in base_cols]
        if not session_cols:
            t = f"No attendance values stored for {subject_name}."
            text_to_speech(t)
            return

        merged[session_cols] = merged[session_cols].apply(
            pd.to_numeric, errors="coerce"
        ).fillna(0)

        merged["Attendance"] = (
            (merged[session_cols].mean(axis=1, numeric_only=True) * 100)
            .round()
            .astype(int)
            .astype(str)
            + "%"
        )

        summary_path = os.path.join(subject_dir, "attendance.csv")
        merged.to_csv(summary_path, index=False)
        text_to_speech("Attendance generated successfully.")
        show_table(summary_path, subject_name)

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            subject_dir = os.path.join(ATTENDANCE_ROOT, sub)
            if not os.path.isdir(subject_dir):
                t = f"No attendance folder found for {sub}."
                text_to_speech(t)
            else:
                os.startfile(subject_dir)

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
        text="View Attendance",
        command=calculate_attendance,
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
