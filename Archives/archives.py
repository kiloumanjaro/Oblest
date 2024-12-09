from pathlib import Path
from tkinter import *
import ttkbootstrap as ttk
import customtkinter as ctk
from ttkbootstrap.widgets import Checkbutton

def create_archives_page():
    # Initialize the application window
    app = ttk.Window(themename="custom")  # Using ttkbootstrap for theming
    app.geometry("480x820")  # Width x Height in pixels
    app.title("Progress Tracker")

    # Configure the TCheckbutton font size globally
    style = ttk.Style()
    style.configure('TCheckbutton', font=('Helvetica', 20))

    ASSETS_PATH = Path(__file__).parent / "assets"

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
        if right_button_state.get():
            right_button_state.set(False)
            button_right.configure(image=right_icon)
            frame_archives.pack_forget()  # Hide archives page
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

    # Start the main event loop
    app.mainloop()

# Call the function to display the window
create_archives_page()
