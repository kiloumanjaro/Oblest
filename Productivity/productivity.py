import ttkbootstrap as ttk

def create_productivity_page(app):
    page = ttk.Frame(app, padding=10, bootstyle="info")
    
    # Add a label for the productivity page
    ttk.Label(page, text="This is the Productivity Page!", font=("Helvetica", 20)).pack(pady=50)
    
    # Ensure the frame takes up all available space within the window
    page.pack(fill="both", expand=True, side="top")
    
    return page
