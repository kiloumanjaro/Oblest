from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import simpledialog, scrolledtext
from datetime import datetime
# import calendar

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# --- Main App Window (From First Snippet) ---
app = ttk.Window(themename="litera")  # You can change the theme to your preference
app.geometry("480x820")  # Width x Height in pixels
totaldays = 203
dayspassed = 90

# Load icons (From First Snippet)
# right_icon = PhotoImage(file=str(relative_to_assets("right_icon.png")))
# left_icon = PhotoImage(file=str(relative_to_assets("left_icon.png")))

# Create frames for each section (From First Snippet)
# ... (Rest of the frames and widgets from the first snippet) ...

# --- Task Management Functionality (Refactored from Second Snippet) ---

# Frame for task management content (add to main app)
frame_tasks = ttk.Frame(app, bootstyle="light")
frame_tasks.pack(fill="both", expand=True)

def show_task_form():
    frame_tasks.pack_forget()  # Hide the main tasks frame

    # Create task form frame
    frame_task_form = ttk.Frame(app, bootstyle="light")
    frame_task_form.pack(fill="both", expand=True)

    # Task Title
    ttk.Label(frame_task_form, text="Task Title:").pack(pady=10)
    task_title_entry = ttk.Entry(frame_task_form, width=50)
    task_title_entry.pack(pady=10)

    # Deadline Date
    ttk.Label(frame_task_form, text="Deadline Date:").pack(pady=10)
    deadline_date_entry = ttk.DateEntry(frame_task_form, bootstyle="danger")
    deadline_date_entry.pack(pady=10)

    # Course List
    ttk.Label(frame_task_form, text="Course:", font=('Helvetica', 14, 'bold')).pack(pady=10)
    courses = ["", "Course 1", "Course 2", "Course 3"]
    course_var = tk.StringVar()
    course_var.set(courses[0])
    course_dropdown = ctk.CTkComboBox(
        master=frame_task_form,
        corner_radius=20, 
        text_color="white",
        fg_color="#cf5b58", 
        values=courses,
        variable=course_var,
        button_color="#cf5b58", 
        button_hover_color="#c4524e", 
        dropdown_fg_color="#cf5b58",
        dropdown_hover_color="#c4524e",
        border_color="#cf5b58",
    )
    for course in courses:
        course_dropdown.option_add(value=course, pattern=f"{course}")
    course_dropdown.pack(pady=10)

    # Content
    ttk.Label(frame_task_form, text="Content:").pack(pady=10)
    content_text = scrolledtext.ScrolledText(frame_task_form, width=50, height=10)
    content_text.pack(pady=10)

    def submit_task_form():
        task_title = task_title_entry.get()
        deadline_date = deadline_date_entry.entry.get()
        course = course_var.get()
        content = content_text.get("1.0", "end-1c")

        # Validate deadline date
        try:
            datetime.strptime(deadline_date, "%Y-%m-%d")
        except ValueError:
            simpledialog.messagebox.showerror("Invalid Date", f"Please enter a valid date in the format YYYY-MM-DD: {deadline_date}")
            return

        # Output data
        print("Task Title:", task_title)
        print("Deadline Date:", deadline_date)
        print("Course:", course)
        print("Content:", content)

        frame_task_form.pack_forget()  # Hide task form
        frame_tasks.pack(fill="both", expand=True)  # Show main tasks frame again

    def hide_task_form():
        frame_task_form.pack_forget()  # Hide task form
        frame_tasks.pack(fill="both", expand=True)  # Show main tasks frame again

    # Framed Submit and Cancel Buttons
    
    button_frame = ctk.CTkFrame(
        master=frame_task_form,
        fg_color="#f8f9fa",
        )
    button_frame.pack(pady=10)

    ctk.CTkButton(
        master=button_frame, 
        text="Submit", font=('Helvetica', 16, 'bold'), text_color="white", 
        command=submit_task_form, corner_radius=20, fg_color="#cf5b58", hover_color="#c4524e"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        master=button_frame, 
        text="Cancel", font=('Helvetica', 16, 'bold'), text_color="white", 
        command=hide_task_form, corner_radius=20, fg_color="#cf5b58", hover_color="#c4524e"
    ).pack(side="left", padx=10)

