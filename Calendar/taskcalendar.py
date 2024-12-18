from calendar import Calendar
from datetime import datetime, timedelta
from pathlib import Path
import ttkbootstrap as ttk
import customtkinter as ctk
from ttkbootstrap.constants import *
from tkinter import PhotoImage

# Paths
OUTPUT_PATH = Path(__file__).parent 
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class TkinterCalendar(Calendar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasks = {}
        
    def name_task(self, date, task_name, subject, color): 
        if date not in self.tasks:
            self.tasks[date] = []
        self.tasks[date].append({"name": task_name, "subject": subject, "color": color})

    def darken_color(hex_color, factor=0.45):
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, int(c * factor)) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*darkened_rgb)


    def formatmonth(self, master, year, month):
        dates = self.monthdatescalendar(year, month)
        frame = ttk.Frame(master, bootstyle=PRIMARY)
        self.labels = []

        today = datetime.now().date()

        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for c, weekday in enumerate(weekdays):
            ttk.Label(
                frame,
                text=weekday,
                font=("Helvetica", 12, "bold"),
                width=4,
                anchor="center",
                bootstyle=SECONDARY
            ).grid(row=0, column=c, padx=5, pady=(5,5))

        # Configure columns to expand
        for c in range(7):
            frame.grid_columnconfigure(c, weight=1, uniform="equal")

        for r, week in enumerate(dates, start=1):
            labels_row = []
            for c, date in enumerate(week):
                cell_frame = ttk.Frame(frame, width=50, height=50, bootstyle=PRIMARY)
                cell_frame.grid(row=r, column=c, padx=5, pady=25, sticky="nsew")

                label = ttk.Label(
                    cell_frame,
                    text=date.strftime('%d'),
                    font=("Helvetica", 9),
                    width=4,
                    anchor="center",
                    bootstyle=SECONDARY
                )
                label.pack(expand=True, fill="both")

                # Configuration for days not in the current month
                if date.month != month:
                    label.configure(foreground="#f2ebea")

                # Configuration for Sundays
                if c == 6 and date.month == month:
                    label.configure(foreground="#cf5b58")

                # Highlight current day
                if date == today:
                    label.configure(
                        font=("Helvetica", 9, "bold"),
                        foreground="#050505",
                        background="#efefef"
                    )

                if date in self.tasks:
                    task_frame = ttk.Frame(cell_frame, bootstyle=PRIMARY)
                    task_frame.pack(fill="both", expand=True)
                    max_tasks_per_row = 2
                    base_task_width = 10
                    task_height = 5

                    num_tasks = len(self.tasks[date])

                    for i, task in enumerate(self.tasks[date]):
                        row = i // max_tasks_per_row
                        col = i % max_tasks_per_row

                        task_width = base_task_width * 2.5 if num_tasks == 1 else base_task_width

                        task_button = ctk.CTkButton(
                            master=task_frame,
                            text="",
                            fg_color=task["color"],
                            hover_color=task["color"],
                            width=task_width,
                            height=task_height,
                            corner_radius=1
                        )
                        task_button.grid(row=row, column=col, padx=2, pady=2)

                labels_row.append(label)
            self.labels.append(labels_row)

        return frame


    def formatweek(self, master, year, month):
        today = datetime.now().date()

        # Generate week dates for the current week
        week_dates = [self.current_week + timedelta(days=i) for i in range(7)]

        # Main container
        container = ctk.CTkFrame(master, fg_color="white")
        container.pack(fill="both", expand=True)

        # Configure grid layout for equal expansion
        container.grid_columnconfigure(tuple(range(7)), weight=1, uniform="equal")  # 7 columns
        container.grid_rowconfigure(0, weight=1)  # Single row

        # Days of the week layout
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        for c, (weekday, date) in enumerate(zip(weekdays, week_dates)):
            # Cell container for each day
            cell_frame = ctk.CTkFrame(container, fg_color="white", corner_radius=5)
            cell_frame.grid(row=0, column=c, padx=5, pady=5, sticky="nsew")

            # Header with date and day of the week
            header_label = ctk.CTkLabel(
                master=cell_frame,
                text=f"{date.strftime('%d %b')}\n{weekday}",
                font=("Helvetica", 10, "bold"),
                justify="center",
                anchor="center",
                text_color="black",
            )
            header_label.pack(fill="both", expand=False, pady=(5, 0))

            # Highlight today's date
            if date == today:
                header_label.configure(
                    font=("Helvetica", 10, "bold"),
                    text_color="#050505",
                )

            # Task container inside each day
            task_frame = ctk.CTkFrame(cell_frame, fg_color="#f0f0f0", corner_radius=5)
            task_frame.pack(fill="both", expand=True, padx=5, pady=(5, 10))

            # Display tasks if any
            if date in self.tasks:
                for i, task in enumerate(self.tasks[date]):
                    # Create a frame for each task
                    task_button = ctk.CTkFrame(
                        master=task_frame,
                        fg_color=task["color"],
                        corner_radius=5,
                        height=50,
                    )
                    task_button.pack(fill="x", expand=False, pady=5)

                    # Task name
                    name_label = ctk.CTkLabel(
                        master=task_button,
                        text=task.get("name"),
                        font=("Helvetica", 14, "bold"),
                        text_color=TkinterCalendar.darken_color(task["color"]),
                    )
                    name_label.pack(side="top", padx=5, pady=(2, 0))

                    # Task subject
                    subject_label = ctk.CTkLabel(
                        master=task_button,
                        text=task.get("subject"),
                        font=("Helvetica", 11),
                        text_color=TkinterCalendar.darken_color(task["color"]),
                    )
                    subject_label.pack(side="bottom", padx=5, pady=(0, 2))

        return container



