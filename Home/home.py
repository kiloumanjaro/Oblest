from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
from datetime import datetime  # Import datetime module for the current date
import random  # Import random module for selecting random phrases

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"
MOTIVATIONS_FILE = OUTPUT_PATH / "assets" / "motivations.txt"  # Path to the motivations file

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_random_motivation(file_path: Path) -> str:
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        return random.choice(lines).strip() if lines else "Stay motivated!"
    except FileNotFoundError:
        return "Motivation file not found!"

# Create the application window
app = ttk.Window(themename="custom")  # Change theme if needed
app.geometry("480x820")  # Width x Height in pixels
app.title("Progress Tracker")

# Variables
totaldays = 203
dayspassed = 90
rank = "diamond"
rankpts = 78 
is_overlay_shown = False  # Flag to track overlay visibility
left_button_state = BooleanVar(value=False)
right_button_state = BooleanVar(value=False)

# Load icons
right_icon = PhotoImage(file=str(relative_to_assets("right_icon.png")))
left_icon = PhotoImage(file=str(relative_to_assets("left_icon.png")))
right_icon_active = PhotoImage(file=str(relative_to_assets("right_icon_active.png")))
left_icon_active = PhotoImage(file=str(relative_to_assets("left_icon_active.png")))

# Frames
frame_controls = ttk.Frame(app, padding=0)
frame_controls.pack(fill="x", padx=10, pady=(10, 5))

frame_text = ttk.Frame(app, bootstyle="primary", padding=10)
frame_text.pack(fill="x", padx=10, pady=5)

frame_circle = ttk.Frame(app, bootstyle="primary", padding=10)
frame_circle.pack(fill="x", padx=10, pady=10)

frame_days = ttk.Frame(app, bootstyle="primary", padding=5)
frame_days.pack(fill="x", padx=10, pady=0, anchor="center")

frame_progress = ttk.Frame(app, bootstyle="primary", padding=5)
frame_progress.pack(fill="x", padx=10, pady=0, anchor="center")

frame_empty = ttk.Frame(app, bootstyle="primary", padding=5)
frame_empty.pack(fill="x", padx=10, pady=(10, 5))

overlay_frame = ttk.Frame(app, bootstyle="primary", padding=10)

frame_pages = ttk.Frame(app, padding=5)
frame_pages.pack(padx=0, pady=0, anchor="center")

frame_button = ttk.Frame(app, bootstyle="primary", padding=0)
frame_button.pack(fill="x", padx=10, pady=(0, 10), side="bottom")

# Overlay toggle function
def toggle_overlay():
    global is_overlay_shown
    meter.configure(amountused=rankpts)

    if is_overlay_shown:
        # Hide the overlay and revert changes
        overlay_frame.place_forget()
        meter.configure(bootstyle="danger")  # Revert meter color
        is_overlay_shown = False
        meter.configure(amountused=int((dayspassed / totaldays) * 100))

    else:
        # Show the overlay and apply changes
        overlay_frame.place(x=165, y=327, width=150, height=120)
        overlay_frame.tkraise()  # Bring overlay to the front

        # Update overlay label based on rank
        if rank == "copper":
            overlay_label.config(text="Cu", bootstyle="dark")
        elif rank == "silver":
            overlay_label.config(text="Ag", bootstyle="success")
        elif rank == "gold":
            overlay_label.config(text="Au", bootstyle="warning")
        elif rank == "diamond":
            overlay_label.config(text="C", bootstyle="info")
        else:
            overlay_label.config(text="Na", bootstyle="primary")

        # Change meter color
        if rank == "copper":
            meter.configure(bootstyle="dark")
        elif rank == "silver":
            meter.configure(bootstyle="success")
        elif rank == "gold":
            meter.configure(bootstyle="warning")
        elif rank == "diamond":
            meter.configure(bootstyle="info")
        else:
            meter.configure(bootstyle="primary")

        is_overlay_shown = True

# Overlay content
overlay_label = ttk.Label(
    overlay_frame,
    text="Cu",
    font=("Helvetica", 37),
    bootstyle="dark"
)
overlay_label.pack(pady=10)


def toggle_left_button():
    if left_button_state.get():
        left_button_state.set(False)
        button_left.configure(image=left_icon)  # Default style
    else:
        left_button_state.set(True)
        button_left.configure(image=left_icon_active)  # Active style
    toggle_overlay()

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

# Motivation and date
motivation_text = load_random_motivation(MOTIVATIONS_FILE)
motivation = ttk.Label(
    frame_text,
    text=motivation_text,
    font=("Helvetica", 22, "bold"),
    bootstyle="fg"
)
motivation.pack(side="top", pady=0, anchor="w")

current_date = datetime.now().strftime("%B %d, %Y")
date = ttk.Label(
    frame_text,
    text=current_date,
    font=("Helvetica", 11),
    bootstyle="secondary"
)
date.pack(side="top", pady=5, anchor="w")

# Meter
meter = ttk.Meter(
    frame_circle,
    metersize=260,
    meterthickness=30,
    padding=0,
    amountused=int((dayspassed / totaldays) * 100),
    metertype="full",
    interactive=True,
    textfont=['Helvetica', 40, 'normal']
)
meter.configure(bootstyle="danger")
meter.pack(pady=20)

# Days and progress
label_1 = ttk.Label(
    frame_days,
    text=f"{totaldays} Days",
    font=("Helvetica", 12),
    bootstyle="fg"
)
label_1.pack(side="left", pady=0, anchor="w")

label_2 = ttk.Label(
    frame_days,
    text=f"Remaining: {dayspassed}",
    font=("Helvetica", 12),
    bootstyle="fg"
)
label_2.pack(side="right", pady=0, anchor="e")

progress_bar = ctk.CTkProgressBar(
    master=frame_progress,
    width=360,
    height=20,
    corner_radius=10,
    progress_color="#DC7373",
    fg_color="#f7f7f7",
)
progress_bar.set(dayspassed / totaldays)
progress_bar.pack(pady=0)

# Radio buttons
radio_value = StringVar(value="2")

radio_button_1 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=8,
    radiobutton_height=8,
    variable=radio_value,
    value="1",
    border_width_unchecked=4,
    border_width_checked=4,
    border_color="#D9D9D9",
    fg_color="#DC7373",
    width=0,
    hover=False
)
radio_button_1.pack(side="left", padx=0)

radio_button_2 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=8,
    radiobutton_height=8,
    variable=radio_value,
    value="2",
    border_width_unchecked=4,
    border_width_checked=4,
    border_color="#D9D9D9",
    fg_color="#DC7373",
    width=0,
    hover=False
)
radio_button_2.pack(side="left", padx=0)

radio_button_3 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=8,
    radiobutton_height=8,
    variable=radio_value,
    value="3",
    border_width_unchecked=4,
    border_width_checked=4,
    border_color="#D9D9D9",
    fg_color="#DC7373",
    width=0,
    hover=False
)
radio_button_3.pack(side="left", padx=0)

# Set Goals button
button_1 = ctk.CTkButton(
    master=frame_button,
    text="Set Goals",
    text_color="white",
    command=lambda: print("Set Goals button clicked"),
    fg_color="#DC7373",
    hover_color="#c4524e",
    width=360,
    height=55,
    corner_radius=20,
    font=("Helvetica", 16),
)
button_1.pack(side="bottom", anchor="s", pady=10)

# Start the application
app.mainloop()
