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
tasks = ["Task1", "Task2", "Task3", "Task 4"]
remaining_time = 0 # Initialize running time as zero

#Key objectives for further improvements:
    # Make it so that the Task Name Search Bar is locked once the user inputs the timer and presses the Start Timer
    # Add Stop Timer Button and Reset Timer Button(self-explainatory)
    # Adding to the Stop and Reset Timer Button, make sure to transform or create a new frame that would display the two buttons
    # Find alternative solution to maek the oble icon a bit larger(it looks quite small still)

#Function for the creation of the search box
def create_searchable_combobox(master, task_list):
    def filter_tasks(event):
        query = search_entry.get().lower()
        filtered = [task for task in task_list if query in task.lower()]
        update_listbox(filtered)

    def update_listbox(filtered_tasks):
        listbox.delete(0, tk.END)
        for task in filtered_tasks:
            listbox.insert(tk.END, task)

        if filtered_tasks:
            listbox.place(x=search_entry.winfo_x(), y=search_entry.winfo_y() + search_entry.winfo_height() + 5, width=search_entry.winfo_width())
        else:
            listbox.place_forget()

    def select_task(event):
        selected = listbox.get(listbox.curselection())
        search_entry.delete(0, tk.END)
        search_entry.insert(0, selected)
        listbox.place_forget()  # Hide listbox after selection

    def hide_listbox(event=None):
        listbox.place_forget()  # Hide the listbox when clicking outside or pressing Escape

    # Create a frame for the search bar
    search_frame = ctk.CTkFrame(master, fg_color="transparent") # Outlline color of the listbox box
    search_frame.pack(pady=10, fill="x")

    # Search entry (like a search bar)
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search tasks...", font=("Arial", 14))
    search_entry.pack(pady=5, fill="x")
    search_entry.bind("<KeyRelease>", filter_tasks)  # Filter tasks as you type
    search_entry.bind("<FocusOut>", hide_listbox)  # Hide listbox when losing focus

    # Listbox for search results (overlay style)
    listbox = tk.Listbox(
        master,
        height=5,
        font=("Arial", 12),
        relief=tk.FLAT,  # No border
        bg="#f9f9f9",    # Light background
        fg="black",
        highlightthickness=1,
        highlightcolor="gray"
    )
    listbox.bind("<<ListboxSelect>>", select_task)
    listbox.bind("<FocusOut>", hide_listbox)  # Hide listbox when it loses focus

    return search_frame

def create_productivity_page(app):
    global timer_running, timer_end_time
    breaks_remaining = 3  # Initializes the number of breaks
    oble_icon = PhotoImage(file=str(relative_to_assets("oble_icon.png")))

    # Create the main frame for the productivity page
    frame_productivity = ctk.CTkFrame(app, fg_color="white")
    frame_productivity.pack(fill="both", expand=True, padx=20, pady=20)

    # Create a frame for the task input and position it properly
    """task_frame = ctk.CTkFrame(frame_productivity, fg_color="transparent")
    task_frame.pack(pady=10, fill="x", expand=True) """

    # Inside create_productivity_page
    search_bar = create_searchable_combobox(frame_productivity, tasks)

    # Create a smaller rounded entry-like ComboBox
    """task_entry = ctk.CTkComboBox(
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
    task_entry.pack(pady=10, fill="x", expand=True) """

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
