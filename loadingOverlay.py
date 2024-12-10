import tkinter as tk
import ttkbootstrap as ttk

class LoadingOverlay:
    def __init__(self, master, text="Loading...", font=("Helvetica", 18), delay=0):
        """
        Initialize the LoadingOverlay class.

        Args:
            master (tkinter widget): The parent widget.
            text (str, optional): The loading message. Defaults to "Loading...".
            font (tuple, optional): The font of the loading message. Defaults to ("Helvetica", 18).
            delay (int, optional): The delay in milliseconds before hiding the overlay. Defaults to 0.
        """
        self.master = master
        self.text = text
        self.font = font
        self.delay = delay
        self.overlay_frame = None
        self.after_id = None

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

        # Schedule the hide method if a delay is set
        if self.delay > 0:
            self.after_id = self.master.after(self.delay, self.hide)

    def hide(self):
        # Cancel any scheduled hide calls
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        # Destroy the overlay frame
        if self.overlay_frame:
            self.overlay_frame.destroy()
            self.overlay_frame = None
