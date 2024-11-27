from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import simpledialog
import time
# from fuzzywuzzy import process 

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

global timer_running, timer_end_time
timer_running = False  # Initial state of the timer
timer_end_time = 0  # Timer end time
tasks = ["Task1", "Task2", "Task3"]
remaining_time = 0

def naive_algorithm(input_text, tasks):
    return [task for task in tasks if task.lower() == input_text.lower()]

def create_productivity_page(app):
    global timer_running, timer_end_time
    breaks_remaining = 3  # Initializes the number of breaks
    oble_icon = PhotoImage(file=str(relative_to_assets("oble_icon.png")))

    # Create the main frame for the productivity page
    frame_productivity = ctk.CTkFrame(app, fg_color="white")
    frame_productivity.pack(fill="both", expand=True, padx=20, pady=20)

    # Create a frame for the task input and position it properly
    task_frame = ctk.CTkFrame(frame_productivity, fg_color="transparent")
    task_frame.pack(pady=10, fill="x", expand=True)

    # Create a smaller rounded entry-like ComboBox
    task_entry = ctk.CTkComboBox(
        master=task_frame,
        values=tasks,
        corner_radius=20,  # Makes the widget rounded
        width=250,  # Smaller width
        height=30,  # Smaller height
        font=("Arial", 12),  # Adjust font size
        fg_color="gray",
        border_width=1,
        border_color="white",
        state="readonly"
    )
    task_entry.pack(pady=10, fill="x", expand=True)

    # Timer Label
    timer_label = tk.Label(frame_productivity, text="00:00", font=("Arial", 36))
    timer_label.pack(pady=10)

    breaks_label = tk.Label(frame_productivity, text=f"Breaks remaining: {breaks_remaining}")
    breaks_label.pack(pady=10)

    oble_icon_label = tk.Label(
        frame_productivity,
        image=oble_icon,
        bg="white"
    )
    oble_icon_label.image = oble_icon  # Keep a reference to the image
    oble_icon_label.pack(pady=10, fill="x", expand=True)

    # Start Timer Function
    def start_timer():
        global timer_running, timer_end_time, remaining_time
        if not timer_running:
            if remaining_time == 0:  # If the timer hasn't started yet
                # Prompt user for timer input in minutes
                timer_input = simpledialog.askstring("Input", "Enter the time in minutes:", parent=app)
                if timer_input and timer_input.isdigit():
                    timer_duration = int(timer_input) * 60  # Convert minutes to seconds
                    timer_end_time = time.time() + timer_duration  # Calculate end time
                    remaining_time = timer_duration
                else:
                    simpledialog.messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")
                    return
            else:
                timer_end_time = time.time() + remaining_time  # Resume from paused time

            timer_running = True
            start_timer_button.configure(text="Pause Timer", fg_color="#c4524e")
            update_timer()
        else:
            # Pause the timer
            timer_running = False
            remaining_time = max(0, int(timer_end_time - time.time()))  # Store the remaining time
            start_timer_button.configure(text="Start Timer", fg_color="#cf5b58")

    # Update Timer Function
    def update_timer():
        global timer_running, timer_end_time, remaining_time
        if timer_running:
            remaining_time = max(0, int(timer_end_time - time.time()))  # Update remaining time
            if remaining_time <= 0:
                # Stop the timer when it reaches 0
                timer_running = False
                timer_label.config(text="00:00")
                start_timer_button.configure(text="Start Timer", fg_color="#cf5b58")
            else:
                minutes, seconds = divmod(remaining_time, 60)
                timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                app.after(1000, update_timer)  # Call update_timer every second

    # Reset Timer Function
    def reset_timer():
        global timer_running, timer_end_time, remaining_time
        timer_running = False
        timer_end_time = 0
        remaining_time = 0
        timer_label.config(text="00:00")
        start_timer_button.configure(text="Start Timer", fg_color="#cf5b58")

    # Start Timer Button
    start_timer_button = ctk.CTkButton(
        master=frame_productivity,
        text="Start Timer",
        command=start_timer,
        width=200,
        height=50,
        font=('Arial', 18, 'bold'),
        text_color="white",
        corner_radius=20,
        fg_color="#cf5b58",  # Red color for start
        hover_color="#c4524e",  # Hover effect color
        anchor="center"
    )
    start_timer_button.pack(pady=20, padx=20, side="bottom", fill="x")

    # Reset Timer Button
    reset_button = tk.Button(frame_productivity, text="Reset Timer", command=reset_timer)
    reset_button.pack(pady=10)

    return frame_productivity
