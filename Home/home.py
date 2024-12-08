from pathlib import Path
import ttkbootstrap as ttk
from tkinter import StringVar, BooleanVar
import customtkinter as ctk
import random
from datetime import datetime


def create_home_page(app):
    ASSETS_PATH = Path(__file__).parent / "assets"
    MOTIVATIONS_FILE = ASSETS_PATH / "motivations.txt"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def load_random_motivation(file_path: Path) -> str:
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
            return random.choice(lines).strip() if lines else "Stay motivated!"
        except FileNotFoundError:
            return "Motivation file not found!"

    # Variables
    totaldays = 203
    dayspassed = 90
    rank = "diamond"
    rankpts = 78
    left_button_state = BooleanVar(value=False)
    right_button_state = BooleanVar(value=False)

    # Load icons
    try:
        right_icon = ttk.PhotoImage(file=str(relative_to_assets("right_icon.png")))
        left_icon = ttk.PhotoImage(file=str(relative_to_assets("left_icon.png")))
        right_icon_active = ttk.PhotoImage(file=str(relative_to_assets("right_icon_active.png")))
        left_icon_active = ttk.PhotoImage(file=str(relative_to_assets("left_icon_active.png")))
    except Exception as e:
        print(f"Error loading icons: {e}")
        return None

    # Frame definition and layout
    frame_home = ttk.Frame(app)
    frame_home.pack(fill="both", expand=True)  # Ensure frame_home expands

    frame_controls = ttk.Frame(frame_home, bootstyle="success", padding=0)
    frame_controls.pack(fill="x", padx=10, pady=(10, 5))

    frame_text = ttk.Frame(frame_home, bootstyle="primary", padding=10)
    frame_text.pack(fill="x", padx=10, pady=5)

    frame_circle = ttk.Frame(frame_home, bootstyle="primary", padding=15)
    frame_circle.pack(fill="x", padx=10, pady=(10, 2))

    frame_days = ttk.Frame(frame_home, bootstyle="primary", padding=10)
    frame_days.pack(fill="x", padx=10, pady=0, anchor="center")

    frame_progress = ttk.Frame(frame_home, bootstyle="primary", padding=(10, 0))
    frame_progress.pack(fill="x", padx=10, pady=0, anchor="center")

    frame_pages = ttk.Frame(frame_home, padding=5)  # Added definition for frame_pages
    frame_pages.pack(fill="x", padx=10, pady=10)

    overlay_frame = ttk.Frame(frame_home, bootstyle="primary", padding=10)

    frame_button = ttk.Frame(frame_home, bootstyle="primary", padding=0)
    frame_button.pack(fill="x", padx=10, pady=(0, 5), side="bottom")

    # Meter
    meter = ttk.Meter(
        frame_circle,
        metersize=264,
        meterthickness=30,
        padding=0,
        amountused=int((dayspassed / totaldays) * 100),
        metertype="full",
        interactive=True,
        textfont=['Helvetica', 40, 'normal']
    )
    meter.configure(bootstyle="danger")
    meter.pack(pady=20)

    is_overlay_shown = False

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
        height=15,
        corner_radius=10,
        progress_color="#DC7373",
        fg_color="#f7f7f7",
    )
    progress_bar.set(dayspassed / totaldays)
    progress_bar.pack(pady=0)

    # Overlay toggle function
    def toggle_overlay():
        nonlocal is_overlay_shown
        meter.configure(amountused=rankpts)

        if is_overlay_shown:
            overlay_frame.place_forget()        
            meter.configure(bootstyle="danger")
            is_overlay_shown = False
            meter.configure(amountused=int((dayspassed / totaldays) * 100))
        else:
            overlay_frame.place(x=165, y=326, width=150, height=120)
            overlay_frame.tkraise()

            # Update overlay label based on rank
            overlay_label = ttk.Label(
                overlay_frame,
                text="Cu",
                font=("Helvetica", 37),
                bootstyle="dark"
            )
            overlay_label.pack(pady=10)

            if rank == "copper":
                overlay_label.config(text="Cu", bootstyle="dark")
                meter.configure(bootstyle="dark")
            elif rank == "silver":
                overlay_label.config(text="Ag", bootstyle="success")
                meter.configure(bootstyle="success")
            elif rank == "gold":
                overlay_label.config(text="Au", bootstyle="warning")
                meter.configure(bootstyle="warning")
            elif rank == "diamond":
                overlay_label.config(text="C", bootstyle="info")
                meter.configure(bootstyle="info")
            else:
                overlay_label.config(text="Na", bootstyle="primary")
                meter.configure(bootstyle="primary")

            is_overlay_shown = True

    # Toggle buttons
    def toggle_left_button():
        if left_button_state.get():
            left_button_state.set(False)
            button_left.configure(image=left_icon)
        else:
            left_button_state.set(True)
            button_left.configure(image=left_icon_active)
        toggle_overlay()

    def toggle_right_button():
        if right_button_state.get():
            right_button_state.set(False)
            button_right.configure(image=right_icon)
        else:
            right_button_state.set(True)
            button_right.configure(image=right_icon_active)

    # Buttons
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
    date.pack(side="top", pady=4, anchor="w")

    # Set Goals button
    button_1 = ctk.CTkButton(
        master=frame_button,
        text="Set Goals",
        text_color="white",
        command=lambda: print("Set Goals button clicked"),
        fg_color="#DC7373",
        hover_color="#c4524e",
        width=360,
        height=56,
        corner_radius=19,
        font=("Helvetica", 15),
    )
    button_1.pack(side="bottom", anchor="s", pady=10)


    return frame_home
