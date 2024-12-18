# ==============================================
# Section 1: Data Preparation
# ==============================================
from pathlib import Path
from calendar import Calendar
from datetime import datetime, timedelta
from Tasks.TaskManager import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import PhotoImage
from tkinter import simpledialog
from ttkbootstrap.scrolled import ScrolledText
import yaml
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from matplotlib.dates import DateFormatter, DayLocator

from bridge import bridge
from bridge import set_task_for_productivity
from datetime import datetime
from loadingOverlay import *

# import list
# import calendar

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

all_tasks = TaskManager()

bridge.register_all_tasks(all_tasks)

def update_radial_progress_bar():
    return int(all_tasks.get_num_completed_tasks() / all_tasks.get_num_total_tasks() * 100)

def calculate_new_rank_points():
    # current_points = bridge.get_rank_points()
    current_points = 0
    # Perform calculations to update the rank points
    
    completed_tasks = all_tasks.get_completed_tasks()
    for task in completed_tasks:
        current_points += task.difficulty_rating
    
    new_points = current_points  # Example calculation
    

    bridge.set_value_for_rank_points_calculation(new_points)
    bridge.calculate_new_rank_points()
    
    print(f"New rank points: {new_points}")
    return new_points




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


# ==============================================
# Section 1: Global Initialization
# ==============================================

