import tkinter as tk
from tkinter import Scrollbar, Canvas
import os

def login_button_click():
    root.destroy()  # Close the login window
    os.system("python main.py")

# Create the main window
root = tk.Tk()
root.title("Medicine History Website")

# Set the window to full-screen
root.attributes("-fullscreen", True)

# Set the background color
background_color = "lightblue"
root.configure(bg=background_color)

# Create a frame for content
content_frame = tk.Frame(root, bg=background_color)
content_frame.pack(fill=tk.BOTH, expand=tk.YES)

# Create labels for important information and unique facts
info_label = tk.Label(content_frame, text="Medical Stock Tracker", font=("Helvetica", 26), bg=background_color)
facts_label = tk.Label(content_frame, text="Facts about Medicine's History", font=("Helvetica", 16), bg=background_color)

# Position labels within the frame
info_label.pack(pady=(50, 10))
facts_label.pack(pady=(10, 50))

# Create a login button
login_button = tk.Button(content_frame, text="Login", command=login_button_click, font=("Helvetica", 14))
login_button.pack(side=tk.BOTTOM, pady=20)

# Create a canvas for scrolling
canvas = Canvas(content_frame, bg=background_color)
scrollbar = Scrollbar(content_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas
inner_frame = tk.Frame(canvas, bg=background_color)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Create images and information labels for alternating rows
image_paths_row1 = ["img_2.png", "img_3.png"]  # Replace with actual image paths
image_paths_row2 = ["img_4.png", "img_5.png"]  # Replace with actual image paths

info_texts_row1 = [
    "The human body has enough iron to make a 3-inch nail.",
    "Human brain generates about 20 watts."
]

info_texts_row2 = [
    "Heart Pumps 2,000 Gallons Daily.",
    "Dissolve for Quick Absorption."
]

for idx, image_path in enumerate(image_paths_row1):
    frame = tk.Frame(inner_frame, bg=background_color)
    frame.grid(row=idx, column=0, padx=20, pady=20, sticky="w")

    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(frame, image=image)
    image_label.image = image  # Keep a reference to avoid garbage collection
    image_label.pack(side="left")

    info_label = tk.Label(frame, text=info_texts_row1[idx], font=("Helvetica", 12), bg=background_color)
    info_label.pack(side="right")

for idx, image_path in enumerate(image_paths_row2):
    frame = tk.Frame(inner_frame, bg=background_color)
    frame.grid(row=idx, column=1, padx=20, pady=20, sticky="w")

    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(frame, image=image)
    image_label.image = image  # Keep a reference to avoid garbage collection
    image_label.pack(side="left")

    info_label = tk.Label(frame, text=info_texts_row2[idx], font=("Helvetica", 12), bg=background_color)
    info_label.pack(side="right")

# Configure canvas scrolling region
inner_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Bind canvas to keyboard events for scrolling
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
canvas.bind_all("<Up>", lambda event: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Down>", lambda event: canvas.yview_scroll(1, "units"))

# Start the GUI event loop
root.mainloop()
