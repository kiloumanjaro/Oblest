from pathlib import Path
import ttkbootstrap as ttk
from tkinter import StringVar, BooleanVar
import customtkinter as ctk
import random
from datetime import datetime

def create_archives_page(app):
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
        return None
    
    frame_archives = ttk.Frame(app)

    frame_controls = ttk.Frame(frame_archives, bootstyle="success", padding=0)
    frame_controls.pack(fill="x", padx=10, pady=(10, 5))

    def toggle_right_button():
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