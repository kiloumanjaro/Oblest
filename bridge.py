class Bridge:
    def __init__(self):
        self.search_entry = None
        self.listbox = None
        self.show_page_func = None  # Function to switch pages in the main app

    def register_search_entry(self, search_entry):
        self.search_entry = search_entry

    def register_listbox(self, listbox):
        self.listbox = listbox

    def register_show_page_func(self, func):
        self.show_page_func = func

    def select_task_in_ui(self, task_name):
        if self.search_entry and self.listbox:
            self.search_entry.delete(0, "end")
            self.search_entry.insert(0, task_name)
            self.listbox.place_forget()

    def register_radio_var(self, radio_var):
        self.radio_var = radio_var

    def switch_to_productivity_page(self):
        if self.show_page_func:
            self.show_page_func("3")  # Switch to page "3" (productivity)
            if self.radio_var:
                self.radio_var.set("3")  # Update radio button variable

# Create a global instance of the Bridge
bridge = Bridge()

def set_task_for_productivity(task):
    """
    This function will be called from tasks.py.
    It receives the task and uses the bridge to:
        1. Interact with the UI elements (if needed)
        2. Switch to the productivity page
    """
    bridge.select_task_in_ui(task.name)  # Assuming your Task object has a 'name' attribute
    bridge.switch_to_productivity_page()