# ==============================================
# Section 1: Data Preparation
# ==============================================

from pathlib import Path
from calendar import Calendar
from datetime import datetime, timedelta
from Tasks.TaskManager import TaskStatus, Task, Node
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import PhotoImage
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

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    Font = 'Helvetica'


    frame_controls = ttk.Frame(frame_taskpage, padding=0)
    frame_controls.pack(fill="x", padx=10, pady=(10, 5))

    frame_button = ttk.Frame(frame_taskpage, bootstyle="primary", padding=0)
    frame_button.pack(fill="x", padx=int(screen_height*0.0093), pady=(0, int(screen_height*0.0046)), side="bottom")

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

    frame_tasks = ttk.Frame(frame_taskpage, bootstyle="primary", padding=(0, 0, 0, 25))
    frame_tasks.pack(fill="both", expand=True)

    #frame_overlay = ttk.Frame(frame_taskpage, bootstyle="primary")
    #frame_overlay.place(relx=0.5, y=300, anchor="center", width=150)

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

        frame_task_form = ttk.Frame(frame_taskpage, bootstyle="primary")
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
            frame_button.pack(fill="x", padx=int(screen_height*0.0093), pady=(0, int(screen_height*0.0046)), side="bottom")

        def hide_task_form():
            frame_task_form.pack_forget()
            frame_tasks.pack(fill="both", expand=True)
            frame_button.pack(fill="x", padx=int(screen_height*0.0093), pady=(0, int(screen_height*0.0046)), side="bottom")

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
        fg_color="white",
    )
    frame_task_count.pack(side='top', anchor='w', pady=(0, 0), padx=(20, 0))

    # Create text for task count
    Task_Text = ctk.CTkLabel(
        master=frame_task_count,
        text="You completed",  # Title of task count
        font=(Font, 16),  # Font style and size
        fg_color="white",  # Background color
        text_color="#343a40" 
    )
    Task_Text.pack(side='top', anchor='w', pady=(10, 0), padx=(10, 0))

    # Create frame to hold task count number and text
    Tasks_Completed_Frame = ctk.CTkFrame(
        master=frame_task_count,
        bg_color="transparent",
        fg_color="white"
    )
    Tasks_Completed_Frame.pack(side='top', anchor='w', pady=(0, 0), padx=(10, 0))

    # Create task count number
    Tasks_Completed = ctk.CTkLabel(
        master=Tasks_Completed_Frame,
        # text=f"{somenumberhere}";  # Replace with actual number
        text="234",  # Replace with actual number
        bg_color="transparent",  # Background color
        fg_color="#ffffff",  # Foreground color
        font=(Font, 90),  # Font style and size
        anchor='w',  # Anchor position
        text_color="#343a40"  # Text color
    )
    Tasks_Completed.pack(side='left', anchor='sw')

    # Create text for "tasks"
    Tasks_Completed_Text = ctk.CTkLabel(
        master=Tasks_Completed_Frame,
        text="tasks",  # Text to display
        bg_color="transparent",  # Background color
        fg_color="#ffffff",  # Foreground color
        font=(Font, 25),
        anchor='w',  # Anchor position
        text_color="#343a40"  # Text color
    )
    Tasks_Completed_Text.pack(side='left', anchor='sw', pady=(0,15), padx=(5,0))

    # ==============================================
    # Section 7: Segmented Buttons AND Calendar
    # ==============================================

    # Code here that shows different frames of tasks groupings
    def calendar(option):
        print(f"Selected option: {option}")

    segmented_frame = ctk.CTkFrame(
        master=frame_tasks, 
        fg_color="white",
        bg_color="transparent"
    )
    segmented_frame.pack(fill="x", pady=10, padx=15, expand=YES)

    custom_font = ("Arial", 13,)  # Replace "Arial" with your desired font family

    # ==============================================
    # Week, Month, Day button functionality
    # ==============================================


    def update_task_frame(selected_option):
        current_view = None
        # Clear existing widgets in frame_current_tasks
        for widget in frame_current_tasks.winfo_children():
            widget.destroy()

        if selected_option == "Day":
            frame_current_tasks.pack(pady=(0, 5), padx=(12, 18), fill="both", expand=True)

            # Populate tasks or show generic message
            if nodes:
                for node in nodes:
                    create_node_frame(frame_current_tasks, node)
            else:
                create_generic_frame(frame_current_tasks)
        
        elif selected_option == "Week":
            frame_current_tasks.pack(pady=(0, 5), padx=(12, 18), fill="both", expand=True)
            show_week_view()
            toggle_calendar()

        elif selected_option == "Month":
            frame_current_tasks.pack(pady=(0, 5), padx=(12, 18), fill="both", expand=True)
            show_month_view()
            toggle_calendar()

    # ==============================================
    # Segment Buttons Update Logic
    # ==============================================

    def on_segmented_button_change(option):
        update_task_frame(option)

    button1 = ctk.CTkSegmentedButton(
        master=segmented_frame,
        corner_radius=200,
        height=40,
        border_width=0,
        fg_color="#f7f7f7",  # Default unselected background color
        font=custom_font,  # Use the defined font here
        text_color="#f7f7f7",  # Default unselected text color
        selected_hover_color="#cf5b58",  # Hover color when selected
        selected_color="#DC7373",  # Color when selected
        unselected_hover_color="#f7f7f7",  # Hover color when unselected
        unselected_color="#f7f7f7",  # Background color when unselected
        values=["Day", "Week", "Month"],  # Button options
        command=on_segmented_button_change  # Corrected here
    )


    button1.pack(fill="both", expand="yes")

    button1.set("Day")

    # ==============================================
    # Section 8: Scrollable current Tasks Frame
    # ==============================================

    def create_node_frame(frame, node):
        task_frame = ctk.CTkFrame(frame, fg_color="white", height=60, corner_radius=10)
        task_frame.pack(fill="x", padx=10, pady=5)
        task_label = ctk.CTkLabel(task_frame, text=node.task.name, font=("Arial", 12))
        task_label.pack(side="left", padx=10)
        deadline_label = ctk.CTkLabel(task_frame, text=f"Deadline: {node.task.deadline}", font=("Arial", 10))
        deadline_label.pack(side="left", padx=10)
        edit_button = ctk.CTkButton(task_frame, text="Edit", command=lambda: edit_task(node.task))
        edit_button.pack(side="right", padx=10)


    frame_current_tasks = ctk.CTkScrollableFrame(
        master=frame_tasks,
        bg_color="transparent",
        corner_radius=0,
        fg_color="#dcdfe7",
        height = 350,
        border_color="#FFFFFF",
        scrollbar_button_color="#dcdfe7",       # Default color of scrollbar button     
        scrollbar_button_hover_color="#555555"
    )
    # Initially hide the frame (it will only appear when "Day" is selected)
    frame_current_tasks.pack(pady=(0, 5), padx=(12, 18), fill="both", side="bottom", expand=YES)


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
            corner_radius=20,
            height=105
        )
        node_task.pack(pady=(8, 8), padx=(5, 5), fill=tk.X, side="top", expand=tk.YES)

        # Create a frame to hold task name and course tag horizontally
        title_frame = ctk.CTkFrame(
            master=node_task,
            fg_color="transparent"  # Make the frame transparent to blend with the parent
        )
        title_frame.pack(fill=tk.X, padx=(20, 20), pady=(10, 0))

        # Task name label
        ctk.CTkLabel(
            master=title_frame,
            text=node.task.name,
            text_color="black",
            font=("Arial", 16)
        ).pack(side="left", anchor="w")

        # Course tag label
        ctk.CTkLabel(
            master=title_frame,
            text=node.task.course_tag,
            text_color="gray",
            font=("Arial", 14)
        ).pack(side="right", anchor="w")

        # Text content label
        ctk.CTkLabel(
            master=node_task,
            text=node.task.text_content,
            text_color="gray",
            font=("Arial", 14),
            anchor="w"  # Align text content to the left
        ).pack(fill=tk.X, padx=(20, 20), pady=(5, 10))

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
        width=int(screen_height * 0.3333),
        height=int(screen_height * 0.0519),
        corner_radius=int(screen_height * 0.0185),
        font=("Helvetica", int(screen_height * 0.0148)),
    )
    task_button.pack(side="bottom", anchor="s", pady=int(screen_height * 0.0093))

    # ==============================================
    # Section 11: Hyas Code
    # ==============================================

    frame = None

    # ==============================================
    # Section 11.1: Calendar Widget Class
    # ==============================================

    class TkinterCalendar(Calendar):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tasks = {}
            
        def name_task(self, date, task_name, subject, color): 
            if date not in self.tasks:
                self.tasks[date] = []
            self.tasks[date].append({"name": task_name, "subject": subject, "color": color})

        def darken_color(hex_color, factor=0.45):
            hex_color = hex_color.lstrip("#")
            rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            darkened_rgb = tuple(max(0, int(c * factor)) for c in rgb)
            return "#{:02x}{:02x}{:02x}".format(*darkened_rgb)


        def formatmonth(self, master, year, month):
            dates = self.monthdatescalendar(year, month) #generates a list of weeks (with dates) for a given month.
            frame = ttk.Frame(master, bootstyle=PRIMARY)
            self.labels = []

            today = datetime.now().date()

            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            for c, weekday in enumerate(weekdays):
                ttk.Label(
                    frame,
                    text=weekday,
                    font=("Helvetica", 12, "bold"),
                    width=4,
                    anchor="center",
                    bootstyle=SECONDARY
                ).grid(row=0, column=c, padx=5, pady=(5,5))

            for r, week in enumerate(dates, start=1):
                labels_row = []
                for c, date in enumerate(week):
                    cell_frame = ttk.Frame(frame, width=50, height=50, bootstyle=PRIMARY)
                    cell_frame.grid(row=r, column=c, padx=5, pady=25)

                    label = ttk.Label(
                        cell_frame,
                        text=date.strftime('%d'),
                        font=("Helvetica", 9),
                        width=4,
                        anchor="center",
                        bootstyle=SECONDARY
                    )
                    label.pack()

                    # configuration of the days thats not in the current month
                    if date.month != month:
                        label.configure(foreground="#f2ebea")

                    # configuration of all the sundays for that month
                    if c == 6 and date.month == month:
                        label.configure(foreground="#cf5b58")

                    # configuration of the current day
                    if date == today:
                        label.configure(
                            font=("Helvetica", 9, "bold"),
                            foreground="#050505",
                            background="#efefef" #idk if this is ugly or not
                        )

                    if date in self.tasks:
                        task_frame = ttk.Frame(cell_frame, bootstyle=PRIMARY)
                        task_frame.pack(fill="both", expand=True)
                        max_tasks_per_row = 2 #task max per row sa date
                        base_task_width = 10
                        task_height = 5

                        num_tasks = len(self.tasks[date]) # Total number of tasks for the date

                        for i, task in enumerate(self.tasks[date]):
                            row = i // max_tasks_per_row
                            col = i % max_tasks_per_row

                            # this adjusts the width if there's only one task, making it wider
                            task_width = base_task_width * 2.5 if num_tasks == 1 else base_task_width

                            task_button = ctk.CTkButton(
                                master=task_frame,
                                text="",
                                fg_color=task["color"],
                                hover_color=task["color"], #just made it the same color because it doesnt really act as a button for users to click
                                width=task_width,
                                height=task_height,
                                corner_radius=1
                            )
                            task_button.grid(row=row, column=col, padx=2, pady=2)

                    labels_row.append(label)
                self.labels.append(labels_row)

            return frame

        def formatweek(self, master, year, month):
            today = datetime.now().date()

            week_dates = [self.current_week + timedelta(days=i) for i in range(7)] #shows the week header

            # main container to help with the scrollbars
            container = ctk.CTkFrame(master, fg_color="white", width=480, height=820)
            container.pack_propagate(False) #to make it consistent (rs)
            container.pack(fill="both", expand=True)

            #scrollable canvas
            canvas = ctk.CTkCanvas(container, bg="white", width=460, height=562)
            canvas.grid(row=0, column=0, sticky="nsew")

            # our vertical scrollbar
            v_scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
            v_scrollbar.grid(row=0, column=1, sticky="ns")

            # our horizontal scrollbar
            h_scrollbar = ctk.CTkScrollbar(container, orientation="horizontal", command=canvas.xview)
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            # Configure the canvas for scrolling
            canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

            # Frame inside the canvas
            week_frame = ttk.Frame(canvas, bootstyle=PRIMARY)
            canvas.create_window((0, 0), window=week_frame, anchor="nw")

            # days of the week layout
            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

            for c, (weekday, date) in enumerate(zip(weekdays, week_dates)):
                cell_frame = ttk.Frame(week_frame, bootstyle=PRIMARY)
                cell_frame.grid(row=0, column=c, padx=10, pady=0, sticky="nsew")

                header_label = ttk.Label(
                    cell_frame,
                    text=f"{date.strftime('%d %b')}\n{weekday}",
                    font=("Helvetica", 10, "bold"),
                    justify="center",
                    anchor="center",
                    bootstyle=SECONDARY,
                )
                header_label.pack()

                # Task frame inside each date cell
                task_frame = ttk.Frame(cell_frame, bootstyle=PRIMARY)
                task_frame.pack(fill="both", expand=True)

                if date == today:
                    header_label.configure(
                        font=("Helvetica", 10, "bold"),
                        foreground="#050505",
                    )

                if date in self.tasks:
                    max_tasks_per_row = 1
                    base_task_width = 60
                    task_height = 40

                    for i, task in enumerate(self.tasks[date]):
                        row = i // max_tasks_per_row
                        col = i % max_tasks_per_row

                        task_width = base_task_width * 2.5

                        task_button = ctk.CTkFrame(
                            master=task_frame,
                            fg_color=task["color"],
                            corner_radius=5,
                            width=task_width,
                            height=task_height,
                        )
                        task_button.grid(row=row, column=col, padx=2, pady=5)

                        #label: title of the task
                        name_label = ctk.CTkLabel(
                            master=task_button,
                            text=task.get("name"),
                            font=("Helvetica", 14, "bold"),
                            text_color=TkinterCalendar.darken_color(task["color"]),
                        )
                        name_label.pack(side="top", anchor="center", padx=15, pady=(2, 0))

                        #label: subject name
                        subject_label = ctk.CTkLabel(
                            master=task_button,
                            text=task.get("subject"),
                            font=("Helvetica", 11),
                            text_color=TkinterCalendar.darken_color(task["color"]),
                        )
                        subject_label.pack(side="bottom", anchor="center", padx=15, pady=(0, 2))

            # Update scroll region
            week_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            return container
        
    current_year = datetime.now().year
    current_month = datetime.now().month
    tkcalendar = TkinterCalendar()
    frame = tkcalendar.formatmonth(frame_current_tasks, current_year, current_month)
    frame.pack_forget()


    def update_month_calendar():
        global frame, current_year, current_month
        header.configure(text=f"{datetime(current_year, current_month, 1):%B %Y}")
        frame = tkcalendar.formatmonth(frame_current_tasks, current_year, current_month)
        frame.pack(pady=20)

    def update_week_calendar():
        global frame
        if not tkcalendar.current_week:
            tkcalendar.current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
        week_number = tkcalendar.current_week.isocalendar()[1]  
        year = tkcalendar.current_week.year
        header.configure(text=f"Week {week_number} - {year}")
        frame = tkcalendar.formatweek(frame_current_tasks, tkcalendar.current_week.year, tkcalendar.current_week.month)
        frame.pack(pady=20)

    def prev_month():
        global current_year, current_month
        current_month -= 1
        if current_month == 0:
            current_month = 12
            current_year -= 1
        update_month_calendar()

    def next_month():
        global current_year, current_month
        current_month += 1
        if current_month == 13:
            current_month = 1
            current_year += 1
        update_month_calendar()

    def prev_week():
        if tkcalendar.current_week:
            tkcalendar.current_week -= timedelta(weeks=1)
        else:
            tkcalendar.current_week = datetime.now().date() - timedelta(weeks=1)
        update_week_calendar()

    def next_week():
        if tkcalendar.current_week:
            tkcalendar.current_week += timedelta(weeks=1)
        else:
            tkcalendar.current_week = datetime.now().date() + timedelta(weeks=1)
        update_week_calendar()

    current_view = None

    def show_month_view():
        global current_view, frame
        current_view = "month"
        current_year = datetime.now().year
        current_month = datetime.now().month  # Reset to curret when we switch
        frame = tkcalendar.formatmonth(frame_current_tasks, current_year, current_month)
        frame.pack(pady=20)
        update_navigation_buttons()  # Update navigation buttons so that it knows what to switch
        header.configure(text=f"{datetime(current_year, current_month, 1):%B %Y}") # refreshes to the current month
        color_view()


    def show_week_view():
        global current_view, frame
        current_view = "week"
        tkcalendar.current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())  # Refreshes the week calendar with the current week
        frame = tkcalendar.formatweek(frame_current_tasks, current_year, current_month)
        frame.pack(pady=20)
        update_navigation_buttons() 
        update_week_calendar() 
        color_view()

    #so depending on what view we are in, it uses that button
    def update_navigation_buttons():
        if current_view == "month":
            button_prev.configure(command=prev_month)
            button_next.configure(command=next_month)
        elif current_view == "week":
            button_prev.configure(command=prev_week)
            button_next.configure(command=next_week)

    #this is for the header and prev & next buttons
    frame_header = ttk.Frame(frame_current_tasks, bootstyle="primary", padding=5)
    frame_header.pack(fill="x", padx=10, pady=(10,0))

    button_prev = ttk.Button(
        frame_header,
        text="◄",
        command=prev_month,
        bootstyle="danger-outline"
    )
    button_prev.pack(side="left", padx=10)

    header = ttk.Label(
        frame_header,
        text=f"{datetime.now():%B %Y}",
        font=("Helvetica", 18, "bold"),
        bootstyle="DANGER"
    )
    header.pack(side="left", padx=10, expand=True)

    button_next = ttk.Button(
        frame_header,
        text="►",
        command=next_month,
        bootstyle="danger-outline"
    )
    button_next.pack(side="right", padx=10)


    # Sample tasks with descriptions for week view
    tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700")
    tkcalendar.name_task(datetime(2024, 11, 26).date(), "Examination", "CMSC 130", "#DC7373")
    tkcalendar.name_task(datetime(2024, 11, 27).date(), "Evaluation", "Ethics", "#90EE90")

    def toggle_calendar():
        """Toggle the visibility of the calendar frame."""
        global frame  # Declare frame as global
        if frame and frame.winfo_ismapped():  # If the frame is currently displayed
            frame.pack_forget()  # Hide the frame
        else:
            # Show the calendar based on the current view
            if current_view == "month":
                update_month_calendar()
            elif current_view == "week":
                update_week_calendar()


    return frame_taskpage