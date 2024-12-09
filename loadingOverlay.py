import tkinter as tk
import ttkbootstrap as ttk

class LoadingOverlay:
    def __init__(self, master, text="Loading...", font=("Helvetica", 18)):
        self.master = master
        self.text = text
        self.font = font
        self.overlay_frame = None

    def show(self):
        # Create a frame that covers the entire parent widget
        self.overlay_frame = ttk.Frame(self.master)
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay_frame.lift()  # Ensure overlay is on top

        # Add a label with the loading message
        loading_label = ttk.Label(
            self.overlay_frame,
            text=self.text,
            font=self.font,
            foreground="black",
            background="white"
        )
        loading_label.pack(expand=True)

    def hide(self):
        if self.overlay_frame:
            self.overlay_frame.destroy()