app = ttk.Window(themename="custom")
app.geometry("480x820")
app.title("Calendar View")
app.configure(bg="#f0f0f0")  # Set the background color

current_year = datetime.now().year
current_month = datetime.now().month

tkcalendar = TkinterCalendar()

def update_month_calendar():
    global frame, current_year, current_month
    header.configure(text=f"{datetime(current_year, current_month, 1):%B %Y}")
    if frame:
        frame.destroy()
    frame = tkcalendar.formatmonth(frame_view, current_year, current_month)
    frame.pack(pady=20, fill="both", expand=True) 

def update_week_calendar():
    global frame
    if frame:
        frame.destroy()
    if not tkcalendar.current_week:
        tkcalendar.current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
    week_number = tkcalendar.current_week.isocalendar()[1]  
    year = tkcalendar.current_week.year
    header.configure(text=f"Week {week_number} - {year}")
    frame = tkcalendar.formatweek(frame_view, tkcalendar.current_week.year, tkcalendar.current_week.month)
    frame.pack(pady=20, fill="both", expand=True) 

def prev_month():
    global current_year, current_month
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1
    update_month_calendar()

def next_month():
    global current_year, current_month
    current_month += 1
    if current_month == 13:
        current_month = 1
        current_year += 1
    update_month_calendar()

def prev_week():
    if tkcalendar.current_week:
        tkcalendar.current_week -= timedelta(weeks=1)
    else:
        tkcalendar.current_week = datetime.now().date() - timedelta(weeks=1)
    update_week_calendar()

def next_week():
    if tkcalendar.current_week:
        tkcalendar.current_week += timedelta(weeks=1)
    else:
        tkcalendar.current_week = datetime.now().date() + timedelta(weeks=1)
    update_week_calendar()

current_view = None

def show_month_view():
    global current_view, frame
    current_view = "month"
    current_year = datetime.now().year
    current_month = datetime.now().month  # Reset to curret when we switch
    if frame:
        frame.destroy()
    frame = tkcalendar.formatmonth(frame_view, current_year, current_month)
    frame.pack(pady=20, fill="both", expand=True) 
    update_navigation_buttons()  # Update navigation buttons so that it knows what to switch
    header.configure(text=f"{datetime(current_year, current_month, 1):%B %Y}") # refreshes to the current month
    color_view()


