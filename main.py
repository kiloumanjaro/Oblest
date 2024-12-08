from pathlib import Path
import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import StringVar
from Tasks import TaskManager

# Paths
OUTPUT_PATH = Path(__file__).parent

# Import page creation functions
from Home.home import create_home_page
from Productivity.productivity import create_productivity_page
from Tasks.tasks import create_tasks_page

# Create the application window
app = ttk.Window(themename="custom")  # Using ttkbootstrap for theming
app.geometry("480x820")  # Width x Height in pixels
app.title("Progress Tracker")

screen_height = app.winfo_screenheight()

# Variables
radio_value = StringVar(value="2")  # Default selected page

# Dictionary to store frames for each page
frames = {}

# Create pages and add them to the frames dictionary
frames["1"] = create_tasks_page(app)
frames["2"] = create_home_page(app)
frames["3"] = create_productivity_page(app)


# Function to switch pages
def show_page(page_number):
    """Switches to the selected page by hiding others."""
    for frame in frames.values():
        frame.pack_forget()
    frames[page_number].pack(fill="both", expand=True)

# Create the navigation frame
frame_pages = ttk.Frame(app, padding=0, bootstyle="primary")
frame_pages.place(relx=0.505, y=int(screen_height*0.6593), anchor="center", height=int(screen_height*0.0185))


# Create styled radio buttons
radio_button_1 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=int(screen_height*0.0083),
    radiobutton_height=int(screen_height*0.0083),
    variable=radio_value,
    value="1",
    border_width_unchecked=int(screen_height*0.0037),
    border_width_checked=int(screen_height*0.0037),
    border_color="#D9D9D9",
    fg_color="#DC7373",
    hover=False,
    width=0,
    command=lambda: show_page("1")
)
radio_button_1.pack(side="left", padx=0)  # Add space between buttons

radio_button_2 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=int(screen_height*0.0083),
    radiobutton_height=int(screen_height*0.0083),
    variable=radio_value,
    value="2",
    border_width_unchecked=int(screen_height*0.0037),
    border_width_checked=int(screen_height*0.0037),
    border_color="#D9D9D9",
    fg_color="#DC7373",
    hover=False,
    width=0,
    command=lambda: show_page("2")
)
radio_button_2.pack(side="left", padx=0)

radio_button_3 = ctk.CTkRadioButton(
    master=frame_pages,
    text="",
    radiobutton_width=int(screen_height*0.0083),
    radiobutton_height=int(screen_height*0.0083),
    variable=radio_value,
    value="3",
    border_width_unchecked=int(screen_height*0.0037),
    border_width_checked=int(screen_height*0.0037),
    border_color="#D9D9D9",
    fg_color="#DC7373",
    hover=False,
    width=0,
    command=lambda: show_page("3")
)
radio_button_3.pack(side="left", padx=0)

# Show the initial page (Home)
show_page("3")

# Start the application
app.mainloop()
