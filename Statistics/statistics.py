from pathlib import Path
from tkinter import *
import ttkbootstrap as ttk
#from Tasks.TaskManager import *
import customtkinter as ctk

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
    tasks_top.pack(fill="both", expand="yes", padx=0, pady=0, side="top")


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
        fg_color="transparent",
        hover=False,
        width=90,
        height=35,
        corner_radius=30,
        font=("Helvetica", 11)  # Specify the font and size
    )
    button_time.pack(side="left", padx=15, pady=0)


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
    button_average.pack(side="left", padx=10, pady=0)


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
    button_streak.pack(side="right", padx=15, pady=0)


    # ==============================================
    # Section 3: Data
    # ==============================================

    data_entry = ctk.CTkFrame(
        master=tasks_top,
        fg_color="blue",  # Frame color
        corner_radius=0,    # Rounded corners
    )
    data_entry.pack(fill="x", padx=20, pady=(10,0), side="top")

    time_label = ctk.CTkLabel(data_entry, text="400 mins", fg_color="white", text_color="black", width=100)
    average_label = ctk.CTkLabel(data_entry, text="12 mins/task", fg_color="white", text_color="black", width=100)
    streak_label = ctk.CTkLabel(data_entry, text="50 days", fg_color="white", text_color="black", width=100)

    # Placing the labels side by side using grid
    time_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
    average_label.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
    streak_label.grid(row=0, column=2, padx=5, pady=10, sticky="e")


    app.mainloop()

# Call the function to display the window
create_stats_page()