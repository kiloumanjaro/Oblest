from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import time
from tkinter import messagebox
import random
from Tasks import TaskManager



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"
GIF_PATH = OUTPUT_PATH / "OBLE GIF"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

global timer_running, timer_end_time
timer_running = False  # Initial state of the timer
timer_end_time = 0  # Timer end time
tasks = ["Task1", "Task2", "Task3"]
remaining_time = 0

class Node:
    def __init__(self, key=None, level=0):
        self.key = key
        self.forward = [None] * (level + 1)

class Skiplist:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = Node(level=max_level)
        self.level = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl

        new_node = Node(key, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]
        return current and current.key == key

    def get_keys_starting_with(self, prefix):
        current = self.header
        while current.forward[0] and not current.forward[0].key.startswith(prefix):
            current = current.forward[0]

        results = []
        while current.forward[0] and current.forward[0].key.startswith(prefix):
            current = current.forward[0]
            results.append(current.key)
        return results

task_skiplist = Skiplist()

for task in tasks:
    task_skiplist.insert(task) #inserts the tasks in the skiplist

def create_searchable_combobox(master, task_list):
    def filter_tasks(event):
        query = search_entry.get().lower()  # Get the lowercase version of the query
        filtered = task_skiplist.get_keys_starting_with(query)  # Filter tasks that contain the query (case-insensitive)
        update_listbox(filtered)

    def update_listbox(filtered_tasks):
        listbox.delete(0, tk.END)  # Clear the listbox before inserting new items
        if filtered_tasks:  # Only show the listbox if there are matching tasks
            for task in filtered_tasks:
                listbox.insert(tk.END, task)
            listbox_height = min(len(filtered_tasks), 5)
            listbox.config(height=listbox_height)
            # Ensure the listbox is visible while matching tasks are found
            if listbox.winfo_ismapped() == 0:  # If the listbox is not currently visible
                listbox.place(x=search_entry.winfo_x(), y=search_entry.winfo_y() + search_entry.winfo_height() + 5, width=search_entry.winfo_width())
        else:
            listbox.place_forget()  # Hide the listbox if no tasks match

    def select_task(event):
        selected = listbox.get(listbox.curselection())  # Get the selected task
        search_entry.delete(0, tk.END)  # Clear the entry field
        search_entry.insert(0, selected)  # Insert the selected task into the entry field
        listbox.place_forget()  # Hide the listbox after selection

    def select_first_task(event):
        if listbox.size() > 0:  # Ensure there are items in the listbox
            listbox.select_set(0)  # Select the first item in the listbox
            select_task(event)  # Simulate selecting that task

    def hide_listbox(event=None):
        if not (search_entry.focus_get() or listbox.focus_get()):
            listbox.place_forget()  # Hide the listbox when clicking outside or when mouse leaves
    # Create a frame for the search bar
    search_frame = ctk.CTkFrame(master, fg_color="transparent")
    search_frame.pack(pady=(10,0), fill="none", side="top")

    # Search entry (like a search bar)
    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Task Name",
        font=("Arial", 14),
        fg_color="white",  # Set the background color of the search bar
        text_color="#A4ADBD",  # Set the text color
        border_color="white",  # Set border color for a subtle effect
        corner_radius=20,  # Rounded edges for a better look
        width=300,  # Set width in pixels
        height=40  # Set height in pixels
    )
    search_entry.pack(padx=10, pady=5, fill="x")
    search_entry.bind("<KeyRelease>", filter_tasks)  # Filter tasks as you type
    search_entry.bind("<FocusOut>", hide_listbox)  # Hide listbox when losing focus
    search_entry.bind("<Return>", select_first_task)  # Bind Enter key to select the first task

    # Listbox for search results (overlay style)
    listbox = tk.Listbox(
        master,
        height=5,
        font=("Arial", 12),
        relief=tk.FLAT,  # No border
        fg="white",  # Updated text color
        highlightthickness=1,
        selectbackground="#BA5757",  # Selection highlight
        selectforeground="white"  # Text color for selection
    )
    listbox.bind("<<ListboxSelect>>", select_task)
    listbox.bind("<FocusOut>", hide_listbox)  # Hide listbox when focus moves out
    listbox.bind("<Leave>", hide_listbox)  # Hide listbox when mouse leaves the listbox
    return search_frame
    #return search_entry

