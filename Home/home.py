from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
from datetime import datetime  # Import datetime module for the current date

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Create the application window with ttkbootstrap theme
app = ttk.Window(themename="litera")  # You can change the theme to your preference
app.geometry("480x820")  # Width x Height in pixels
totaldays = 203
dayspassed = 90

# Load icons
right_icon = PhotoImage(file=str(relative_to_assets("right_icon.png")))
left_icon = PhotoImage(file=str(relative_to_assets("left_icon.png")))

# Create frames for each section
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

# Empty frame to add space between pages and progress
frame_empty = ttk.Frame(app, bootstyle="primary", padding=5)
frame_empty.pack(fill="x", padx=10, pady=(10, 5))  # Adjust the padding as needed

overlay_frame = ttk.Frame(app, bootstyle="secondary", padding=10)
overlay_frame.place(x=50, y=300, width=200, height=100)  # Position and size the frame
overlay_frame.tkraise()  # Bring it to the front

overlay_label = ttk.Label(
    overlay_frame,
    text="Ag",
    font=("Helvetica", 40),
    bootstyle="fg"
)
overlay_label.pack(pady=10)

frame_pages = ttk.Frame(app, padding=5)
frame_pages.pack(padx=0, pady=0, anchor="center")

frame_button = ttk.Frame(app, bootstyle="primary", padding=0)
frame_button.pack(fill="x", padx=10, pady=(0,10), side="bottom")

def change_meter_color():
    # meter.configure(bootstyle="warning")  # gold
    # meter.configure(bootstyle="info")  # diamond
    # meter.configure(bootstyle="success")  # silver
    meter.configure(bootstyle="dark")  # bronze
    meter.configure(showtext=False)
# Controls section with two buttons
button_left = ttk.Button(
    frame_controls,
    text="",  # No text
    image=left_icon,  # Set the icon
    command=change_meter_color,  # Change the meter color when clicked
    bootstyle="primary, link"
)
button_left.pack(side="left", padx=0, anchor="w")  # Align left

button_right = ttk.Button(
    frame_controls,
    text="",  # No text
    image=right_icon,  # Set the icon
    command=lambda: print("Right button clicked"),
    width=5
)
button_right.pack(side="right", padx=0, anchor="e")  # Align right

# Text section with "Keep Going!" and date
motivation = ttk.Label(
    frame_text, 
    text="Keep Going!", 
    font=("Helvetica", 22, "bold"), 
    bootstyle="fg")
motivation.pack(side="top", pady=0, anchor="w")

# Add the current date below the "Keep Going!" text
current_date = datetime.now().strftime("%B %d, %Y")  # Format: e.g., November 20, 2024
date = ttk.Label(
    frame_text, 
    text=current_date, 
    font=("Helvetica", 11), 
    bootstyle="secondary"
    )
date.pack(side="top", pady=5, anchor="w")

# Circle section (Meter widget)
meter = ttk.Meter(
    frame_circle,
    metersize=260,
    meterthickness=30,
    padding=0,
    amountused=int((dayspassed / totaldays) * 100),  # Ensure this is an integer
    metertype="full",
    interactive=True,
    textfont=['Helvetica', 40, 'normal'],
)
meter.configure(bootstyle="danger")
meter.pack(pady=20)

# Progress section
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

# Radio buttons section (three radio buttons placed side by side)
radio_value = StringVar()

# Add an empty frame to separate sections
frame_empty = ttk.Frame(app, bootstyle="primary", padding=20)
frame_empty.pack(fill="x", padx=10, pady=(0, 100))

space = ttk.Label(
    frame_pages,
    text=".",
    font=("Helvetica", 12),
    bootstyle="light"
)
space.pack(side="left", pady=0)

radio_button_1 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=8,
    radiobutton_height=8,
    variable=radio_value, 
    value="1",
    border_width_unchecked=4 ,
    border_width_checked=4,
    border_color="#D9D9D9",
    fg_color="#DC7373",
    width=0,
    hover=False
)
radio_button_1.pack(side="left", padx=0)

# Create a CTkRadioButton
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


# Button section
button_1 = ctk.CTkButton(
    master=frame_button,
    text="Set Goals",
    text_color="white",  # Set text color to white
    command=lambda: print("Set Goals button clicked"),
    fg_color="#DC7373",
    hover_color="#c4524e",
    width=360,
    height=55,
    corner_radius=20,
    font=("Helvetica", 16),
)
button_1.pack(side="bottom", anchor="s", pady=10)



# Start the Tkinter main loop
app.mainloop()