# --- Grid Buttons (Refactored without class) ---

Task_Text = ctk.CTkLabel(
    master=frame_tasks,
    text="You completed",
    font=('Helvetica', 16),
    fg_color="#f8f9fa",
    text_color="black"
    
)

Task_Text.pack(side='top', anchor='w', pady=(50, 0), padx=(20, 0))

Tasks_Completed_Frame = ctk.CTkFrame(
    master=frame_tasks,
    # bg_color="#f8f9fa"
    fg_color="#f8f9fa",
    border_color="#f8f9fa",
)
Tasks_Completed_Frame.pack(side='top', anchor='w', pady=(0, 0), padx=(20, 0))

Tasks_Completed = ctk.CTkLabel(
    master=Tasks_Completed_Frame,
    # text=f"{somenumberhere}";
    text="234",
    font=('Helvetica', 120, 'bold'),
    anchor='w',
    text_color="black"
)
Tasks_Completed.pack(side='left', anchor='sw')

Tasks_Completed_Text = ctk.CTkLabel(
    master=Tasks_Completed_Frame,
    text="tasks",
    font=('Helvetica', 30),
    anchor='w',
    text_color="black"
)
Tasks_Completed_Text.pack(side='left', anchor='sw', pady=(0,20), padx=(5,0))

# Create a CTkFrame as the background in frame_tasks
canvas = ctk.CTkFrame(
    master=frame_tasks, 
    width=320, 
    height=55, 
    corner_radius=50, 
    fg_color="dark grey"
)
canvas.pack(pady=10, padx=10, fill="x")

# Create a frame to hold the grid
grid_frame = ctk.CTkFrame(
    master=canvas, 
    corner_radius=50, 
    fg_color="dark grey"
)
grid_frame.pack(pady=5, padx=5, fill="x")

# Create buttons
button1 = ctk.CTkButton(
    master=grid_frame, 
    text="Button 1", 
    corner_radius=50,
    fg_color="dark grey",
    hover_color="brown3"
)        
button1.grid(row=0, column=0)

button2 = ctk.CTkButton(
    master=grid_frame, 
    text="Button 2", 
    corner_radius=50,
    fg_color="IndianRed1",
    hover_color="brown3"
)        
button2.grid(row=0, column=1)

button3 = ctk.CTkButton(
    master=grid_frame, 
    text="Button 3", 
    corner_radius=50,
    fg_color="dark grey",
    hover_color="brown3"
)        
button3.grid(row=0, column=2)

# Configure grid columns
grid_frame.grid_columnconfigure(0, weight=1)
grid_frame.grid_columnconfigure(1, weight=1)
grid_frame.grid_columnconfigure(2, weight=1)

selected_button = button2  # Initially selected button

def select_button(button):
    global selected_button
    if selected_button:
        selected_button.configure(fg_color="dark grey")
    selected_button = button
    selected_button.configure(fg_color="IndianRed1")

button1.configure(command=lambda: select_button(button1))
button2.configure(command=lambda: select_button(button2))
button3.configure(command=lambda: select_button(button3))

# --- Add Task Button (From Second Snippet) ---
task_button = ctk.CTkButton(
    master=frame_tasks, 
    text="Add Task",             
    command=show_task_form, 
    width=200,
    height=50,
    font=('Helvetica', 18, 'bold'),
    text_color="white",
    corner_radius=20, 
    fg_color="#cf5b58", 
    hover_color="#c4524e",
    anchor= "center"
    )
task_button.pack(pady=20, padx=20, side="bottom", fill="x")

# --- Main App Loop (From First Snippet) ---
app.mainloop()