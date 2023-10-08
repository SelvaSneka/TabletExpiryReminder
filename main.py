import tkinter as tk
from tkinter import messagebox
import PIL
from PIL import Image, ImageTk
from tkinter import font as tkFont
import mysql.connector
import os

def go_to_previous_page():
    root.destroy()  # Close the login window
    os.system("python trywithdb.py")
def check_login():
    # Replace this logic with your actual authentication mechanism
    username = entry_username.get()
    password = entry_password.get()

    # Connect to MySQL (replace 'your_username', 'your_password', 'your_database', and 'your_host' with actual values)
    connection = mysql.connector.connect(
        user='root',
        password='root',
        database='project1',
        host='localhost',  # Replace 'localhost' with the correct hostname or IP address of your MySQL server.
        port='3306'  # Replace '3306' with the correct port number of your MySQL server.
    )

    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # SQL query to check if the user exists in the database
        sql = "SELECT * FROM user1 WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # The user exists, perform successful login action here
            messagebox.showinfo(title="Success", message="Login successfully")
            go_to_next_page()
        else:
            # The user does not exist or credentials are incorrect
            messagebox.showerror(title="Error", message="Invalid login.")

    except mysql.connector.Error as error:
        # Show an error message if something goes wrong with the database connection or query execution
        messagebox.showerror("Error", f"Error while connecting to MySQL: {error}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()

def go_to_next_page():
    root.destroy()  # Close the login window
    os.system("python nextpage.py")

# Rest of the code remains the same...
root = tk.Tk()
root.title("MEDICAL STOCK TRACKER")

# Set the window to fullscreen
root.attributes("-fullscreen", True)

# Set the background color
root.config(bg="#f0f0f0")

# Load the image
image_path = "img.png"
image = Image.open(image_path)
image = image.resize((300, 300), Image.LANCZOS)
image = ImageTk.PhotoImage(image)

# Create a frame for the login section
frame = tk.Frame(root, bg="#ffffff")
frame.pack(expand=True, padx=50, pady=50)

font_bold = tkFont.Font(family="Algerian", size=25, weight="bold")
title_label = tk.Label(frame, text="MEDICAL STOCK TRACKER", font=font_bold, bg="#ffffff")
title_label.pack(pady=20)

# Add the image label to the center of the frame
image_label = tk.Label(frame, image=image, bg="#ffffff")
image_label.pack(padx=20, pady=20)

# Create widgets for login
label_username = tk.Label(frame, text="Username:", bg="#ffffff", font=("Times New Roman", 20))
entry_username = tk.Entry(frame, font=("Arial", 16))

label_password = tk.Label(frame, text="Password:", bg="#ffffff", font=("Times New Roman", 20))
entry_password = tk.Entry(frame, show="*", font=("Arial", 16))

button_login = tk.Button(frame, text="Login", command=check_login, font=("Times New Roman", 15))

# Grid layout for login widgets
label_username.pack(pady=(0, 5))
entry_username.pack(pady=(0, 15))

label_password.pack(pady=(0, 5))
entry_password.pack(pady=(0, 15))

button_login.pack()

# Canvas to display the back button image
canvas = tk.Canvas(root, width=60, height=60, bg='white')
canvas.place(x=20, y=20)  # Position the canvas in the top-left corner

# Draw the circular background for the back button
canvas.create_oval(0, 0, 60, 60, fill='white', outline='white')

# Load and resize the back button image
back_image = PIL.Image.open("img_7.png")
back_image = back_image.resize((60, 60), PIL.Image.LANCZOS)
back_image = PIL.ImageTk.PhotoImage(back_image)

# Place the image on the canvas to create the circular button
canvas.create_image(30, 30, image=back_image)

# Function to handle the back button click event
def on_back_button_click(event):
    go_to_previous_page()

# Bind the click event to the back button
canvas.bind("<Button-1>", on_back_button_click)
# Start the main event loop
root.mainloop()