current_year = datetime.now().year
current_month = datetime.now().month

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
    frame_button.pack(fill="x", padx=10, pady=(12, 5), side="bottom")

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
            return

        frame_archives = ttk.Frame(app)
        frame_archives.pack(fill="both", expand=True)

        frame_controls = ttk.Frame(frame_archives, bootstyle="primary", padding=0)
        frame_controls.pack(fill="x", padx=10, pady=(10, 5), side="top")

        frame_container = ttk.Frame(frame_archives, bootstyle="primary", padding=0)
        frame_container.pack(fill="both", expand="yes", padx=10, pady=(10, 5))

        frame_text = ttk.Frame(frame_container, bootstyle="primary", padding=10)
        frame_text.pack(fill="x", padx=10, pady=5)

        frame_search = ttk.Frame(frame_container, bootstyle="primary", padding=0)
        frame_search.pack(fill="x", padx=10, pady=0)

        frame_labels = ttk.Frame(frame_search, bootstyle="primary", padding=0)
        frame_labels.pack(fill="x", padx=10, pady=(30, 0), side="bottom")

        frame_items = ttk.Frame(frame_container, bootstyle="info", padding=0)
        frame_items.pack(fill="x", padx=10, pady=0)

        frame_button = ttk.Frame(frame_archives, bootstyle="primary", padding=0)
        frame_button.pack(fill="x", padx=10, pady=(0, 5), side="bottom")

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

        text = ttk.Label(
            frame_text,
            text="Archives",
            font=("Helvetica", 22, "bold"),
            bootstyle="fg",
        )
        text.pack(side="top", pady=0, anchor="w")

        description = ttk.Label(
            frame_text,
            text="Tasks you’ve completed will be archived here, so \nyou can restore them later.",
            font=("Helvetica", 10),
            bootstyle="secondary",
        )
        description.pack(side="top", pady=4, anchor="w")

        # ==============================================
        # Search Bar
        # ==============================================
        search_var = StringVar()  # Holds the text entered in the search bar
        # Apply the custom style to the search entry
        search_entry = ttk.Entry(
            frame_search,
            textvariable=search_var,
            bootstyle="secondary",
            width=30,
        )
        search_entry.pack(side="left", padx=(10, 10), pady=5)

        def perform_search():
            query = search_var.get()
            print(f"Searching for: {query}")  # Replace with actual search logic

        search_button = ctk.CTkButton(
            master=frame_search,
            text="⌕",
            hover="false",
            command=perform_search,
            corner_radius=8,
            fg_color="#DC7373",
            width=25,
            height=25,
            font=("Arial", 13, "bold"),
            anchor="n",
        )
        search_button.pack(side="left", padx=0, pady=0)

        text = ttk.Label(
            frame_labels,
            text="           Name                                     Type",
            font=("Helvetica", 10),
            bootstyle="fg",
        )
        text.pack(pady=0, anchor="w")

        # ==============================================
        # Scrollable Frame with Checkable Items
        # ==============================================
        scrollable_frame = ctk.CTkScrollableFrame(frame_items, height=325, width=460, fg_color="white")
        scrollable_frame.pack(fill="both", expand=True)

        def create_checkable_item(text, var):
            separator = ttk.Separator(scrollable_frame, orient='horizontal')
            separator.pack(fill="x", padx=(0,10), pady=5)  # Adjust padding for spacing

            var= IntVar()
            checkbox = ttk.Checkbutton(
                scrollable_frame,
                text=text,
                variable=var,
                onvalue = 1,
                offvalue = 2,
                bootstyle="danger, square-toggle",  # Use ttkbootstrap styles
            )
            checkbox.pack(anchor="w", padx=5, pady=10)  # Adjust padding for spacing
            return var
        
        Course = 'Science'
        
        # Create sample checkboxes
        for i in range(5):
            create_checkable_item(f"  Task {i + 1}                                  {Course}", 0)

        separator = ttk.Separator(scrollable_frame, orient='horizontal')
        separator.pack(fill="x", padx=(0,10), pady=5)  # Adjust padding for spacing

        # Set Goals button
        button_1 = ctk.CTkButton(
            master=frame_button,
            text="Restore",
            text_color="white",
            command=lambda: print("Set Goals button clicked"),
            fg_color="#DC7373",
            hover_color="#c4524e",
            width=360,
            height=56,
            corner_radius=19,
        )
        button_1.pack(side="bottom", anchor="s", pady=10)

        return frame_archives
    
    frame_archives = create_archives_page(app)
    frame_archives.pack_forget() 

    # ==============================================
    # Statistics Code
    # ==============================================

    def create_stats_page(app):
        left_button_state = BooleanVar(value=False)
        right_button_state = BooleanVar(value=False)

        try:
            right_icon = ttk.PhotoImage(file=str(relative_to_assets("right_icon.png")))
            left_icon = ttk.PhotoImage(file=str(relative_to_assets("left_icon.png")))
            right_icon_active = ttk.PhotoImage(file=str(relative_to_assets("right_icon_active.png")))
            left_icon_active = ttk.PhotoImage(file=str(relative_to_assets("left_icon_active.png")))
        except Exception as e:
            print(f"Error loading icons: {e}")
            return
        
        frame_statistics = ttk.Frame(app)
        frame_statistics.pack(fill="both", expand=True)

        frame_controls = ttk.Frame(frame_statistics, bootstyle="primary", padding=0)
        frame_controls.pack(fill="x", padx=10, pady=(10, 5), side="top")

        frame_tasks = ttk.Frame(frame_statistics, bootstyle="primary")
        frame_tasks.pack(fill="both", pady=0, expand=True, side="top")

        tasks_top = ttk.Frame(frame_tasks, bootstyle="primary", padding=0)
        tasks_top.pack(fill="both", padx=0, pady=0, side="top")

        tasks_middle = ttk.Frame(frame_tasks, bootstyle="primary", padding=0)
        tasks_middle.pack(fill="both", expand="yes", padx=0, pady=0, side="top")

        frame_button = ttk.Frame(frame_statistics, bootstyle="primary", padding=0)
        frame_button.pack(fill="x", padx=10, pady=(0, 5), side="bottom")

        def toggle_right_button():
            if right_button_state.get():
                right_button_state.set(False)
                button_right.configure(image=right_icon)
            else:
                right_button_state.set(True)
                button_right.configure(image=right_icon_active)


        def toggle_left_button():
            frame_statistics.pack_forget()  # Hide archives page
            frame_taskpage.pack(fill="both", expand=True)  # Show tasks page
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

        button_1 = ctk.CTkButton(
            master=frame_button,
            text="Share",
            text_color="white",
            command=lambda: print("Set Goals button clicked"),
            fg_color="#DC7373",
            hover_color="#c4524e",
            width=360,
            height=56,
            corner_radius=19,
        )
        button_1.pack(side="bottom", anchor="s", pady=10)

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

            #text=all_tasks.get_num_completed_tasks(),  # Replace with actual number
            text="273",
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


        # Unified container for labels and data
        stats_container = ctk.CTkFrame(
            master=tasks_top,
            fg_color="white",
            corner_radius=0
        )
        stats_container.pack(fill="x", padx=20, pady=(10,0), side="top")

        # Configure a 3-column grid in the container to align labels and data
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)
        stats_container.grid_columnconfigure(2, weight=1)

        # ==============================================
        # Row 1: Labels (Time, Average, Streak)
        # ==============================================
        tasks_labels = ctk.CTkFrame(
            master=stats_container,
            fg_color="#f7f7f7",
            corner_radius=30
        )
        tasks_labels.grid(row=0, column=0, columnspan=3, sticky="ew")

        # Configure tasks_labels for a 3-column layout
        tasks_labels.grid_columnconfigure(0, weight=1)
        tasks_labels.grid_columnconfigure(1, weight=1)
        tasks_labels.grid_columnconfigure(2, weight=1)

        button_time = ctk.CTkButton(
            master=tasks_labels,
            text="Time",
            text_color="#525252",
            bg_color="transparent",
            fg_color="#f7f7f7",
            hover=False,
            width=90,
            height=35,
            corner_radius=30,
            font=("Helvetica", 11)
        )
        button_time.grid(row=0, column=0, sticky="ew", padx=(18,0), pady=0)

        button_average = ctk.CTkButton(
            master=tasks_labels,
            text="Average",
            text_color="#525252",
            hover=False,
            fg_color="#f7f7f7",
            width=105,
            height=35,
            corner_radius=10,
            font=("Helvetica", 11)
        )
        button_average.grid(row=0, column=1, sticky="ew", padx=(12,8), pady=0)

        button_streak = ctk.CTkButton(
            master=tasks_labels,
            text="Streak",
            text_color="#525252",
            hover=False,
            fg_color="#f7f7f7",
            width=90,
            height=35,
            corner_radius=10,
            font=("Helvetica", 11)
        )
        button_streak.grid(row=0, column=2, sticky="ew", padx=(0,18), pady=0)


        # ==============================================
        # Row 2: Data (numeric values)
        # ==============================================
        font_settings_value = ("Helvetica", 15)  # Font for the numeric values
        font_settings_unit = ("Helvetica", 13)   # Font for the units

        data_entry = ctk.CTkFrame(
            master=stats_container,
            fg_color="white",
            corner_radius=0
        )
        data_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(3,0))

        data_entry.grid_columnconfigure(0, weight=1)
        data_entry.grid_columnconfigure(1, weight=1)
        data_entry.grid_columnconfigure(2, weight=1)

        # Time Frame
        time_frame = ctk.CTkFrame(data_entry, fg_color="white", corner_radius=0)
        time_frame.grid_rowconfigure(0, weight=1)
        time_frame.grid_columnconfigure((0, 1), weight=1)
        time_label_value = ctk.CTkLabel(time_frame, text="400", text_color="black", font=font_settings_value)
        time_label_unit = ctk.CTkLabel(time_frame, text="mins", text_color="gray", font=font_settings_unit)
        time_label_value.grid(row=0, column=0, padx=(0, 5), sticky="e")
        time_label_unit.grid(row=0, column=1, sticky="w")
        time_frame.grid(row=0, column=0, padx=(15, 5), pady=0, sticky="nsew")

        # Average Frame
        average_frame = ctk.CTkFrame(data_entry, fg_color="white", corner_radius=0)
        average_frame.grid_rowconfigure(0, weight=1)
        average_frame.grid_columnconfigure((0, 1), weight=1)
        average_label_value = ctk.CTkLabel(average_frame, text="12", text_color="black", font=font_settings_value)
        average_label_unit = ctk.CTkLabel(average_frame, text="mins/task", text_color="gray", font=font_settings_unit)
        average_label_value.grid(row=0, column=0, padx=(0, 5), sticky="e")
        average_label_unit.grid(row=0, column=1, sticky="w")
        average_frame.grid(row=0, column=1, padx=5, pady=0, sticky="nsew")

        # Streak Frame
        streak_frame = ctk.CTkFrame(data_entry, fg_color="white", corner_radius=0)
        streak_frame.grid_rowconfigure(0, weight=1)
        streak_frame.grid_columnconfigure((0, 1), weight=1)
        streak_label_value = ctk.CTkLabel(streak_frame, text="50", text_color="black", font=font_settings_value)
        streak_label_unit = ctk.CTkLabel(streak_frame, text="days", text_color="gray", font=font_settings_unit)
        streak_label_value.grid(row=0, column=0, padx=(0, 5), sticky="e")
        streak_label_unit.grid(row=0, column=1, sticky="w")
        streak_frame.grid(row=0, column=2, padx=(5, 15), pady=0, sticky="nsew")



        # ==============================================
        # Section 3: Graph
        # ==============================================

        # Sample YAML data structure
        yaml_data = """
        - date: "2024-12-01"
          tasks_completed: 5
        - date: "2024-12-02"
          tasks_completed: 8
        - date: "2024-12-03"
          tasks_completed: 3
        - date: "2024-12-04"
          tasks_completed: 7
        """

        font_settings = {"family": "Arial", "size": 8}

        data = yaml.safe_load(yaml_data)

        # Extract dates and task counts
        dates = [datetime.strptime(entry["date"], "%Y-%m-%d") for entry in data]
        tasks_completed = [entry["tasks_completed"] for entry in data]

        # Create the matplotlib figure
        fig, ax = plt.subplots(figsize=(3, 3))

        # Plot data
        ax.plot(dates, tasks_completed, marker="o", color="#DC7373", linestyle="-", linewidth=1)


        # Customize tick labels with a smaller font
        ax.tick_params(axis="x", labelsize=8, labelrotation=0)
        ax.tick_params(axis="y", labelsize=8)

        # Remove the tick marks on the x-axis
        ax.tick_params(axis='x', pad=6, length=0)
        ax.tick_params(axis='y', pad=6, length=0)

        ax.xaxis.set_major_locator(DayLocator(interval=1))  # Set interval for label spacing
            
        # Format the x-axis to display dates
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%m/%d"))
        plt.xticks(rotation=0)  # Ensure horizontal labels

        # Adjust the bottom margin to create more space between the labels and the graph
        plt.subplots_adjust(bottom=0.15, top=0.85)  # Adjust the bottom margin (increase this value to add more space)

        # Embed the matplotlib figure in tkinter
        canvas = FigureCanvasTkAgg(fig, master=tasks_middle)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="x", expand=True, pady=("15", "0"), side="top")

        ax.spines['top'].set_color('#525252')   # Top border color
        ax.spines['right'].set_color('#525252') # Right border color
        ax.spines['bottom'].set_color('#525252')# Bottom border color
        ax.spines['left'].set_color('#525252')  # Left border color


        # ==============================================
        # Graph Title
        # ==============================================

        # Create a label for the graph title
        graph_title = ctk.CTkLabel(
            master=tasks_middle,
            text="Your Progress",  # Title text
            font=("Helvetica", 13),  # Font style and size
            fg_color="transparent",  # Background color
            text_color="#343a40",  # Text color
        )
        
        # Position the label using place method
        graph_title.place(relx=0.5, rely=0.07, anchor="n") 


        return frame_statistics
    
    frame_statistics = create_stats_page(app)
    frame_statistics.pack_forget() 


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
    tasks_middle.pack(fill="x", expand=False, padx=0, pady=0, side="top", anchor="n")

    tasks_bottom = ttk.Frame(frame_tasks, bootstyle="dark", padding=0)
    tasks_bottom.pack(fill="both", expand="yes", padx=20, pady=0, side="top")
 
    #frame_overlay = ttk.Frame(frame_taskpage, bootstyle="primary")
    #frame_overlay.place(relx=0.5, y=300, anchor="center", width=150)

    # ==============================================
    # Section 4: Button Functions and Creation
    # ==============================================

    def toggle_left_button():
        frame_taskpage.pack_forget()
        frame_statistics.pack(fill="both", expand=True)
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
        tkcalendar.update_tasks()
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
        ttk.Label(frame_task_form, text="Task Title:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        task_title_entry = ttk.Entry(frame_task_form, width=50, bootstyle="danger")
        task_title_entry.pack(pady=(0,10))

        # Deadline Date Field
        ttk.Label(frame_task_form, text="Deadline Date:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        deadline_date_entry = ttk.DateEntry(
            master=frame_task_form,
            bootstyle="danger",
            dateformat="%Y-%m-%d"
        )
        deadline_date_entry.pack(pady=(0,10))

        # Course Selection Field (Modified)
        ttk.Label(frame_task_form, text="Course:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))

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
        course_dropdown.pack(pady=(0,10))
        
        # Difficulty Rating Slider

        def update_label(val):
            difficulty_rating_label.configure(text=f"Difficulty Rating: {round(float(val))}", font=('Helvetica', 10, 'bold'))
        
        difficulty_rating_label = ttk.Label(frame_task_form, text=f"Difficulty Rating: 1", font=('Helvetica', 10, 'bold'))
        difficulty_rating_label.pack(pady=(10,10))
        difficulty_rating_slider = ttk.Scale(frame_task_form, from_=1, to=10, orient="horizontal", command=update_label, bootstyle="danger")
        difficulty_rating_slider.pack(pady=(0,10))

        # Content Field
        ttk.Label(frame_task_form, text="Content:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        content_text = ScrolledText(frame_task_form, width=50, height=10, bootstyle="danger", autohide=True)
        content_text.pack(pady=(0,10))

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
                'difficulty_rating': round(difficulty_rating_slider.get()),
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

            update_radial_progress_bar()
            refresh_task_list(course, deadline_date)
            calculate_new_rank_points()

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

        text=all_tasks.get_num_completed_tasks(),  # Replace with actual number
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

    segmented_frame = ctk.CTkFrame(
        master=tasks_top, 
        fg_color="white",
        bg_color="transparent"
    )
    segmented_frame.pack(fill="x", pady=(0, 0), padx=15, side="top")
    
    # ==============================================
    # Section 8: Tasks Display: Day, Week, Month
    # ==============================================

    # Create the higher frame
    higher_frame = ctk.CTkFrame(tasks_bottom, bg_color="white", fg_color="white", height = 420)
    higher_frame.pack(fill="x", expand=False)

    frame_current_tasks = ctk.CTkScrollableFrame(
        master=higher_frame,
        bg_color="transparent",
        corner_radius=0,
        fg_color="white",
        height = 420,
        border_color="#FFFFFF",
        scrollbar_button_color="white",       # Default color of scrollbar button     
        scrollbar_button_hover_color="#555555"
    )
    # Initially hide the frame (it will only appear when "Day" is selected)
    frame_current_tasks.pack(pady=(0, 0), padx=(12, 18), fill="both", side="top", expand=YES)
    
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
        # As defined before, returns tasks that have a deadline exactly on selected_date
        return [task for task in tasks if task.deadline and task.deadline.date() == selected_date]

    def get_tasks_for_week_dict(tasks: list[Task], start_of_week: datetime) -> dict:
        """Returns a dictionary of tasks keyed by day for the given week."""
        week_tasks = {}
        for i in range(7):  # 7 days in a week
            current_date = start_of_week + timedelta(days=i)
            week_tasks[current_date.date()] = get_tasks_for_day(tasks, current_date)
        return week_tasks

    def get_tasks_for_month_dict(tasks: list[Task], year: int, month: int) -> dict:
        # Calculate the number of days in the month
        if month == 12:
            start_of_month = datetime(year, month, 1)
            end_of_month = datetime(year+1, 1, 1) - timedelta(days=1)
        else:
            start_of_month = datetime(year, month, 1)
            end_of_month = datetime(year, month+1, 1) - timedelta(days=1)

        # Generate a dictionary mapping each day to its tasks
        month_tasks = {}
        current_date = start_of_month
        while current_date <= end_of_month:
            month_tasks[current_date.date()] = get_tasks_for_day(tasks, current_date)
            current_date += timedelta(days=1)

        return month_tasks


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
    switcher.pack(pady=(10, 0), padx=(0, 0), fill="both", side="top", expand=False)

    def offset_calculator(given_date:datetime):
        offset = 0
        if given_date:
            offset = (given_date + timedelta(days=1)) - datetime.now() 
            
        print(f"Offset: {offset.days}")
        print(f"Given Date: {given_date}")
        print(f"Now: {datetime.now()}")
        return offset.days
    
    def day_toggle_switch(given_date:datetime):
        date_offset = offset_calculator(given_date)
        button1.set("Day")
        toggle_switcher("Day", default=False, date_offset=date_offset)
        
    def toggle_switcher(option, default=True, date_offset=0):
        """
        Handles switching between Day, Week, and Month views, including UI updates and button setup.
        """
        
        frame_current_tasks.pack_forget()
        loading_overlay = ctk.CTkFrame(higher_frame, bg_color="white", fg_color="white")
        loading_overlay.pack(fill="both", expand=True)
        loading_overlay.lift()
        loading_text = ctk.CTkLabel(loading_overlay, bg_color="white", fg_color="white", text_color="black", text="Loading...", height=400, font=("Helvetica", 18), anchor="center" )
        loading_text.pack(pady=(10, 10))
        
        frame_current_tasks.pack(pady=(0, 0), padx=(0, 0), fill="both", expand=True)
        loading_overlay.after(100, lambda: loading_overlay.destroy())

        # Clear existing widgets in frame_current_tasks
        for widget in frame_current_tasks.winfo_children():
            widget.destroy()

        # Pack the frame_current_tasks (only if not already packed)
        if not frame_current_tasks.winfo_ismapped():
            frame_current_tasks.pack(pady=(0, 0), padx=(0, 0), fill="both", expand=True)
        
        # Dictionary to map options to functions
        options = {
            "Day": show_day_view_option, 
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
                    func(date_offset=date_offset)  # Week view function doesn't use date_offset directly
                    # Calculate week number based on offset (this is more complex)
                    target_week = datetime.now().date() + timedelta(weeks=date_offset)
                    week_number = target_week.isocalendar()[1]
                    date_display = f"Week {week_number}"
                elif option == "Month":
                    func(date_offset=date_offset)  # Month view function doesn't use date_offset directly
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
        

    def show_day_view_option(given_date:datetime = datetime.now().date(), date_offset: int = 0):
        # Populate tasks or show generic message
        toggle_scrollbar(True) 
        target_date = datetime.now().date() + timedelta(days=date_offset)
        print(f"Target Date: {target_date}")

        if date_offset != 0:
            tasks = get_tasks_for_day(all_tasks.get_all_tasks_by_priority(), target_date)
        elif given_date:
            tasks = get_tasks_for_day(all_tasks.get_all_tasks_by_priority(), given_date)

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
            

    def show_week_view_option(given_date:datetime = datetime.now().date(), date_offset: int = 0):
        toggle_scrollbar(False)
        # Show week view and toggle calendar
        update_week_calendar(date_offset)

    def show_month_view_option(given_date:datetime = datetime.now().date(), date_offset: int = 0):
        # Show month view and toggle calendar
        toggle_scrollbar(False)
        update_month_calendar(date_offset)

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
        font=("Arial", 13,),  # Use the defined font here
        text_color="#f7f7f7",  # Default unselected text color
        selected_hover_color="#cf5b58",  # Hover color when selected
        selected_color="#DC7373",  # Color when selected
        unselected_hover_color="#f7f7f7",  # Hover color when unselected
        unselected_color="#f7f7f7",  # Background color when unselected
        values=["Day", "Week", "Month"],  # Button options
        command=on_segmented_button_change  # Corrected here
    )

    button1.pack(fill="both", expand="yes", side="top", pady=(0, 0))
    button1.set("Day")

    # ==============================================
    # Section 9: Task Nodes and Frame Creation
    # ==============================================
    
    # ----------------------------------------------
    # 9.1: Generic Frame Generation
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

        color_done = None
        task_function = None
        
        # Task Status Logic
        if task.status == TaskStatus.DONE:      
            color_done = "gray70"
            task_function = lambda: None
        else:
            color_done = "gray96"
            task_function = lambda: set_task_for_productivity(task)
            # This is where the function to send the task to the productivity mode will be inserted

        task_frame = ctk.CTkFrame(
            master=master,
            fg_color=color_done,
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
            fg_color=color_done,
            bg_color=color_done,
            width=20,
            text_color="black",
            font=("Arial", 16),
            hover_color=color_done,
            anchor="w",
            command=task_function
        ).grid(row=0, column=0, sticky="w")

        # Course tag button
        course_button = ctk.CTkButton(
            master=title_frame,
            text=task.course_tag,
            fg_color=all_tasks.get_course_color(task.course_tag),  # Button background color
            hover_color=all_tasks.get_course_color(task.course_tag),  # Same color for hover
            text_color=color_done,
            font=("Arial", 14),
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
            fg_color=color_done,
            bg_color=color_done,
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
        frame_tasks.pack_forget()
        frame_button.pack_forget()

        frame_edit_task = ttk.Frame(frame_taskpage, bootstyle="primary")
        frame_edit_task.pack(fill="both", expand=True)

        # Task Title Field
        ttk.Label(frame_edit_task, text="Task Title:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        task_title_entry = ttk.Entry(frame_edit_task, width=50, bootstyle="danger")
        task_title_entry.insert(0, task.name)
        task_title_entry.pack(pady=(0,10))

        date_placeholder = task.deadline.date() if task.deadline else None

        # Deadline Date Field
        ttk.Label(frame_edit_task, text="Deadline Date:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        deadline_date_entry = ttk.DateEntry(
            master=frame_edit_task,
            bootstyle="danger",
            dateformat="%Y-%m-%d",
            startdate=date_placeholder
        )
        deadline_date_entry.pack(pady=(0,10))

        # Status Field (For testing/demo)
        ttk.Label(frame_edit_task, text="Status: [FOR TESTING ONLY]", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        status_var = tk.StringVar(value=task.status.value)
        status_options = [s.value for s in TaskStatus][:2]  # "done", "not_done"
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
        status_dropdown.pack(pady=(0,10))

        # Course Field
        ttk.Label(frame_edit_task, text="Course:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        courses = all_tasks.get_courses() or ["general"]
        course_var = tk.StringVar(value=task.course_tag)
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
        course_dropdown.pack(pady=(0,10))

        # Difficulty Rating
        def update_label(val):
            difficulty_rating_label.configure(text=f"Difficulty Rating: {round(float(val))}", font=('Helvetica', 10, 'bold'))
        difficulty_rating_label = ttk.Label(frame_edit_task, text=f"Difficulty Rating: {task.difficulty_rating}", font=('Helvetica', 10, 'bold'))
        difficulty_rating_label.pack(pady=(10,2))

        difficulty_rating_slider = ttk.Scale(
            frame_edit_task,
            from_=1,
            to=10,
            orient="horizontal",
            command=update_label,
            bootstyle="danger"
        )
        difficulty_rating_slider.set(task.difficulty_rating)
        difficulty_rating_slider.pack(pady=(0,10))

        # Content Field
        ttk.Label(frame_edit_task, text="Content:", font=('Helvetica', 10, 'bold')).pack(pady=(10,2))
        content_text = ScrolledText(frame_edit_task, width=50, height=10, bootstyle="danger")
        content_text.insert("1.0", task.text_content)
        content_text.pack(pady=(0,10))

        def update_task():
            nonlocal task
            new_title = task_title_entry.get()
            new_deadline_str = deadline_date_entry.entry.get()
            new_course = course_var.get()
            new_content = content_text.get("1.0", "end-1c")
            new_status_str = status_var.get()
            new_difficulty_rating = int(difficulty_rating_slider.get())

            # Validate deadline
            try:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d") if new_deadline_str else None
            except ValueError:
                simpledialog.messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")
                return

            # Convert status string to enum
            try:
                new_status = TaskStatus(new_status_str)
            except ValueError:
                simpledialog.messagebox.showerror("Invalid Status", "Please select a valid status.")
                return

            # If course doesn't exist, offer to create it
            if new_course not in all_tasks.get_courses():
                if not simpledialog.messagebox.askyesno("Course Not Found", f"The course '{new_course}' does not exist. Do you want to create it?"):
                    return
                try:
                    all_tasks.add_course(new_course)
                    course_dropdown.configure(values=all_tasks.get_courses())
                    course_var.set(new_course)
                except ValueError as e:
                    simpledialog.messagebox.showerror("Error Creating Course", str(e))
                    return

            old_course = task.course_tag

            # Update task properties
            task.name = new_title
            task.deadline = new_deadline
            task.course_tag = new_course
            task.text_content = new_content
            task.status = new_status
            task.difficulty_rating = new_difficulty_rating

            # If the course changed, move the task first
            if old_course != new_course:
                if not all_tasks.move_task(task.id, old_course, new_course):
                    simpledialog.messagebox.showerror("Error Updating Task", "Failed to move task to the new course.")
                    return
                # After moving the task to the new course, we must update it there
                try:
                    all_tasks.courses[new_course].update_task(task)
                except ValueError as e:
                    simpledialog.messagebox.showerror("Error Updating Task", str(e))
                    return
            else:
                # Update task directly in the current course
                try:
                    all_tasks.courses[new_course].update_task(task)
                except ValueError as e:
                    simpledialog.messagebox.showerror("Error Updating Task", str(e))
                    return

            # Refresh display
            update_radial_progress_bar()
            calculate_new_rank_points()
            refresh_task_list(new_course, new_deadline)
            frame_edit_task.pack_forget()
            frame_button.pack(fill="x", padx=int(screen_height * 0.0093), pady=(12, int(screen_height * 0.0046)), side="bottom")
            frame_tasks.pack(fill="both", expand=True)
            Tasks_Completed.configure(text=f"{all_tasks.get_num_completed_tasks()}")


        def cancel_edit():
            """
            Cancels the edit operation and returns to the task list.
            """
            frame_edit_task.pack_forget()
            frame_button.pack(fill="x", padx=int(screen_height * 0.0093), pady=(12, int(screen_height * 0.0046)), side="bottom")
            # frame_button.pack(fill="x", padx=10, pady=(12, 5), side="bottom")
            frame_tasks.pack(fill="both", expand=True)

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
    # Section 11: Hyas Code
    # ==============================================

    frame = None

    # ----------------------------------------------
    # Section 11.1: Calendar Widget Class
    # ----------------------------------------------

    class TkinterCalendar(Calendar):
        # ----------------------------------------------
        # Section 11.1.1: Initialization and Task Storage
        # ----------------------------------------------

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tasks = all_tasks.get_all_tasks_by_priority()  # Now a list of Task objects
            
        def update_tasks(self):
            self.tasks = all_tasks.get_all_tasks_by_priority()

        # ----------------------------------------------
        # Section 11.1.2: Helper Functions
        # ----------------------------------------------

        def darken_color(self, hex_color, factor=0.45):
            hex_color = hex_color.lstrip("#")
            rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            darkened_rgb = tuple(max(0, int(c * factor)) for c in rgb)
            return "#{:02x}{:02x}{:02x}".format(*darkened_rgb)

        # ----------------------------------------------
        # Section 11.1.3: Monthly View Formatting
        # ----------------------------------------------

        def formatmonth(self, master, year, month, date_offset=0):
            # Check if the frame exists and destroy it if necessary
            if hasattr(self, 'frame') and self.frame.winfo_exists():
                self.frame.destroy()

            dates = self.monthdatescalendar(year, month)
            self.frame = ttk.Frame(master, bootstyle="primary")
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
                    bootstyle="secondary"
                ).grid(row=0, column=c, padx=5, pady=(5, 5))

            # Configure columns to expand
            for c in range(7):
                self.frame.grid_columnconfigure(c, weight=1, uniform="equal")

            for r, week in enumerate(dates, start=1):
                labels_row = []
                for c, date in enumerate(week):
                    cell_frame = ttk.Frame(self.frame, width=14, height=14, bootstyle="primary")
                    cell_frame.grid(row=r, column=c, padx=1, pady=10, sticky="nsew")

                    label = ttk.Label(
                        cell_frame,
                        text=date.strftime('%d'),
                        font=("Helvetica", 9),
                        width=4,
                        anchor="center",
                        bootstyle="secondary"
                    )
                    label.pack(expand=True, fill="both", side="top")

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

                    # Filter tasks for the current date
                    tasks_for_date = [task for task in self.tasks if task.deadline and task.deadline.date() == date]

                    # print(tasks_for_date)   

                    if tasks_for_date:
                        task_frame = ttk.Frame(cell_frame, bootstyle="primary")
                        task_frame.pack(fill="both", expand=True)
                        max_tasks_per_row = 2

                        num_tasks = len(tasks_for_date)
                        rows_needed = (num_tasks + max_tasks_per_row - 1) // max_tasks_per_row

                        for row in range(rows_needed):
                            task_frame.grid_rowconfigure(row, weight=1, uniform="equal")
                        for col in range(max_tasks_per_row):
                            task_frame.grid_columnconfigure(col, weight=1, uniform="equal")

                        if num_tasks == 1:
                            for single_task in tasks_for_date:
                                task_button = ctk.CTkButton(
                                    master=task_frame,
                                    text="",  # Display task name
                                    fg_color=all_tasks.get_course_color(single_task.course_tag),
                                    hover_color=self.darken_color(all_tasks.get_course_color(single_task.course_tag)),
                                    corner_radius=1,
                                    width=250,
                                    height=5,
                                    command=lambda d=single_task.deadline: day_toggle_switch(d)
                                )
                                task_button.pack(fill="both", expand=True, padx=2, pady=2)
                        else:
                            for i, loop_task in enumerate(tasks_for_date):
                                row = i // max_tasks_per_row
                                col = i % max_tasks_per_row

                                task_button = ctk.CTkButton(
                                    master=task_frame,
                                    text="",  # Display task name
                                    fg_color=all_tasks.get_course_color(loop_task.course_tag),
                                    hover_color=self.darken_color(all_tasks.get_course_color(loop_task.course_tag)),
                                    width=250,
                                    height=5,
                                    corner_radius=1,
                                    command=lambda d=loop_task.deadline: day_toggle_switch(d)
                                )
                                task_button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

                    labels_row.append(label)
                self.labels.append(labels_row)

            return self.frame

        # ----------------------------------------------
        # Section 11.1.4: Weekly View Formatting
        # ----------------------------------------------

        def formatweek(self, master, year, month, date_offset=0):
            today = datetime.now().date()

            # Correctly calculate the start of the target week
            target_date = datetime(year, month, today.day) + timedelta(weeks=date_offset)  # Start from the first of the month
            start_of_week = target_date - timedelta(days=(target_date.weekday()))  # Adjust to start of the week
            self.current_week = start_of_week

            # Check if the container exists and destroy it if necessary
            if hasattr(self, 'container') and self.container.winfo_exists():
                self.container.destroy()

            # Generate week dates for the current week
            week_dates = [(self.current_week + timedelta(days=i)) for i in range(7)]

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
                cell_frame = ctk.CTkFrame(self.container, fg_color="white", corner_radius=0)
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
                task_frame = ctk.CTkFrame(cell_frame, fg_color="#f0f0f0", corner_radius=0)
                task_frame.pack(fill="both", expand=True, padx=1, pady=(5, 10))

                # Filter tasks for the current date
                tasks_for_date = [task for task in self.tasks if task.deadline and task.deadline.date() == date.date()]

                # print(tasks_for_date) # Uncomment to check if tasks are being found
                # print(date.date())

                # Display tasks if any
# Display tasks if any
                if tasks_for_date:
                    for i, task in enumerate(tasks_for_date):
                        # Create a frame for each task
                        task_button = ctk.CTkFrame(
                            master=task_frame,
                            fg_color=all_tasks.get_course_color(task.course_tag),
                            corner_radius=0,
                            height=50,
                        )
                        task_button.pack(fill="x", expand=False, pady=1)

                        # Task name button
                        name_button = ctk.CTkButton(
                            master=task_button,
                            text=task.name.split()[0],
                            font=("Helvetica", 12, "bold"),
                            fg_color=all_tasks.get_course_color(task.course_tag),
                            hover_color=self.darken_color(all_tasks.get_course_color(task.course_tag)),
                            text_color="black",
                            command=lambda d=task.deadline: day_toggle_switch(d)
                        )
                        name_button.pack(side="top", fill="x", expand=True, padx=1, pady=(0, 0))

                        # Task course tag
                        # subject_label = ctk.CTkLabel(
                        #     master=task_button,
                        #     text=task.course_tag,
                        #     font=("Helvetica", 8),
                        #     text_color=self.darken_color(all_tasks.get_course_color(task.course_tag)),
                        # )
                        # subject_label.pack(side="bottom", padx=1, pady=(0, 0))

            return self.container
        

    # ==============================================
    # Section 11.2: Calendar Initialization and Display
    # ==============================================

    tkcalendar = TkinterCalendar()
    frame = tkcalendar.formatmonth(frame_current_tasks, current_year, current_month)
    frame.pack_forget()

    # ==============================================
    # Section 11.3: Calendar Update Functions
    # ==============================================

    def update_month_calendar(date_offset=0):
        global frame, current_month, current_year
        
        # Convert current year/month to a continuous month index
        current_month_index = (current_year * 12) + (current_month - 1)
        # print(current_month_index)
        
        # Add the offset (in months) to the current month index
        target_month_index = current_month_index + date_offset
        
        # Convert back to year and month
        target_year, target_month = divmod(target_month_index, 12)
        target_year = target_year
        target_month = target_month + 1  # because months are 1-based

        # Now just call formatmonth with the correct year and month
        frame = tkcalendar.formatmonth(frame_current_tasks, target_year, target_month)
        frame.pack(pady=10, fill="both", expand=True)

    def update_week_calendar(date_offset = 0):
        global frame
        # Calculate the start of the target week based on the offset
        target_date = datetime.now().date() + timedelta(weeks=date_offset)
        tkcalendar.current_week = target_date - timedelta(days=target_date.weekday())
        
        week_number = tkcalendar.current_week.isocalendar()[1]
        year = tkcalendar.current_week.year
        frame = tkcalendar.formatweek(frame_current_tasks, year, tkcalendar.current_week.month, date_offset)
        frame.pack(pady=10, fill="both", expand=True)

    # ==============================================
    # Section 11.4: Sample Tasks
    # ==============================================

    # # Sample tasks with descriptions for week view
    # tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700")
    # tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700") #just to see how it looks like with more tasks
    # tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700")
    # tkcalendar.name_task(datetime(2024, 12, 8).date(), "Examination", "CMSC 130", "#DC7373")
    # tkcalendar.name_task(datetime(2024, 12, 5).date(), "Evaluation", "Ethics", "#90EE90")

    return frame_taskpage

