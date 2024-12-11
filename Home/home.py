from pathlib import Path
import ttkbootstrap as ttk
from tkinter import StringVar, BooleanVar
import customtkinter as ctk
import random
from datetime import datetime
from Tasks.tasks import update_radial_progress_bar
from bridge import bridge

meter = None
radial_progress_bar = 0

# Non-linear progression parameters
base = 100         # Base points for the lowest rank
growth_factor = 1.5 # Growth factor that increases the threshold for each subsequent rank

RANK_NAMES = ["copper", "silver", "gold", "diamond"]
RANK_ORDER = {name: i for i, name in enumerate(RANK_NAMES)}

# Global rank points (this would be dynamically updated in your actual application)
rankpts = 0  # Example starting points; in a real scenario, this could be updated over time

bridge.register_rank_points(rankpts)

def rank_threshold_function(rank_order_index, base=100, growth_factor=1.5):
    """
    Calculates the total cumulative points required to achieve the rank at rank_order_index.
    rank_order_index = 0 for copper, 1 for silver, etc.
    """
    if rank_order_index < 0:
        return 0
    total = 0
    for i in range(rank_order_index + 1):
        total += int(base * (growth_factor ** i))
    return total

def get_current_rank_from_points(rankpts, base=100, growth_factor=1.5):
    """
    Given a certain amount of rankpts, determine the user's current rank.
    If the user's points exceed the top threshold, they remain at the highest rank.
    """
    for i, rank_name in enumerate(RANK_NAMES):
        next_threshold = rank_threshold_function(i, base, growth_factor)
        if rankpts < next_threshold:
            # If rankpts is less than the current rank's threshold,
            # the user is currently in this rank.
            return rank_name

    # If we finish the loop and haven't returned, user has surpassed the top rank's threshold
    return RANK_NAMES[-1]


def calculate_rank_progress(current_rank, rankpts, base=100, growth_factor=1.5):
    """
    Calculates a 0-100 percentage that indicates how far along the user is within the current rank's range.
    """
    rank_index = RANK_ORDER[current_rank]

    # Get the current rank's start and end thresholds
    current_rank_min = rank_threshold_function(rank_index - 1, base, growth_factor) if rank_index > 0 else 0
    current_rank_max = rank_threshold_function(rank_index, base, growth_factor)

    # Clamp points to current rank range
    adjusted_points = min(max(rankpts, current_rank_min), current_rank_max)

    # Calculate percentage within this rank's range
    progress_percentage = ((adjusted_points - current_rank_min) / (current_rank_max - current_rank_min)) * 100
    return progress_percentage

def update_meter():
    global meter
    meter.configure(amountused=update_radial_progress_bar())

def create_home_page(app):
    global radial_progress_bar, meter, rankpts
    
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
    frame_home.pack(fill="both", expand=True)

    frame_controls = ttk.Frame(frame_home, bootstyle="primary", padding=0)
    frame_controls.pack(fill="x", padx=10, pady=(10, 5), side="top")

    frame_container = ttk.Frame(frame_home, bootstyle="primary", padding=0)
    frame_container.pack(fill="both", expand="yes", padx=0, pady=0)

    frame_text = ttk.Frame(frame_container, bootstyle="primary", padding=10)
    frame_text.pack(fill="x", padx=10, pady=5)

    frame_circle = ttk.Frame(frame_container, bootstyle="primary", padding=15)
    frame_circle.pack(fill="x", padx=10, pady=(10, 2))

    frame_days = ttk.Frame(frame_container, bootstyle="primary", padding=10)
    frame_days.pack(fill="x", padx=10, pady=0, anchor="center")

    frame_progress = ttk.Frame(frame_container, bootstyle="primary", padding=(5, 0))
    frame_progress.pack(fill="x", padx=10, pady=0, anchor="center")

    overlay_frame = ttk.Frame(frame_container, bootstyle="primary", padding=10)

    frame_button = ttk.Frame(frame_home, bootstyle="primary", padding=0)
    frame_button.pack(fill="x", padx=10, pady=(0, 5), side="bottom")

    # Meter
    meter = ttk.Meter(
        frame_circle,
        metersize=264,
        meterthickness=30,
        padding=0,
        amountused=radial_progress_bar,
        metertype="full",
        interactive=False,
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

    def toggle_overlay():
        nonlocal is_overlay_shown

        # Determine current rank from rankpts
        current_rank = get_current_rank_from_points(rankpts, base, growth_factor)
        # Calculate the rank progress percentage
        rank_progress = int(calculate_rank_progress(current_rank, rankpts, base, growth_factor))
        meter.configure(amountused=rank_progress)

        if is_overlay_shown:
            overlay_frame.place_forget()
            meter.configure(bootstyle="danger")
            is_overlay_shown = False
            update_meter()
        else:
            overlay_frame.place(x=165, y=326, width=150, height=120)
            overlay_frame.tkraise()

            # Update overlay label based on current rank
            overlay_label = ttk.Label(
                overlay_frame,
                text="Cu",
                font=("Helvetica", 37),
                bootstyle="dark"
            )
            overlay_label.pack(pady=10)

            # Since current_rank is now correct, these conditions will set the correct label and style.
            if current_rank == "copper":
                overlay_label.config(text="Cu", bootstyle="dark")
                meter.configure(bootstyle="dark")
            elif current_rank == "silver":
                overlay_label.config(text="Ag", bootstyle="success")
                meter.configure(bootstyle="success")
            elif current_rank == "gold":
                overlay_label.config(text="Au", bootstyle="warning")
                meter.configure(bootstyle="warning")
            elif current_rank == "diamond":
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
