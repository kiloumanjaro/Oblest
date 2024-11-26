import tkinter as tk
from tkinter import scrolledtext
import subprocess

def run_script():
    """Run the specified Python file and display its output."""
    file_path = file_entry.get()  # Get the Python file path from the entry
    try:
        # Run the Python file and capture its output
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        output_display.delete(1.0, tk.END)  # Clear the display
        output_display.insert(tk.END, result.stdout)  # Show the script's output
    except subprocess.CalledProcessError as e:
        output_display.delete(1.0, tk.END)
        output_display.insert(tk.END, f"Error while running script:\n{e.stderr}")
    except FileNotFoundError:
        output_display.delete(1.0, tk.END)
        output_display.insert(tk.END, "Error: Python file not found!")

# Create the main window
root = tk.Tk()
root.title("Python Script Runner")
root.geometry("800x600")

# Input field for the Python file path
file_entry = tk.Entry(root, width=50, font=("Arial", 14))
file_entry.pack(pady=10)

# Button to execute the script
run_button = tk.Button(root, text="Run Script", command=run_script, font=("Arial", 14))
run_button.pack(pady=10)

# ScrolledText widget to display the output
output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 12))
output_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Example: Preload a file name (you can change it)
file_entry.insert(0, "example.py")  # Replace with your Python file name

# Run the main loop
root.mainloop()
