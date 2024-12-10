from pathlib import Path
from tkinter import *
import ttkbootstrap as ttk
#from Tasks.TaskManager import *
import customtkinter as ctk
import yaml
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from matplotlib.dates import DateFormatter, DayLocator

#all_tasks = TaskManager()

def create_stats_page():
    app = ttk.Window(themename="custom")  # Using ttkbootstrap for theming
    app.geometry("480x820")  # Width x Height in pixels
    app.title("Progress Tracker")

    ASSETS_PATH = Path(__file__).parent / "assets"
    Font = 'Helvetica'

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
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
            frame_statistics.pack_forget()  # Hide archives page
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
        bootstyle="secondary, link",
    )
    button_left.pack(side="left", padx=0, anchor="w")

    button_right = ttk.Button(
        frame_controls,
        text="",
        image=right_icon,
        command=toggle_right_button,
        bootstyle="primary, link",
        width=4,
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


    # ==============================================
    # Section 3: Labels
    # ==============================================

    tasks_labels = ctk.CTkFrame(
        master=tasks_top,
        fg_color="#f7f7f7",  # Frame color
        corner_radius=30,    # Rounded corners
    )
    tasks_labels.pack(fill="x", padx=20, pady=(10,0), side="top")

    # Add three buttons: Time, Average, and Streak
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
        font=("Helvetica", 11)  # Specify the font and size
    )
    button_time.pack(side="left", padx=(18,0), pady=0)


    button_average = ctk.CTkButton(
        master=tasks_labels,
        text="Average",
        text_color="#525252",
        hover=False,
        fg_color="#f7f7f7",
        width=105,
        height=35,
        corner_radius=10,
        font=("Helvetica", 11)  # Specify the font and size
    )
    button_average.pack(side="left", padx=(12, 8), pady=0)


    button_streak = ctk.CTkButton(
        master=tasks_labels,
        text="Streak",
        text_color="#525252",
        hover=False,
        fg_color="#f7f7f7",
        width=90,
        height=35,
        corner_radius=10,
        font=("Helvetica", 11)  # Specify the font and size
    )
    button_streak.pack(side="right", padx=(0,18), pady=0)


    # ==============================================
    # Section 3: Data
    # ==============================================

    font_settings_value = ("Helvetica", 15)  # Font for the numeric values
    font_settings_unit = ("Helvetica", 13)  # Font for the units

    data_entry = ctk.CTkFrame(
        master=tasks_top,
        fg_color="white",  # Frame color
        corner_radius=0,  # Rounded corners
    )
    data_entry.pack(fill="x", padx=20, pady=(3, 0), side="top")

    # Time Label Frame
    time_frame = ctk.CTkFrame(data_entry, fg_color="white", corner_radius=0)
    time_frame.grid_rowconfigure(0, weight=1)
    time_frame.grid_columnconfigure((0, 1), weight=1)  # Configure grid to center labels
    time_label_value = ctk.CTkLabel(time_frame, text="400", text_color="black", font=font_settings_value)
    time_label_unit = ctk.CTkLabel(time_frame, text="mins", text_color="gray", font=font_settings_unit)
    time_label_value.grid(row=0, column=0, padx=(0, 5), sticky="e")  # Use grid to center
    time_label_unit.grid(row=0, column=1, sticky="w")

    # Average Label Frame
    average_frame = ctk.CTkFrame(data_entry, fg_color="white", corner_radius=0, width=80)
    average_frame.grid_rowconfigure(0, weight=1)
    average_frame.grid_columnconfigure((0, 1), weight=1)
    average_label_value = ctk.CTkLabel(average_frame, text="12", text_color="black", font=font_settings_value)
    average_label_unit = ctk.CTkLabel(average_frame, text="mins/task", text_color="gray", font=font_settings_unit)
    average_label_value.grid(row=0, column=0, padx=(0, 5), sticky="e")
    average_label_unit.grid(row=0, column=1, sticky="w")

    # Streak Label Frame
    streak_frame = ctk.CTkFrame(data_entry, fg_color="white", corner_radius=0)
    streak_frame.grid_rowconfigure(0, weight=1)
    streak_frame.grid_columnconfigure((0, 1), weight=1)
    streak_label_value = ctk.CTkLabel(streak_frame, text="50", text_color="black", font=font_settings_value)
    streak_label_unit = ctk.CTkLabel(streak_frame, text="days", text_color="gray", font=font_settings_unit)
    streak_label_value.grid(row=0, column=0, padx=(0, 5), sticky="e")
    streak_label_unit.grid(row=0, column=1, sticky="w")

    # Configure grid columns to distribute space evenly
    data_entry.grid_columnconfigure(0, weight=1)
    data_entry.grid_columnconfigure(1, weight=1)
    data_entry.grid_columnconfigure(2, weight=1)

    # Place frames in the grid
    time_frame.grid(row=0, column=0, padx=(15, 5), pady=0, sticky="nsew")
    average_frame.grid(row=0, column=1, padx=5, pady=0, sticky="nsew")
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



    def on_closing():
        # Destroy the app and any background resources
        plt.close('all')  # Close any matplotlib figures
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)    
    app.mainloop()

# Call the function to display the window
create_stats_page()