def show_week_view():
    global current_view, frame
    current_view = "week"
    tkcalendar.current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())  # Refreshes the week calendar with the current week
    if frame:
        frame.destroy()
    frame = tkcalendar.formatweek(frame_view, current_year, current_month)
    frame.pack(pady=20, fill="both", expand=True) 
    update_navigation_buttons() 
    update_week_calendar() 
    color_view()

#so depending on what view we are in, it uses that button
def update_navigation_buttons():
    if current_view == "month":
        button_prev.configure(command=prev_month)
        button_next.configure(command=next_month)
    elif current_view == "week":
        button_prev.configure(command=prev_week)
        button_next.configure(command=next_week)


right_icon = PhotoImage(file=str(relative_to_assets("right_icon.png")))
left_icon = PhotoImage(file=str(relative_to_assets("left_icon.png")))

frame_controls = ttk.Frame(app, bootstyle="primary", padding=0)
frame_controls.pack(fill="x", padx=10, pady=(10, 5))

frame_view_controls = ttk.Frame(app, bootstyle="primary", padding=5)
frame_view_controls.pack(fill="both", padx=10, pady=(1, 1))

frame_view = ttk.Frame(app, bootstyle="secondary", padding=0)
frame_view.pack(fill="both", padx=10, pady=(1, 1))


def color_view():
    if current_view == "month":
        button_week.configure(fg_color= "#f7f4f4", text_color="grey")
        button_month.configure(fg_color= "#DC7373", text_color="white")

    else:
        button_week.configure(fg_color= "#DC7373", text_color="white")
        button_month.configure(fg_color= "#f7f4f4",text_color="grey")


button_week = ctk.CTkButton(
    master=frame_view_controls,
    text="Week",
    text_color="grey",
    command=show_week_view,
    fg_color="#f7f4f4",
    hover_color="#c4524e",
    width=135,
    height=45,
    corner_radius=20,
    font=("Helvetica", 16),
)
button_week.pack(side="left", anchor="s", pady=(10, 2))

button_month = ctk.CTkButton(
    master=frame_view_controls,
    text="Month",
    text_color="white",
    command=show_month_view,
    fg_color="#DC7373",
    hover_color="#c4524e",
    width=135,
    height=45,
    corner_radius=20,
    font=("Helvetica", 16),
)
button_month.pack(side="right", anchor="s", pady=2)


#this is for the header and prev & next buttons
frame_header = ttk.Frame(app, bootstyle="primary", padding=5)
frame_header.pack(fill="x", padx=10, pady=(10,0))

button_prev = ttk.Button(
    frame_header,
    text="◄",
    command=prev_month,
    bootstyle="danger-outline"
)
button_prev.pack(side="left", padx=10)

header = ttk.Label(
    frame_header,
    text=f"{datetime.now():%B %Y}",
    font=("Helvetica", 18, "bold"),
    bootstyle="DANGER"
)
header.pack(side="left", padx=10, expand=True)

button_next = ttk.Button(
    frame_header,
    text="►",
    command=next_month,
    bootstyle="danger-outline"
)
button_next.pack(side="right", padx=10)


# Sample tasks with descriptions for week view
tkcalendar.name_task(datetime(2024, 11, 25).date(), "Assignment", "CMSC 123", "#FFD700")
tkcalendar.name_task(datetime(2024, 11, 26).date(), "Examination", "CMSC 130", "#DC7373")
tkcalendar.name_task(datetime(2024, 11, 27).date(), "Evaluation", "Ethics", "#90EE90")

frame = tkcalendar.formatmonth(frame_view, current_year, current_month)
frame.pack(pady=20)

app.mainloop()
