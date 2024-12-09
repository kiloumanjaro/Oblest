# ==============================================
# Section 1: Data Preparation
# ==============================================
from pathlib import Path
from calendar import Calendar
from datetime import datetime, timedelta
from Tasks.TaskManager import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import PhotoImage
from tkinter import simpledialog, scrolledtext
from datetime import datetime
from loadingOverlay import *

# import list
# import calendar

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

all_tasks = TaskManager()

# Uncomment this following function if wanting to reindex tasks
# all_tasks.reindex_task_ids()


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
    frame_controls.pack(fill="x", padx=10, pady=(10, 5), side="top")

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
    # Section 2.1: Archives Code
    # ==============================================


    def create_archives_page(app):
        left_button_state = BooleanVar(value=False)
        right_button_state = BooleanVar(value=False)
        
        try:
            right_icon = ttk.PhotoImage(file=str(relative_to_assets("right_icon.png")))
            left_icon = ttk.PhotoImage(file=str(relative_to_assets("left_icon.png")))
            right_icon_active = ttk.PhotoImage(file=str(relative_to_assets("right_icon_active.png")))
            left_icon_active = ttk.PhotoImage(file=str(relative_to_assets("left_icon_active.png")))
        except Exception as e:
            print(f"Error loading icons: {e}")
            return None
        
        frame_archives = ttk.Frame(app)

        frame_controls = ttk.Frame(frame_archives, bootstyle="success", padding=0)
        frame_controls.pack(fill="x", padx=10, pady=(10, 5))

        def toggle_right_button():
            frame_archives.pack_forget()  # Hide archives page
            frame_taskpage.pack(fill="both", expand=True)  # Show tasks page
            if right_button_state.get():
                right_button_state.set(False)
                button_right.configure(image=right_icon)
            else:
                right_button_state.set(True)
                button_right.configure(image=right_icon_active)

        def toggle_left_button():
            if left_button_state.get():
                left_button_state.set(False)
                button_left.configure(image=left_icon)
            else:
                left_button_state.set(True)
                button_left.configure(image=left_icon_active)

        button_left = ttk.Button(
            frame_controls,
            text="",
            image=left_icon,
            command=toggle_left_button,
            bootstyle="secondary, link"
        )
        button_left.pack(side="left", padx=0, anchor="w")

        button_right = ttk.Button(
            frame_controls,
            text="",
            image=right_icon,
            command=toggle_right_button,
            bootstyle="primary, link",
            width=4
        )
        button_right.pack(side="right", padx=0, anchor="e")

        return frame_archives
    
    frame_archives = create_archives_page(app)
    frame_archives.pack_forget() 

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
    frame_tasks.pack(fill="both", pady=0, expand=True)

    tasks_top = ttk.Frame(frame_tasks, bootstyle="primary", padding=0)
    tasks_top.pack(fill="both", expand="yes", padx=0, pady=0, side="top")

    tasks_middle = ttk.Frame(frame_tasks, bootstyle="primary", padding=0)
    tasks_middle.pack(fill="both", expand="yes", padx=0, pady=0, side="top")

    tasks_bottom = ttk.Frame(frame_tasks, bootstyle="dark", padding=0)
    tasks_bottom.pack(fill="both", expand="yes", padx=20, pady=0, side="top")
 
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
        frame_taskpage.pack_forget()  # Hide tasks page
        frame_archives.pack(fill="both", expand=True)
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
    # Section 5: Task Form Functions and Creation (Modified)
    # ==============================================

    def refresh_task_list(course_option, given_deadline):
        print("Refreshing task list...")
        toggle_switcher("Day", default=True)
        all_tasks.courses[course_option].update_priorities(given_deadline)

    def show_task_form():
        global all_tasks  # Ensure we're using the global TaskManager instance

        frame_tasks.pack_forget()
        frame_button.pack_forget()

        frame_task_form = ttk.Frame(frame_taskpage, bootstyle="primary")
        frame_task_form.pack(fill="both", expand=True)

        # ----------------------------------------------
        # 5.2: Form Field Creation (Modified)
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

        # Course Selection Field (Modified)
        ttk.Label(frame_task_form, text="Course:", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # Dynamically get courses from TaskManager
        courses = all_tasks.get_courses()
        if not courses:
            courses = ["general"]  # Default to "general" if no courses exist

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
        course_dropdown.pack(pady=10)

        # Content Field
        ttk.Label(frame_task_form, text="Content:").pack(pady=10)
        content_text = scrolledtext.ScrolledText(frame_task_form, width=50, height=10)
        content_text.pack(pady=10)

        # ----------------------------------------------
        # 5.3: Form Action Functions (Modified)
        # ----------------------------------------------

        def submit_task_form():
            global all_tasks

            task_title = task_title_entry.get()
            deadline_date_str = deadline_date_entry.entry.get()
            course = course_var.get()
            content = content_text.get("1.0", "end-1c")

            # Validate deadline date
            try:
                if deadline_date_str:  # Only parse if a date is entered
                    deadline_date = datetime.strptime(deadline_date_str, "%Y-%m-%d")
                else:
                    deadline_date = None
            except ValueError:
                simpledialog.messagebox.showerror(
                    "Invalid Date",
                    "Please enter a valid date in the format YYYY-MM-DD."
                )
                return

            # --- COURSE EXISTENCE CHECK WITH CONFIRMATION ---
            if course not in all_tasks.get_courses():
                if not simpledialog.messagebox.askyesno(
                    "Course Not Found",
                    f"The course '{course}' does not exist. Do you want to create it?"
                ):
                    # User chose not to create the course, so return to the form
                    return

                # User chose to create the course
                try:
                    all_tasks.add_course(course)
                    course_dropdown.configure(values=all_tasks.get_courses()) # Update dropdown values
                    course_var.set(course) # Set the new course as selected
                except ValueError as e:
                    simpledialog.messagebox.showerror("Error Creating Course", str(e))
                    return
            # --- END OF COURSE CHECK ---

            # Prepare task data dictionary
            task_data = {
                'name': task_title,
                'deadline': deadline_date_str,
                'course_tag': course,
                'text_content': content,
                'initial_date': datetime.today().strftime('%Y-%m-%d'),  # Format as string
                'status': TaskStatus.NOT_DONE,
            }

            # Add task using TaskManager
            try:
                all_tasks.add_task(course, task_data)
            except ValueError as e:
                simpledialog.messagebox.showerror("Error Adding Task", str(e))
                return

            refresh_task_list(course, deadline_date)

            # Hide the form and show the task list/buttons
            frame_task_form.pack_forget()
            frame_tasks.pack(fill="both", expand=True)
            frame_button.pack(fill="x", padx=int(screen_height * 0.0093), pady=(0, int(screen_height * 0.0046)), side="bottom")

        def hide_task_form():
            frame_task_form.pack_forget()
            frame_tasks.pack(fill="both", expand=True)
            frame_button.pack(fill="x", padx=int(screen_height * 0.0093), pady=(0, int(screen_height * 0.0046)), side="bottom")

        # ----------------------------------------------
        # 5.4: Button Creation and Layout (No Changes)
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
        master=tasks_top,
        bg_color="transparent",
        fg_color="white",
    )
    frame_task_count.pack(side='top', anchor='w', pady=(0, 0), padx=(20, 0))

    # Create text for task count
    Task_Text = ctk.CTkLabel(
        master=frame_task_count,
        text="You completed",  # Title of task count
        font=(Font, 15),  # Font style and size
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

        # Will Utilize the totals obtained from each Course Skipl List
        ###########################################################
        # text=f"{somenumberhere}";  # Replace with actual number #
        ###########################################################
        text="234",  # Replace with actual number
        bg_color="transparent",  # Background color
        fg_color="#ffffff",  # Foreground color
        font=(Font, 85),  # Font style and size
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
        font=(Font, 20),
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
        master=tasks_top, 
        fg_color="white",
        bg_color="transparent"
    )
    segmented_frame.pack(fill="x", pady=(10, 0), padx=15,)

    custom_font = ("Arial", 13,)  # Replace "Arial" with your desired font family


    # ==============================================
    # Section 8: Tasks Display: Day, Week, Month
    # ==============================================

    frame_current_tasks = ctk.CTkScrollableFrame(
        master=tasks_bottom,
        bg_color="transparent",
        corner_radius=0,
        fg_color="#dcdfe7",
        height = 350,
        border_color="#FFFFFF",
        scrollbar_button_color="#dcdfe7",       # Default color of scrollbar button     
        scrollbar_button_hover_color="#555555"
    )
    # Initially hide the frame (it will only appear when "Day" is selected)
    frame_current_tasks.pack(pady=0, padx=(12, 18), fill="both", side="bottom", expand=YES)

    original_scrollbar_grid_info = frame_current_tasks._scrollbar.grid_info()

    def toggle_scrollbar(enable):
        if enable:
            # Restore the scrollbar to its original position
            frame_current_tasks._scrollbar.grid(**original_scrollbar_grid_info)
        else:
            # Hide the scrollbar
            frame_current_tasks._scrollbar.grid_forget()

    # ----------------------------------------------
    # Helper Functions: Gets tasks for day, week, month
    # ----------------------------------------------
   
    def get_tasks_for_day(tasks: list[Task], selected_date: datetime) -> list[Task]:
        relevant_tasks = []
        for task in tasks:
            target_day = task.deadline.date()
            if target_day == selected_date:
                relevant_tasks.append(task)
        return relevant_tasks
    
    def get_tasks_for_week(tasks: list[Task], start_of_week: datetime) -> list[Task]:
        end_of_week = start_of_week + timedelta(days=6)
        relevant_tasks = []
        for task in tasks:
            start = task.initial_date.date()
            end = task.deadline.date() if task.deadline else start
            if start <= end_of_week and end >= start_of_week:
                relevant_tasks.append(task)
        return relevant_tasks
    
    def get_tasks_for_month(tasks: list[Task], year: int, month: int) -> list[Task]:
        # Calculate start and end of the month
        start_of_month = datetime(year, month, 1)
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_of_month = datetime(year, month + 1, 1) - timedelta(days=1)

        relevant_tasks = []
        for task in tasks:
            start = task.initial_date.date()
            end = task.deadline.date() if task.deadline else start
            if start <= end_of_month and end >= start_of_month:
                relevant_tasks.append(task)
        return relevant_tasks

    # ----------------------------------------------
    # Week, Month, Day button functionality
    # ----------------------------------------------

    def create_switcher():
        return ctk.CTkFrame(
            master=tasks_middle,
            fg_color="white",
            height=20
        )

    switcher = create_switcher()
    switcher.pack(pady=(0, 0), padx=(0, 0), fill="both", side="top", expand=False)

    def toggle_switcher(option, default=True, date_offset=0):
        """
        Handles switching between Day, Week, and Month views, including UI updates and button setup.
        """

        # Clear existing widgets in frame_current_tasks
        for widget in frame_current_tasks.winfo_children():
            widget.destroy()

        # Pack the frame_current_tasks (only if not already packed)
        if not frame_current_tasks.winfo_ismapped():
            frame_current_tasks.pack(pady=(0, 0), padx=(0, 0), fill="both", expand=True)
        
        # Dictionary to map options to functions
        options = {
            "Day": show_day_view, 
            "Week": show_week_view_option,    
            "Month": show_month_view_option,  
        }

        # This will determine how far forward or backward the switcher will be relative to the given date
        # depending on the date type
        
        func = options.get(option)
        current_offset = date_offset
                
        date_display = None

        if default:
            # For default view, use the respective function with default parameters
            if func:
                if option == "Day":
                    func()  # Call show_day_view with no offset (today)
                    date_display = datetime.now().date().strftime("%Y-%m-%d")
                elif option == "Week":
                    func()
                    # Calculate week number (e.g., "Week 47")
                    week_number = datetime.now().date().isocalendar()[1]
                    date_display = f"Week {week_number}"
                elif option == "Month":
                    func()
                    # Get current month name (e.g., "November")
                    date_display = datetime.now().date().strftime("%B")
        else:
            # For non-default view (previous/next), pass the date_offset
            if func:
                if option == "Day":
                    func(date_offset=date_offset)  # Pass date_offset to show_day_view
                    target_date = datetime.now().date() + timedelta(days=date_offset)
                    date_display = target_date.strftime("%Y-%m-%d")
                elif option == "Week":
                    func()  # Week view function doesn't use date_offset directly
                    # Calculate week number based on offset (this is more complex)
                    target_week = datetime.now().date() + timedelta(weeks=date_offset)
                    week_number = target_week.isocalendar()[1]
                    date_display = f"Week {week_number}"
                elif option == "Month":
                    func()  # Month view function doesn't use date_offset directly
                    # Calculate month based on offset (also more complex)
                    target_month = datetime.now().date() + timedelta(days=date_offset * 30)  # Approximation!
                    date_display = target_month.strftime("%B")

            

        # Configure the grid to expand and center the widgets (for switcher)
        switcher.grid_columnconfigure(0, weight=0)
        switcher.grid_columnconfigure(1, weight=1)
        switcher.grid_columnconfigure(2, weight=1)
        switcher.grid_columnconfigure(3, weight=0)
        switcher.grid_rowconfigure(0, weight=1)

        def previous_of():
            toggle_switcher(option, default=False, date_offset= current_offset - 1)
            

        def next_of():
            toggle_switcher(option, default=False, date_offset= current_offset + 1)
            
        

        # Create Previous button
        previous = ctk.CTkButton(
            master=switcher,
            corner_radius=200,
            width=100,
            text="Previous",
            text_color="brown",
            fg_color="#f7f7f7",
            hover_color="#cf5b58",
            height=30,
            command=previous_of  # Link to your previous_of function
        )
        previous.grid(row=0, column=0, padx=20, pady=5)

        # Create Date State Label
        datestate = ctk.CTkLabel(
            master=switcher,
            text=date_display,
            text_color="black",
            wraplength=400,
        )
        datestate.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Create Next button
        next = ctk.CTkButton(
            master=switcher,
            corner_radius=200,
            width=100,
            text="Next",
            text_color="brown",
            fg_color="#f7f7f7",
            hover_color="#cf5b58",
            height=30,
            command=next_of  # Link to your next_of function
        )
        next.grid(row=0, column=3, padx=20, pady=5)

    def show_day_view(given_date:datetime = datetime.now().date(), date_offset: int = 0):
        # Populate tasks or show generic message
        toggle_scrollbar(True) 
        target_date = datetime.now().date() + timedelta(days=date_offset)
        print(f"Target Date: {target_date}")

        if date_offset != 0:
            tasks = get_tasks_for_day(all_tasks.get_all_tasks(), target_date)
        elif given_date:
            tasks = get_tasks_for_day(all_tasks.get_all_tasks(), given_date)

        # Safely check for 'general' key
        if all_tasks.courses.get("general"):
            print(all_tasks.courses["general"].task_amount())
            print(datetime.now())
        else:
            print("Key 'general' is missing or has no tasks.")

        if tasks:
            for task in tasks:
                create_task_frame(frame_current_tasks, task)
        else:
            create_generic_frame(frame_current_tasks)
            
    # def show_day_view_option():
    #     populate_day_view()

    def show_week_view_option(given_date:datetime = datetime.now().date(), date_offset: int = 0):
        toggle_scrollbar(False)
        # Show week view and toggle calendar
        show_week_view()
        toggle_calendar()

    def show_month_view_option(given_date:datetime = datetime.now().date(), date_offset: int = 0):
        # Show month view and toggle calendar
        toggle_scrollbar(False)
        show_month_view()
        toggle_calendar()

    # ----------------------------------------------
    # Segment Buttons Update Logic
    # ----------------------------------------------

    def on_segmented_button_change(option):
        toggle_switcher(option, default=True)

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
    # Section 9: Task Nodes and Frame Creation
    # ==============================================

    # ----------------------------------------------
    # 9.1: Sample Data and Node Creation
    # ----------------------------------------------
    # Sample task list creation

    tasks = [
        Task(
            id=1,
            name="Task 1",
            priority=5,
            text_content="Task 1 content",
            course_tag="Course 1",
            difficulty_rating=3,
            initial_date=datetime.strptime("2022-01-01", '%Y-%m-%d'),
            deadline=datetime.strptime("2022-01-15", '%Y-%m-%d')
        ),
        Task(
            id=2,
            name="Task 2",
            priority=3,
            text_content="Task 2 content",
            course_tag="Course 2",
            difficulty_rating=2,
            initial_date=datetime.strptime("2022-01-05", '%Y-%m-%d')
        ),
        Task(
            id=3,
            name="Task 3",
            priority=8,
            text_content="Task 3 content",
            course_tag="Super Cool Course",
            difficulty_rating=4,
            initial_date=datetime.strptime("2022-01-10", '%Y-%m-%d'),
            deadline=datetime.strptime("2022-01-20", '%Y-%m-%d')
        ),
        Task(
            id=4,
            name="Task 4",
            priority=6,
            text_content="Task 4 content",
            difficulty_rating=3,
            initial_date=datetime.strptime("2022-01-15", '%Y-%m-%d'),
            deadline=datetime.strptime("2022-01-25", '%Y-%m-%d')
        ),
        Task(
            id=5,
            name="Task 5",
            priority=6,
            text_content="Task 4 content But Perhaps",
            course_tag="Course 4",
            difficulty_rating=3,
            initial_date=datetime.strptime("2022-01-15", '%Y-%m-%d'),
            deadline=datetime.strptime("2022-01-25", '%Y-%m-%d')
        ),
        Task(
            id=6,
            name="Task 6",
            priority=6,
            text_content="Task 4 content But Awesome",
            course_tag="Course 4",
            difficulty_rating=3,
            initial_date=datetime.strptime("2022-01-15", '%Y-%m-%d'),
            deadline=datetime.strptime("2022-01-25", '%Y-%m-%d')
        ),
    ]

    # Node list generation from tasks
    # nodes = [Node(task, 1) for task in tasks]
    
    # The following mini section is for retrieval of tasks depending on the selected view
    # These functions must be called by their respective date functions
    
    # ----------------------------------------------
    # 9.2: Generic Frame Generation
    # ----------------------------------------------
    
    def create_generic_frame(master):
        course_color = "white"  # Default color for generic frame

        generic_task = ctk.CTkFrame(
            master=master,
            fg_color=course_color,
            corner_radius=20,
            height=105
        )
        generic_task.pack(pady=(8, 8), padx=(22, 5), fill=tk.X, side="top", expand=tk.YES)

        # Create a frame to hold generic message horizontally
        title_frame = ctk.CTkFrame(
            master=generic_task,
            fg_color="transparent"  # Make the frame transparent to blend with the parent
        )
        title_frame.pack(fill=tk.X, padx=(20, 20), pady=(10, 10))

        # Create a grid layout for the title frame
        title_frame.grid_columnconfigure(0, weight=1)

        # Generic message label
        ctk.CTkLabel(
            master=title_frame,
            text="No tasks available",
            text_color="gray",
            font=("Arial", 16)
        ).grid(row=0, column=0, sticky="nsew")
        title_frame.grid_rowconfigure(0, weight=1)
        
    # ----------------------------------------------
    # 9.3: Node Frame Generation
    # ----------------------------------------------

    def create_task_frame(master, task):
        course_color = {
            "Course 1": "#FFC080",  # Orange
            "Course 2": "#C5CAE9",  # Blue
            # Add more course colors as needed
        }

        task_frame = ctk.CTkFrame(
            master=master,
            fg_color=course_color.get(task.course_tag, "white"),
            corner_radius=20,
            height=20
        )
        task_frame.pack(pady=(8, 8), padx=(22, 5), fill=tk.X, side="top", expand=tk.YES)

        # Create a frame to hold task name and course tag horizontally
        title_frame = ctk.CTkFrame(
            master=task_frame,
            fg_color="transparent"  # Make the frame transparent to blend with the parent
        )
        title_frame.pack(fill=tk.X, padx=(10, 20), pady=(10, 10))

        # Create a grid layout for the title frame
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=1)

        # Task name label
        ctk.CTkButton(
            master=title_frame,
            corner_radius=100,
            text=task.name,
            fg_color="white",
            bg_color="white",
            width=20,
            text_color="black",
            font=("Arial", 16),
            hover_color="#f7f7f7",
            anchor="w",
            # command=lambda: somefunction(task)
        ).grid(row=0, column=0, sticky="w")

    # Course tag button
        course_button = ctk.CTkButton(
            master=title_frame,
            text=task.course_tag,
            fg_color=all_tasks.get_course_color(task.course_tag),  # Button background color
            hover_color=all_tasks.get_course_color(task.course_tag),  # Same color for hover
            text_color="white",
            font=("Arial", 14),
            command=lambda: None,  # Replace with your desired action
            width=10,
            corner_radius=50
        )
        course_button.grid(row=0, column=1, sticky="e")


        # Text content label
        text_content_label = ctk.CTkLabel(
            master=title_frame,
            text=task.text_content,
            text_color="gray",
            font=("Arial", 14),
            anchor="w"  # Align text content to the left
        )
        text_content_label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(10,0))
        title_frame.grid_rowconfigure(1, weight=1)
        
        # Edit button (three dots)
        edit_button = ctk.CTkButton(
            master=task_frame,
            corner_radius=100,  
            fg_color="white",
            bg_color="white",
            hover_color="#f7f7f7",
            text_color="gray",
            text="...",
            width=20,  # Adjust width as needed
            height=20,
            font=("Arial", 10),
            command=lambda: edit_task(task)  # Empty command for now
        )
        # Place at bottom-right corner, accounting for padding/margins
        edit_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
            
    # ----------------------------------------------
    # 9.4: Frame Creation Logic | SHOWS UP BY DEFAULT AT START OF PROGRAM
    # ----------------------------------------------
    
    toggle_switcher("Day", default=True)

    # ==============================================
    # Section 9.5: Edit Task Functionality (NEW)
    # ==============================================
    
    def edit_task(task: Task):
        """
        Opens a form to edit an existing task.
        """
        frame_tasks.pack_forget()
        frame_button.pack_forget()

        frame_edit_task = ttk.Frame(frame_taskpage, bootstyle="primary")
        frame_edit_task.pack(fill="both", expand=True)

        # ----------------------------------------------
        # 9.5.1: Form Field Creation
        # ----------------------------------------------
        # Task Title Field
        ttk.Label(frame_edit_task, text="Task Title:").pack(pady=10)
        task_title_entry = ttk.Entry(frame_edit_task, width=50)
        task_title_entry.insert(0, task.name)  # Pre-fill with existing title
        task_title_entry.pack(pady=10)

        # Deadline Date Field
        ttk.Label(frame_edit_task, text="Deadline Date:").pack(pady=10)
        deadline_date_entry = ttk.DateEntry(
            master=frame_edit_task,
            bootstyle="danger",
            dateformat="%Y-%m-%d"
        )
        if task.deadline:
            deadline_date_entry._startdate = task.deadline  # Pre-fill with existing deadline
        deadline_date_entry.pack(pady=10)
        
        # Status Field
        ttk.Label(frame_edit_task, text="Status:").pack(pady=10)
        status_var = tk.StringVar()
        status_var.set(task.status.value)  # Set initial value to task's current status
        status_options = [status.value for status in TaskStatus][:2]
        status_dropdown = ctk.CTkComboBox(
            master=frame_edit_task,
            corner_radius=20,
            text_color="white",
            fg_color="#cf5b58",
            values=status_options,
            variable=status_var,
            button_color="#cf5b58",
            button_hover_color="#c4524e",
            dropdown_fg_color="#cf5b58",
            dropdown_hover_color="#c4524e",
            border_color="#cf5b58",
        )
        status_dropdown.pack(pady=10)

        # Course Selection Field
        ttk.Label(frame_edit_task, text="Course:", font=('Helvetica', 14, 'bold')).pack(pady=10)
        courses = all_tasks.get_courses()
        if not courses:
            courses = ["general"]
        course_var = tk.StringVar()
        course_var.set(task.course_tag)  # Pre-select the task's current course
        course_dropdown = ctk.CTkComboBox(
            master=frame_edit_task,
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
        course_dropdown.pack(pady=10)

        # Content Field
        ttk.Label(frame_edit_task, text="Content:").pack(pady=10)
        content_text = scrolledtext.ScrolledText(frame_edit_task, width=50, height=10)
        content_text.insert("1.0", task.text_content)  # Pre-fill with existing content
        content_text.pack(pady=10)

        # ----------------------------------------------
        # 9.5.2: Form Action Functions
        # ----------------------------------------------

        def update_task():
            """
            Updates the task with the new values from the form.
            """
            nonlocal task  # Access the task variable from the outer scope

            # Get updated values from form fields
            new_title = task_title_entry.get()
            new_deadline_str = deadline_date_entry.entry.get()
            new_course = course_var.get()
            new_content = content_text.get("1.0", "end-1c")
            new_status_str = status_var.get()

            # Validate deadline date
            try:
                if new_deadline_str:
                    new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
                else:
                    new_deadline = None
            except ValueError:
                simpledialog.messagebox.showerror(
                    "Invalid Date",
                    "Please enter a valid date in the format YYYY-MM-DD."
                )
                return

            # Convert status string back to TaskStatus enum
            try:
                new_status = TaskStatus(new_status_str)
            except ValueError:
                simpledialog.messagebox.showerror("Invalid Status", "Please select a valid status.")
                return

            # --- COURSE EXISTENCE CHECK ---
            while new_course not in all_tasks.get_courses():
                simpledialog.messagebox.showerror(
                    "Invalid Course",
                    f"The course '{new_course}' does not exist. Please select a valid course from the dropdown."
                )
                # Re-display the edit form to allow the user to select a valid course
                # You might need to adjust how you re-display the form based on your UI structure
                # For example, if you have a separate function to show the edit form:
                # show_edit_form(task)  
                # Or, you can simply return here, assuming the form will remain visible:
                return
            # --- END OF COURSE EXISTENCE CHECK ---

            # Store old course tag to help with moving task between courses
            old_course = task.course_tag

            # Update task properties
            task.name = new_title
            task.deadline = new_deadline
            task.course_tag = new_course
            task.text_content = new_content
            task.status = new_status

            # Update the task in the TaskManager (handling potential course change)
            try:
                if old_course != new_course:
                    # Move the task to the new course
                    all_tasks.move_task(task.id, old_course, new_course)
                else:
                    # Update the task in the current course
                    all_tasks.courses[new_course].update_task(task)

                # Handle status change - mark as complete/incomplete if needed
                if new_status == TaskStatus.DONE:
                    all_tasks.courses[new_course].mark_task_complete(task.id)
                elif new_status == TaskStatus.NOT_DONE and task.status != TaskStatus.NOT_DONE:
                    all_tasks.courses[new_course].mark_task_incomplete(task.id)

            except ValueError as e:
                simpledialog.messagebox.showerror("Error Updating Task", str(e))
                return

            # Refresh task list display
            refresh_task_list(new_course, new_deadline)

            # Hide the edit form and show the task list/buttons
            frame_edit_task.pack_forget()
            frame_tasks.pack(fill="both", expand=True)
            frame_button.pack(fill="x", padx=int(screen_height * 0.0093), pady=(0, int(screen_height * 0.0046)), side="bottom")

        def cancel_edit():
            """
            Cancels the edit operation and returns to the task list.
            """
            frame_edit_task.pack_forget()
            frame_tasks.pack(fill="both", expand=True)
            frame_button.pack(fill="x", padx=int(screen_height * 0.0093), pady=(0, int(screen_height * 0.0046)), side="bottom")

        # ----------------------------------------------
        # 9.5.3: Button Creation and Layout
        # ----------------------------------------------
        button_frame = ctk.CTkFrame(
            master=frame_edit_task,
            fg_color="#f8f9fa",
        )
        button_frame.pack(pady=10)

        ctk.CTkButton(
            master=button_frame,
            text="Update",
            font=('Helvetica', 14),
            text_color="white",
            command=update_task,
            corner_radius=20,
            fg_color="#cf5b58",
            hover_color="#c4524e"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            master=button_frame,
            text="Cancel",
            font=('Helvetica', 14),
            text_color="white",
            command=cancel_edit,
            corner_radius=20,
            fg_color="#cf5b58",
            hover_color="#c4524e"
        ).pack(side="left", padx=10)

    # ==============================================
    # Section 10: Add Task Button
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
    # Section 12: Hyas Code
    # ==============================================

    frame = None

    # ==============================================
    # Section 12.1: Calendar Widget Class
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
            # Check if the frame exists and destroy it if necessary
            if hasattr(self, 'frame') and self.frame.winfo_exists():
                self.frame.destroy()

            dates = self.monthdatescalendar(year, month)
            self.frame = ttk.Frame(master, bootstyle=PRIMARY)
            self.labels = []

            today = datetime.now().date()

            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            for c, weekday in enumerate(weekdays):
                ttk.Label(
                    self.frame,
                    text=weekday,
                    font=("Helvetica", 10, "bold"),
                    width=4,
                    anchor="center",
                    bootstyle=SECONDARY
                ).grid(row=0, column=c, padx=5, pady=(5, 5))

            # Configure columns to expand
            for c in range(7):
                self.frame.grid_columnconfigure(c, weight=1, uniform="equal")

            for r, week in enumerate(dates, start=1):
                labels_row = []
                for c, date in enumerate(week):
                    cell_frame = ttk.Frame(self.frame, width=14, height=14  , bootstyle=PRIMARY)
                    cell_frame.grid(row=r, column=c, padx=1, pady=10, sticky="nsew")

                    label = ttk.Label(
                        cell_frame,
                        text=date.strftime('%d'),
                        font=("Helvetica", 9),
                        width=4,
                        anchor="center",
                        bootstyle=SECONDARY
                    )
                    label.pack(expand=True, fill="both")

                    # Configuration for days not in the current month
                    if date.month != month:
                        label.configure(foreground="#f2ebea")

                    # Configuration for Sundays
                    if c == 6 and date.month == month:
                        label.configure(foreground="#cf5b58")

                    # Highlight current day
                    if date == today:
                        label.configure(
                            font=("Helvetica", 9, "bold"),
                            foreground="#050505",
                            background="#efefef"
                        )

                    if date in self.tasks:
                        task_frame = ttk.Frame(cell_frame, bootstyle=PRIMARY)
                        task_frame.pack(fill="both", expand=True)
                        max_tasks_per_row = 2

                        num_tasks = len(self.tasks[date])
                        rows_needed = (num_tasks + max_tasks_per_row - 1) // max_tasks_per_row 

                        for row in range(rows_needed):
                            task_frame.grid_rowconfigure(row, weight=1, uniform="equal")
                        for col in range(max_tasks_per_row):
                            task_frame.grid_columnconfigure(col, weight=1, uniform="equal")

                        if num_tasks == 1:
                            task_button = ctk.CTkButton(
                                master=task_frame,
                                text="",  # Optional: Add task description
                                fg_color=task["color"],
                                hover_color=task["color"],
                                corner_radius=1,
                                width = 250,
                                height =5
                            )
                            task_button.pack(fill="both", expand=True, padx=2, pady=2)
                        else:
                            for i, task in enumerate(self.tasks[date]):
                                row = i // max_tasks_per_row
                                col = i % max_tasks_per_row

                                task_button = ctk.CTkButton(
                                    master=task_frame,
                                    text="",
                                    fg_color=task["color"],
                                    hover_color=task["color"],
                                    width=250,
                                    height=5,
                                    corner_radius=1
                                )
                                task_button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

                    labels_row.append(label)
                self.labels.append(labels_row)

            return self.frame


        def formatweek(self, master, year, month):
            today = datetime.now().date()

            # Check if the container exists and destroy it if necessary
            if hasattr(self, 'container') and self.container.winfo_exists():
                self.container.destroy()

            # Generate week dates for the current week
            week_dates = [self.current_week + timedelta(days=i) for i in range(7)]

            # Main container
            self.container = ctk.CTkFrame(master, fg_color="white")
            self.container.pack(fill="both", expand=True)

            # Configure grid layout for equal expansion
            self.container.grid_columnconfigure(tuple(range(7)), weight=1, uniform="equal")  # 7 columns
            self.container.grid_rowconfigure(0, weight=1)  # Single row

            # Days of the week layout
            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

            for c, (weekday, date) in enumerate(zip(weekdays, week_dates)):
                # Cell container for each day
                cell_frame = ctk.CTkFrame(self.container, fg_color="white", corner_radius=5)
                cell_frame.grid(row=0, column=c, padx=0, pady=0, sticky="nsew")

                # Header with date and day of the week
                header_label = ctk.CTkLabel(
                    master=cell_frame,
                    text=f"{date.strftime('%d %b')}\n{weekday}",
                    font=("Helvetica", 10, "bold"),
                    justify="center",
                    anchor="center",
                    text_color="#848484",
                )
                header_label.pack(fill="both", expand=False, pady=(5, 0))

                # Highlight today's date
                if date == today:
                    header_label.configure(
                        font=("Helvetica", 10, "bold"),
                        text_color="#050505",
                    )

                # Task container inside each day
                task_frame = ctk.CTkFrame(cell_frame, fg_color="#f0f0f0", corner_radius=5)
                task_frame.pack(fill="both", expand=True, padx=1, pady=(5, 10))

                # Display tasks if any
                if date in self.tasks:
                    for i, task in enumerate(self.tasks[date]):
                        # Create a frame for each task
                        task_button = ctk.CTkFrame(
                            master=task_frame,
                            fg_color=task["color"],
                            corner_radius=5,
                            height=50,
                        )
                        task_button.pack(fill="x", expand=False, pady=1)

                        # Task subject
                        subject_label = ctk.CTkLabel(
                            master=task_button,
                            text=task.get("subject"),
                            font=("Helvetica", 6),
                            text_color=TkinterCalendar.darken_color(task["color"]),
                        )
                        subject_label.pack(side="bottom", padx=1, pady=(0, 0))

            return self.container

    current_year = datetime.now().year
    current_month = datetime.now().month
    tkcalendar = TkinterCalendar()
    frame = tkcalendar.formatmonth(frame_current_tasks, current_year, current_month)
    frame.pack_forget()

    def update_month_calendar():
        global frame, current_month, current_year
        current_year = datetime.now().year
        current_month = datetime.now().month
        frame = tkcalendar.formatmonth(frame_current_tasks, current_year, current_month)
        frame.pack(pady=10, fill="both", expand=True) 

    def update_week_calendar():
        global frame
        if not tkcalendar.current_week:
            tkcalendar.current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
        week_number = tkcalendar.current_week.isocalendar()[1]  
        year = tkcalendar.current_week.year
        frame = tkcalendar.formatweek(frame_current_tasks, tkcalendar.current_week.year, tkcalendar.current_week.month)
        frame.pack(pady=10, fill="both", expand=True) 

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
        frame.pack(pady=20, fill="both", expand=True) 
        update_navigation_buttons()  # Update navigation buttons so that it knows what to switch
        update_month_calendar() 

    def show_week_view():
        global current_view, frame
        current_view = "week"
        tkcalendar.current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())  # Refreshes the week calendar with the current week
        frame = tkcalendar.formatweek(frame_current_tasks, current_year, current_month)
        frame.pack(pady=20, fill="both", expand=True) 
        update_navigation_buttons() 
        update_week_calendar() 

    #so depending on what view we are in, it uses that button
    def update_navigation_buttons():
        if current_view == "month":
            button_prev.configure(command=prev_month)
            button_next.configure(command=next_month)
        elif current_view == "week":
            button_prev.configure(command=prev_week)
            button_next.configure(command=next_week)


    # Sample tasks with descriptions for week view
    tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700")
    tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700") #just to see how it looks like with more tasks
    tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700")
    tkcalendar.name_task(datetime(2024, 12, 8).date(), "Examination", "CMSC 130", "#DC7373")
    tkcalendar.name_task(datetime(2024, 12, 5).date(), "Evaluation", "Ethics", "#90EE90")

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


