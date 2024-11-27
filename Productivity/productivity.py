from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import simpledialog, scrolledtext
from datetime import datetime
from ttkbootstrap import Style
import time

def create_productivity_page(app):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets"
    time_running = False #Sets the time running to 0
    breaks_remaining = 3 # Initializes the number of breaks

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

#Initialize the main window
#app = ttk.Window(themename="litera")  # Change theme if needed
#app.geometry("480x820")  # Width x Height in pixels
#app.title("Productivity Mode")
#totaldays = 203
#dayspassed = 90

    oble_icon = PhotoImage(file=str(relative_to_assets("oble_icon.png")))

#List of tasks
    tasks = ["Task 1", "Task 2", "Task 3", "Task 4"] # Will integrate better after successful

    frame_productivity = ttk.Frame(app)
    frame_productivity.pack(fill="both", expand=True)

# Create a frame for the task name input
    task_frame = tk.Frame(frame_productivity)
    task_frame.pack(pady=20)

#bg_frame = ttk.Frame(frame_productivity, style="TaskFrame.TFrame")
#bg_frame.pack(pady=20)

#style = ttk.Style()
#style.configure("TaskFrame.TFrame", background="lightblue")

# Create a label and an entry field for the task name
    task_label = ttk.Label(task_frame, text="Task Name:")
    task_label.pack(pady=0)

    task_entry = ttk.Combobox(task_frame, values=tasks)
    task_entry.pack(side=tk.LEFT, padx=20)

# Create the timer label
    timer_label = tk.Label(frame_productivity, text="30:00", font=("Arial", 36)) 
    timer_label.pack(pady=10, padx=10)

    breaks_label = tk.Label(frame_productivity, text=f"Breaks remaining: {breaks_remaining}")
    breaks_label.pack(pady=10)

# Create a frame for the icon
    icon_frame = ttk.Frame(frame_productivity)
    icon_frame.pack(pady=20)

# Create a label to hold the icon
    icon_label = ttk.Label(icon_frame, image=oble_icon)
    icon_label.pack()

# Center the icon frame
    icon_frame.pack(pady=20)


# Task Name 
# Change this to fuzzy search algorithm
# Initialize the list to be null

    def show_task_name():
        frame_productivity.pack_forget()

        frame_productivity_form = ttk.Frame(app, bootstyle="light")
        frame_productivity_form.pack(fill="both", expand=True)

        ttk.Label(frame_productivity, text="Task Name:", font=("Helvetica", 16))
        task_name_entry = ttk.Entry(frame_productivity_form, width=50)
        task_name_entry.pack(pady=10)

    def start_timer():
        global timer_running, start_time
        if timer_running == False:
            start_button.config(text="Start Timer")
        else:
            timer_running = True
            start_time = time.time()
            start_button.config(text="Pause Timer")
            update_timer()

    def update_timer():
        global timer_running, start_time
        if timer_running:
            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            timer_label.config(text=f"{minutes:02d}:{seconds:02d}") # Also add hours in this configuration 
            app.after(1000, update_timer)

    def reset_timer():
        global timer_running, start_time
        timer_running = False
        start_time = 0
        timer_label.config(text="00:00")
        start_button.config(text="Start Timer")

#Timer Button
    start_timer_button = ctk.CTkButton(
        master=frame_productivity, 
        text="Start Timer",             
        command=start_timer, 
        width=200,
        height=50,
        font=('Arial', 18, 'bold'),
        text_color="white",
        corner_radius=20, 
        fg_color="#cf5b58", 
        hover_color="#c4524e",
        anchor= "center"
        )
    start_timer_button.pack(pady=20, padx=20, side="bottom", fill="x")

# Create Reset button after Start Timer is clicked

# Create the start/pause/reset button
    start_button = tk.Button(frame_productivity, text="Start Timer", command=start_timer)
    start_button.pack(pady=10)

# Create a reset button 
# Reset is below the start timer, adjust so that both are seen
    reset_button = tk.Button(frame_productivity, text="Reset Timer", command=reset_timer)
    reset_button.pack(pady=10)

#Fix the code so that when the true Start Timer is clicked, it would count backwards from the set time interval of the user
    return frame_productivity
