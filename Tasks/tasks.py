# ==============================================
# Section 1: Data Preparation
# ==============================================

from pathlib import Path
from Tasks.TaskManager import TaskStatus, Task, Node
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
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

# ==============================================
# Testing
# ==============================================

# # Create the application window
# app = ttk.Window(themename="custom")  # Using ttkbootstrap for theming
# app.geometry("480x820")  # Width x Height in pixels
# app.title("Progress Tracker")


def create_tasks_page(app):

    # ==============================================
    # Section 2: Window Initialization
    # ==============================================

    frame_taskpage = ttk.Frame(app, bootstyle="primary")
    is_overlay_shown = False  # Flag to track overlay visibility

    frame_controls = ttk.Frame(frame_taskpage, padding=0)
    frame_controls.pack(fill="x", padx=10, pady=(10, 5))

    frame_button = ttk.Frame(frame_taskpage, bootstyle="primary", padding=0)
    frame_button.pack(fill="x", padx=10, pady=(0, 5), side="bottom")

    left_button_state = BooleanVar(value=False)
    right_button_state = BooleanVar(value=False)

    # Load icons
    right_icon = PhotoImage(file=str(relative_to_assets("right_icon.png")))
    left_icon = PhotoImage(file=str(relative_to_assets("left_icon.png")))
    right_icon_active = PhotoImage(file=str(relative_to_assets("right_icon_active.png")))
    left_icon_active = PhotoImage(file=str(relative_to_assets("left_icon_active.png")))

    # ==============================================
    # Section 3: Frame Creation
    # ==============================================

    # frame_text = ttk.Frame(frame_taskpage bootstyle="primary", padding=10)
    # frame_text.pack(fill="x", padx=10, pady=5)

    # frame_days = ttk.Frame(frame_taskpage bootstyle="primary", padding=5)
    # frame_days.pack(fill="x", padx=10, pady=0, anchor="center")

    # frame_empty = ttk.Frame(frame_taskpage bootstyle="primary", padding=5)
    # frame_empty.pack(fill="x", padx=10, pady=(10, 5))

    # overlay_frame = ttk.Frame(frame_taskpage bootstyle="primary", padding=10)

    frame_tasks = ttk.Frame(frame_taskpage, bootstyle="light")
    frame_tasks.pack(fill="both", expand=True)

    # ==============================================
    # Section 4: Button Functions and Creation
    # ==============================================

    def toggle_left_button():
        if left_button_state.get():
            left_button_state.set(False)
            button_left.configure(image=left_icon)  # Default style
        else:
            left_button_state.set(True)
            button_left.configure(image=left_icon_active)  # Active style
        # toggle_overlay()

    # Function to toggle right button state
    def toggle_right_button():
        if right_button_state.get():
            right_button_state.set(False)
            button_right.configure(image=right_icon)
        else:
            right_button_state.set(True)
            button_right.configure(image=right_icon_active)  # Active style

    # Updated Left Button
    button_left = ttk.Button(
        frame_controls,
        text="",
        image=left_icon,
        command=toggle_left_button,
        bootstyle="secondary, link"
    )
    button_left.pack(side="left", padx=0, anchor="w")

    # Updated Right Button
    button_right = ttk.Button(
        frame_controls,
        text="",
        image=right_icon,
        command=toggle_right_button,
        bootstyle="primary, link",
        width=5
    )
    button_right.pack(side="right", padx=0, anchor="e")

    # ==============================================
    # Section 5: Task Form Functions and Creation
    # ==============================================

    # ----------------------------------------------
    # 5.1: Main Form Display Function
    # ----------------------------------------------
    def show_task_form():
        frame_tasks.pack_forget()
        frame_button.pack_forget()
        frame_pages.pack_forget()

        frame_task_form = ttk.Frame(frame_task, bootstyle="light")
        frame_task_form.pack(fill="both", expand=True)

    # ----------------------------------------------
    # 5.2: Form Field Creation
    # ----------------------------------------------
        # Task Title Field
        ttk.Label(frame_task_form, text="Task Title:").pack(pady=10)
        task_title_entry = ttk.Entry(frame_task_form, width=50)
        task_title_entry.pack(pady=10)

        # Deadline Date Field
        ttk.Label(frame_task_form, text="Deadline Date:").pack(pady=10)
        deadline_date_entry = ttk.DateEntry(
            master=frame_task_form, 
            bootstyle="danger", 
            dateformat="%Y-%m-%d"
        )
        deadline_date_entry.pack(pady=10)

        # Course Selection Field
        ttk.Label(frame_task_form, text="Course:", font=('Helvetica', 14, 'bold')).pack(pady=10)
        courses = ["General", "Course 1", "Course 2", "Course 3"]
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

        # Content Field
        ttk.Label(frame_task_form, text="Content:").pack(pady=10)
        content_text = scrolledtext.ScrolledText(frame_task_form, width=50, height=10)
        content_text.pack(pady=10)

    # ----------------------------------------------
    # 5.3: Form Action Functions
    # ----------------------------------------------
        def submit_task_form():
            task_title = task_title_entry.get()
            deadline_date = deadline_date_entry.entry.get()
            course = course_var.get()
            content = content_text.get("1.0", "end-1c")

            # Validate deadline date
            try:
                datetime.strptime(deadline_date, "%Y-%m-%d")
            except ValueError:
                simpledialog.messagebox.showerror(
                    "Invalid Date", 
                    f"Please enter a valid date in the format YYYY-MM-DD: {deadline_date}"
                )
                return

            # Output data
            print("Task Title:", task_title)
            print("Deadline Date:", deadline_date)
            print("Course:", course)
            print("Content:", content)

            frame_task_form.pack_forget()
            frame_tasks.pack(fill="both", expand=True)

        def hide_task_form():
            frame_task_form.pack_forget()
            frame_tasks.pack(fill="both", expand=True)
            frame_pages.pack(padx=0, pady=0, anchor="center")
            frame_button.pack(fill="x", padx=10, pady=(0, 10), side="bottom")

    # ----------------------------------------------
    # 5.4: Button Creation and Layout
    # ----------------------------------------------
        button_frame = ctk.CTkFrame(
            master=frame_task_form,
            fg_color="#f8f9fa",
        )
        button_frame.pack(pady=10)

        ctk.CTkButton(
            master=button_frame, 
            text="Submit", 
            font=('Helvetica', 14),
            text_color="white", 
            command=submit_task_form,
            corner_radius=20,
            fg_color="#cf5b58",
            hover_color="#c4524e"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            master=button_frame, 
            text="Cancel",
            font=('Helvetica', 14),
            text_color="white", 
            command=hide_task_form,
            corner_radius=20,
            fg_color="#cf5b58",
            hover_color="#c4524e"
        ).pack(side="left", padx=10)
        
    # ==============================================
    # Section 6: Task Count Display
    # ==============================================

    # Create a frame to hold the task count text
    frame_task_count = ctk.CTkFrame(
        master=frame_tasks,
        bg_color="transparent",
        fg_color="#f8f9fa",
        border_color="#f8f9fa",
    )
    frame_task_count.pack(side='top', anchor='w', pady=(0, 0), padx=(20, 0))

    # Create text for task count
    Task_Text = ctk.CTkLabel(
        master=frame_task_count,
        text="You completed",  # Title of task count
        font=('Inter', 16),  # Font style and size
        fg_color="#f8f9fa",  # Background color
        text_color="black"  # Text color
    )
    Task_Text.pack(side='top', anchor='w', pady=(10, 0), padx=(20, 0))

    # Create frame to hold task count number and text
    Tasks_Completed_Frame = ctk.CTkFrame(
        master=frame_task_count,
        bg_color="transparent",
        fg_color="#f8f9fa",
        border_color="#f8f9fa",
    )
    Tasks_Completed_Frame.pack(side='top', anchor='w', pady=(0, 0), padx=(20, 0))

    # Create task count number
    Tasks_Completed = ctk.CTkLabel(
        master=Tasks_Completed_Frame,
        # text=f"{somenumberhere}";  # Replace with actual number
        text="234",  # Replace with actual number
        bg_color="transparent",  # Background color
        fg_color="#f8f9fa",  # Foreground color
        font=('Inter', 120),  # Font style and size
        anchor='w',  # Anchor position
        text_color="black"  # Text color
    )
    Tasks_Completed.pack(side='left', anchor='sw')

    # Create text for "tasks"
    Tasks_Completed_Text = ctk.CTkLabel(
        master=Tasks_Completed_Frame,
        text="tasks",  # Text to display
        bg_color="transparent",  # Background color
        fg_color="#f8f9fa",  # Foreground color
        font=('Inter', 30),  # Font style and size
        anchor='w',  # Anchor position
        text_color="black"  # Text color
    )
    Tasks_Completed_Text.pack(side='left', anchor='sw', pady=(0,20), padx=(5,0))

    # ==============================================
    # Section 7: Segmented Buttons AND Calendar
    # ==============================================

    # Code here that shows different frames of tasks groupings
    def calendar(option):
        print(f"Selected option: {option}")

    segmented_frame = ctk.CTkFrame(
        master=frame_tasks, 
        fg_color="#f8f9fa",
        bg_color="#f8f9fa"
    )
    segmented_frame.pack(fill="x", padx=15, expand=YES)

    button1 = ctk.CTkSegmentedButton(
        master=segmented_frame, 
        corner_radius=200,
        height=50,
        border_width=0,
        fg_color="white",
        font=("Arial", 16, "bold"),
        text_color="black",
        text_color_disabled="white",
        selected_hover_color="#cf5b58",
        selected_color="#cf5b58",
        unselected_hover_color="brown3",
        unselected_color="white",
        values=["Day", "Week", "Month"],
        command=lambda option: calendar(option)
    )
    button1.pack(
        fill=BOTH, 
        expand=YES
        )

    button1.set("Day")

    # ==============================================
    # Section 8: Scrollable current Tasks Frame
    # ==============================================

    #  Holds a variable amount of frames containing unique information depending on the task

    frame_current_tasks = ctk.CTkScrollableFrame(
        master=frame_tasks,
        bg_color="transparent",
        corner_radius=0,
        fg_color="#f8f9fa",
        height = 350,
        border_color="#f8f9fa",
    )
    frame_current_tasks.pack(pady=(0, 5), padx=(10, 10), fill=BOTH, side="bottom", expand=YES)

    # ==============================================
    # Section 9: Task Nodes and Frame Creation
    # ==============================================

    # ----------------------------------------------
    # 9.1: Sample Data and Node Creation
    # ----------------------------------------------
    # Sample task list creation
    tasks = [
        Task(1, "Task 1", 5, [], "Task 1 content", "Course 1", 3, "2022-01-01", deadline="2022-01-15"),
        Task(2, "Task 2", 3, [], "Task 2 content", "Course 2", 2, "2022-01-05"),
        Task(3, "Task 3", 8, [], "Task 3 content", "Course 3", 4, "2022-01-10", deadline="2022-01-20"),
        Task(4, "Task 4", 6, [], "Task 4 content", "Course 4", 3, "2022-01-15", deadline="2022-01-25"),
    ]

    # Node list generation from tasks
    nodes = [Node(task, 1) for task in tasks]

    # ----------------------------------------------
    # 9.2: Generic Frame Generation
    # ----------------------------------------------
    def create_generic_frame(master):
        generic_task = ctk.CTkFrame(
            master=master,
            bg_color="white",
            corner_radius=40,
            height=105
        )
        generic_task.pack(pady=(8, 8), padx=(5, 5), fill=X, side="top", expand=YES)
        
        ctk.CTkLabel(
            master=generic_task,
            text="No tasks available",
            text_color="gray",
            font=("Arial", 16)
        ).pack(pady=(20, 20), padx=(20, 20))

    # ----------------------------------------------
    # 9.3: Node Frame Generation
    # ----------------------------------------------
    def create_node_frame(master, node):
        course_color = {
            "Course 1": "#FFC080",  # Orange
            "Course 2": "#C5CAE9",  # Blue
            # Add more course colors as needed
        }

        node_task = ctk.CTkFrame(
            master=master,
            fg_color=course_color.get(node.task.course_tag, "white"),
            corner_radius=40,
            height=105
        )
        node_task.pack(pady=(8, 8), padx=(5, 5), fill=tk.X, side="top", expand=tk.YES)

        ctk.CTkLabel(
            master=node_task,
            text=node.task.name,
            text_color="black",
            font=("Arial", 16)
        ).pack(pady=(10, 5), padx=(20, 20))

        ctk.CTkLabel(
            master=node_task,
            text=node.task.text_content,
            text_color="gray",
            font=("Arial", 14)
        ).pack(pady=(0, 10), padx=(20, 20))

        ctk.CTkLabel(
            master=node_task,
            text=node.task.course_tag,
            text_color="gray",
            font=("Arial", 14)
        ).pack(pady=(0, 10), padx=(20, 20))

    # ----------------------------------------------
    # 9.4: Frame Creation Logic
    # ----------------------------------------------
    if nodes:
        for node in nodes:
            create_node_frame(frame_current_tasks, node)
    else:
        create_generic_frame(frame_current_tasks)

    # ==============================================
    # Section 11: Add Task Button
    # ==============================================

    # The Task Button that ensures the task form is shown
    task_button = ctk.CTkButton(
        master=frame_button,
        text="Add Task",
        text_color="white",  # Set text color to white
        # command=lambda: print("Add Task button clicked"),
        command=show_task_form, 
        fg_color="#DC7373",
        hover_color="#c4524e",
        width=360,
        height=55,
        corner_radius=20,
        font=("Helvetica", 16),
    )
    task_button.pack(side="bottom", anchor="s", pady=(0, 10))

    return frame_taskpage