def create_productivity_page(app):
    app.configure(bg="#DC7373")
    global timer_running, timer_end_time
    breaks_remaining = 3  # Initializes the number of breaks
    oble_icon = PhotoImage(file=str(relative_to_assets("oble_icon.png")))

    
    # Create the main frame for the productivity page
    frame_productivity = ctk.CTkFrame(app, fg_color="#DC7373")
    frame_productivity.pack(fill="both", expand=True, pady=0)

    search_bar = create_searchable_combobox(frame_productivity, tasks)
    search_bar.pack(pady=(20, 0))

    frame_time = ttk.Frame(frame_productivity, bootstyle="info", padding=25)
    frame_time.pack(fill="x", padx=0, pady=0, side="top")

    frame_oble = ttk.Frame(frame_productivity, bootstyle="secondary", padding=0)
    frame_oble.configure(style="TFrame")
    frame_oble.pack(pady=0, fill="both", expand=True)

    frame_white = ttk.Frame(frame_productivity)
    frame_white.pack(fill="x", padx=0, pady=0 ,side="bottom")  # A

    frame_button = ttk.Frame(frame_white, bootstyle="primary", padding=0)
    frame_button.pack(fill="x", padx=10, pady=(0, 5), side="bottom")


# Inside the create_productivity_page function

    # Create the ttk.Meter widget named circle
    circle = ttk.Meter(
        master=frame_time,
        metersize=1000,  # Diameter of the circle
        amountused=100,   # Initial value of the meter
        metertype="full",  # Full circle
        meterthickness=80,
        interactive=False  # Disable interactivity for read-only display
    )
    circle.configure(bootstyle="danger")
    circle.place(relx=0.5, y=520, anchor="center")


    # Timer Label
    timer_label = tk.Label(frame_time, text="00:00", font=("Helvetica", 55))
    timer_label.pack(pady=(35,0))

    breaks_label = tk.Label(frame_time, text=f"Breaks remaining: {breaks_remaining}", font=("Helvetica", 10))
    breaks_label.pack(pady=0)

    ''' oble_icon_label = tk.Label( #Using this one first as reference to the screen,then proceed with the simulation of progression
        frame_oble,
        image=oble_icon,
        bg="white"
    )
    oble_icon_label.image = oble_icon  # Keep a reference to the image
    oble_icon_label.pack(pady=10, fill="both", expand=True) '''

        # Frame for the animated images
    animation_label = tk.Label(frame_oble, bg="white")
    animation_label.pack(pady=10, fill="both", expand=True)

    def load_and_sort_images():
        # Load images from the "assets/images" folder
        image_dir = OUTPUT_PATH / "OBLE GIF"  # Adjust the path as needed
        image_files = sorted(image_dir.glob("*.png"))  # Sort images alphabetically
        images = [ImageTk.PhotoImage(Image.open(img).resize((300, 300))) for img in image_files]
        return images

    images = load_and_sort_images()

    def animate_images(index=0, delay=100):
        if not images:
            return  # If no images, skip animation
        if timer_running:
            animation_label.config(image=images[index])
            app.after(delay, animate_images, (index + 1) % len(images), delay)  # Change image every 100ms
        else:
            # Stops the animation once the last image is shown
            animation_label.config(image=images[-1])
    # Start the animation
    #animate_images()

    def create_custom_dialog(app, on_ok, on_cancel):
    #Create a new Toplevel window for the dialog
        dialog = tk.Toplevel(app)
        dialog.title("Set Timer")
        dialog.geometry("480x820")
        dialog.resizable(False, False) 
        dialog.grab_set() #Make the dialog modal

    #Entry Label
        label = tk.Label(dialog, text="Enter time in minutes:", font=("Arial", 13))
        label.pack(pady=10)

    #Timer Input Entry
        timer_input = tk.Entry(dialog, font=("Arial", 14))
        timer_input.pack(pady=5)
    
    #Button Frame
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
    
    #Okay Button
        def ok_action():
            input_text = timer_input.get()
            if input_text.isdigit() and int(input_text) > 0:
                dialog.destroy()
                on_ok(int(input_text))
            else:
                tk.messagebox.showerror("Invalid Input", "Please enter a valid number of minutes", parent=dialog)

        '''ok_button = ctk.CTkbutton(button_frame, text="Okay", command=ok_action, width=10)
        ok_button.pack(side="left", padx=5)  '''
        ok_button = ctk.CTkButton(
        button_frame,
        text="Okay",
        command=ok_action,
        width=120,  # Adjust button width
        height=40,  # Adjust button height
        fg_color="#DC7373",  # Set background color
        corner_radius=10,
        font=("Helvetica", 12)
        )
        ok_button.pack(side="left", padx=10)  # Add spacing between buttons

    #Cancel Button
        def cancel_action():
            dialog.destroy()
            on_cancel()

        ''' cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_action, width=10)
        cancel_button.pack(side="right", padx=5)'''
        cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel",
        command=cancel_action,
        width=120,
        height=40,
        fg_color="#A4A4A4",
        corner_radius=10,
        font=("Helvetica", 12)
        )
        cancel_button.pack(side="right", padx=10) 

    # Start Timer Function
    def start_timer():
        global timer_running, timer_end_time, remaining_time
        if not timer_running:
            if remaining_time == 0:  # If the timer hasn't started yet
                # Prompt user for timer input in minutes
                def on_ok(minutes):
                    global timer_end_time, timer_running, remaining_time
                    timer_duration = minutes * 60
                    timer_end_time = time.time() + timer_duration
                    remaining_time = timer_duration
                    timer_running = True
                    start_timer_button.configure(text="Pause Timer", fg_color="#c4524e")
                    update_timer()
                    animate_images(0, 100)  # Start the animation for one cycle

                def on_cancel():
                    pass  # Return to the page without doing something

                create_custom_dialog(app, on_ok, on_cancel)

            else:
                timer_end_time = time.time() + remaining_time
                timer_running = True
                start_timer_button.configure(text="Pause Timer", fg_color="#c4524e")
                update_timer()
                animate_images(0, 100)  # Start the animation for one cycle

        else:
            # Pause timer
            timer_running = False
            remaining_time = max(0, int(timer_end_time - time.time()))
            start_timer_button.configure(text="Start Timer", fg_color="#cf5b58")

    # Update Timer Function
    def update_timer():
        global timer_running, timer_end_time, remaining_time
        if timer_running:
            remaining_time = max(0, int(timer_end_time - time.time()))  # Update remaining time
        if remaining_time <= 0:
            # Stop the timer when it reaches 0
            timer_running = False
            timer_label.config(text="00:00")
            start_timer_button.configure(text="Start Timer", fg_color="#cf5b58")
            messagebox.showinfo("Session Ended", "Your timer session has ended. Take a break or start a new session iskolar!")
        else:
            minutes, seconds = divmod(remaining_time, 60)
            timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

            # Blink the timer label when less than 10 seconds remain
            if remaining_time <= 10:
                current_color = timer_label.cget("fg")
                new_color = "red" if current_color != "red" else "#000000"  # Toggle between red and black
                timer_label.config(fg=new_color)

            app.after(500, update_timer)  # Call update_timer every 500ms for blinking effect
        return
    # Reset Timer Function
    def reset_timer():
        global timer_running, timer_end_time, remaining_time
        timer_running = False
        timer_end_time = 0
        remaining_time = 0
        timer_label.config(text="00:00")
        start_timer_button.configure(text="Start Timer", fg_color="#cf5b58")

    # Start Timer Button
    start_timer_button = ctk.CTkButton(
        master=frame_button,
        text="Start Timer",
        text_color="white",
        command=start_timer,
        fg_color="#DC7373",
        hover_color="#c4524e",
        width=360,
        height=56,
        corner_radius=19,
        font=("Helvetica", 15)
    )
    start_timer_button.pack(side="bottom", anchor="s", pady=10)

    ''''reset_timer_button = ctk.CTkButton(
        master=frame_button,
        text="Reset Timer",
        text_color="white",
        command=reset_timer,
        fg_color="#DC7373",
        hover_color="#c4524e",
        width=360,
        height=56,
        corner_radius=19,
        font=("Helvetica", 15),
    )
    reset_timer_button.pack(side="bottom", anchor="s", pady=10)
    # Reset Timer Button
    # reset_button = tk.Button(frame_button, text="Reset Timer", command=reset_timer)
    # reset_button.pack(pady=10) '''

    return frame_productivity
