import tkinter as tk
import ttkbootstrap as ttk
from Home.home import HomePage
from Productivity.productivity import ProductivityPage
from Tasks.tasks import TaskPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Oblest Application")
        self.geometry("480x820")
        self.pages = {}
        self.current_page = None
        self.show_page(HomePage)

    def show_page(self, page_class):
        """Switches to a given page."""
        # Destroy the current page if it exists
        if self.current_page is not None:
            self.current_page.destroy()
        
        # Initialize and display the new page
        page = page_class(self)
        self.pages[page_class] = page
        self.current_page = page
        page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()