import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import messagebox
import datetime
import PIL
from PIL import Image, ImageTk
import os
import re

def go_to_previous_page():
    root.destroy()  # Close the login window
    os.system("python main.py")

def go_to_previous_page2():
    root.destroy()  # Close the login window
    os.system("python backbutton.py")
# Define your database connection parameters
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "project1",
    "port": 3306,  # MySQL port (default is 3306)
}

# Create a function to establish a database connection
def create_database_connection():
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as error:
        messagebox.showerror("Database Connection Error", f"Error: {error}")
        return None

# Create a function to execute SQL queries
def execute_query(query, values=None):
    connection = create_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except mysql.connector.Error as error:
            messagebox.showerror("MySQL Error", f"Error: {error}")
            return False


def get_next_tablet_id():
    connection = create_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'project1' AND TABLE_NAME = 'auto';")
            next_id = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            return str(next_id)  # Convert to string
        except mysql.connector.Error as error:
            messagebox.showerror("MySQL Error", f"Error: {error}")
            return None


# Define a function to validate email format using regex
def is_valid_email(email):
    # Regular expression for a simple email format validation
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email)
def add_data():
    tablet_id = get_next_tablet_id()
    tablet_name = tablet_name_entry.get()
    manufacturing_date = manufacturing_date_entry.get()
    expiry_date = expiry_date_entry.get()
    company_name = company_name_entry.get()
    company_email = company_email_entry.get()
    contact_no = contact_no_entry.get()

    # Validate the email format
    if not is_valid_email(company_email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    insert_query = "INSERT INTO auto (tablet_id, tablet_name, manufacturing_date, expiry_date, company_name, company_email, contact_no) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (tablet_id, tablet_name, manufacturing_date, expiry_date, company_name, company_email, contact_no)

    if execute_query(insert_query, values):
        messagebox.showinfo("Success", "Data has been successfully added to MySQL.")
        clear_fields()
        get_next_tablet_id()  # Update the next available Tablet Id after adding a record

# Modify the delete_data function
def delete_data():
    # Get the Tablet Id entered by the user
    tablet_id_to_delete = tablet_id_to_delete_entry.get()

    # Check if the entered Tablet Id is a valid integer
    try:
        tablet_id_to_delete = int(tablet_id_to_delete)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid Tablet Id (an integer).")
        return

    # Define the delete query
    delete_query = "DELETE FROM auto WHERE tablet_id = %s"
    values = (tablet_id_to_delete,)

    # Execute the delete query
    if execute_query(delete_query, values):
        messagebox.showinfo("Success", f"Data with Tablet Id {tablet_id_to_delete} has been successfully deleted from MySQL.")
        clear_fields()

def clear_fields():
    # Clear the contents of all entry field
    tablet_name_entry.delete(0, tk.END)
    manufacturing_date_entry.delete(0, tk.END)
    expiry_date_entry.delete(0, tk.END)
    company_name_entry.delete(0, tk.END)
    company_email_entry.delete(0, tk.END)
    contact_no_entry.delete(0, tk.END)
    tablet_id_to_delete_entry.delete(0, tk.END)


    # Show a message when details are cleared
    messagebox.showinfo("Details Cleared", "Details have been cleared.")

def view_all_data():
    view_query = "SELECT * FROM auto"
    connection = create_database_connection()

    if connection:
        cursor = connection.cursor()
        cursor.execute(view_query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if data:
            display_table(data)
        else:
            messagebox.showinfo("No Data", "No data found in the database.")
def fetch_data_from_mysql():
    try:
        # Connect to MySQL (replace 'your_username', 'your_password', 'your_database', and 'your_host' with actual values)
        connection = mysql.connector.connect(
            user='root',
            password='root',
            database='project1',
            host='localhost',  # Replace 'localhost' with the correct hostname or IP address of your MySQL server.
            port='3306'  # Replace '3306' with the correct port number of your MySQL server.
        )

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # SQL query to fetch data from the table (replace 'your_table_name' with the actual table name)
        sql = "SELECT * FROM auto"
        cursor.execute(sql)

        # Fetch all rows of data from the table
        data = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return data
    except mysql.connector.Error as error:
        # Show an error message if something goes wrong with the database connection or query execution
        messagebox.showerror("Error", f"Error while fetching data from MySQL: {error}")
        return None


def view_expired_data():
    # Fetch data from MySQL
    data = fetch_data_from_mysql()

    if data is not None:
        # Get the current date
        current_date = datetime.date.today()

        # Create a new window to display the expired data
        view_window = tk.Toplevel(root)
        view_window.title("Expired Tablets Data")

        # Create a treeview widget to display the data in tabular format
        tree = ttk.Treeview(view_window)
        tree["columns"] = ("Tablet Id", "Tablet Name", "Manufacturing Date", "Expiry Date")
        tree.heading("#0", text="", anchor="w")
        tree.column("#0", anchor="w", width=1)
        tree.heading("Tablet Id", text="Tablet Id")
        tree.heading("Tablet Name", text="Tablet Name")
        tree.heading("Manufacturing Date", text="Manufacturing Date")
        tree.heading("Expiry Date", text="Expiry Date")

        # Insert expired data into the treeview
        for row in data:
            if len(row) >= 4:
                tablet_id, tablet_name, manufacturing_date, expiry_date = row[:4]
                expiry_date = expiry_date.date()  # Convert to date
                if expiry_date < current_date:
                    tree.insert("", "end", values=(tablet_id, tablet_name, manufacturing_date, expiry_date))

        tree.pack(fill="both", expand=True)

def check_expired_tablets():
    # Fetch data from MySQL
    data = fetch_data_from_mysql()

    if data is not None:
        # Get the current date as a date object
        current_date = datetime.datetime.now().date()

        # Create a timedelta for 4 days
        four_days = datetime.timedelta(days=4)

        # Check for expired tablets and those expiring within 4 days
        expired_tablets = []
        expiring_soon = []

        for tablet in data:
            tablet_id, tablet_name, manufacturing_date, expiry_date = tablet[:4]
            expiry_date = expiry_date.date()  # Convert to date
            remaining_days = (expiry_date - current_date).days
            if remaining_days < 0:
                expired_tablets.append((tablet_id, tablet_name, expiry_date, remaining_days))
            elif 0 <= remaining_days <= 4:
                expiring_soon.append((tablet_id, tablet_name, expiry_date, remaining_days))

        if expired_tablets:
            expired_tablet_message = "The following tablets have expired:\n\n"
            for tablet in expired_tablets:
                tablet_id, tablet_name, expiry_date, remaining_days = tablet
                expired_tablet_message += f"Tablet ID: {tablet_id}\n"
                expired_tablet_message += f"Tablet Name: {tablet_name}\n"
                expired_tablet_message += f"Expiry Date: {expiry_date}\n"
                expired_tablet_message += f"Days Expired: {-remaining_days}\n\n"

            # Show the message for expired tablets
            messagebox.showwarning("Expired Tablets Reminder", expired_tablet_message)

        if expiring_soon:
            expiring_soon_message = "The following tablets will expire soon:\n\n"
            for tablet in expiring_soon:
                tablet_id, tablet_name, expiry_date, remaining_days = tablet
                expiring_soon_message += f"Tablet ID: {tablet_id}\n"
                expiring_soon_message += f"Tablet Name: {tablet_name}\n"
                expiring_soon_message += f"Expiry Date: {expiry_date}\n"
                expiring_soon_message += f"Days Remaining: {remaining_days}\n\n"

            # Ask the user if they want to order tablets that are expiring soon
            expiring_soon_message += "Do you want to Order the Tablet Now?"
            response = messagebox.askyesno("Expiring Tablets Reminder", expiring_soon_message)

            if response:
                # Implement the code to go to the next page or perform the desired action here
                # For example, you can create a new window for the next page:
                navigate_to_next_page()

def navigate_to_next_page():
    root.destroy()  # Close the login window
    os.system("python backbutton.py")
def display_table(data):
    view_window = tk.Toplevel(root)
    view_window.title("All Tablets Data")

    tree = ttk.Treeview(view_window, columns=(
    "Tablet Id", "Tablet Name", "Manufacturing Date", "Expiry Date", "Company Name", "Company Email", "Contact No"))
    tree.heading("#1", text="Tablet Id")
    tree.heading("#2", text="Tablet Name")
    tree.heading("#3", text="Manufacturing Date")
    tree.heading("#4", text="Expiry Date")
    tree.heading("#5", text="Company Name")
    tree.heading("#6", text="Company Email")
    tree.heading("#7", text="Contact No")

    for row in data:
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True)


# Create the main application window
root = tk.Tk()
root.title("MEDICINE STOCK TRACKER")

# Set the window to fullscreen
root.attributes("-fullscreen", True)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the frame
x_coordinate = (screen_width - 900) // 2
y_coordinate = (screen_height - 600) // 2

# Set the window position to center
root.geometry(f"900x600+{x_coordinate}+{y_coordinate}")

root.configure(bg='lightgray')

# Set the font style for all widgets
font_style = ("Times new roman", 20)
# Create a frame for the content
frame = tk.Frame(root, background='#90EE90')
frame.pack(expand=True, padx=50, pady=50)

# Create a separate frame for the labels
label_frame = tk.Frame(frame, background='#90EE90')
label_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

font_bold = tkFont.Font(family="Algerian", size=25, weight="bold")
login_label = ttk.Label(frame, text="MEDICINE STOCK TRACKER", font=font_bold, background='#90EE90')
login_label.grid(row=0, column=0, columnspan=2, pady=(50, 20))

# Create a label to display the next Tablet Id

next_tablet_id_label = ttk.Label(frame, text=f" {get_next_tablet_id()}", font=font_style, background='#90EE90')
next_tablet_id_label.grid(row=7, column=0, padx=10, pady=10, columnspan=2)

# Add an entry field for the user to input the Tablet Id to delete
tablet_id_to_delete_entry = ttk.Entry(frame, font=font_style)
tablet_id_to_delete_entry.grid(row=8, column=1, padx=10, pady=10)
delete_label = ttk.Label(frame, text="Tablet Id to Delete:", font=font_style, background='#90EE90')
delete_label.grid(row=8, column=0, padx=10, pady=10)

tablet_name_label = ttk.Label(frame, text="Tablet Name:", font=font_style, background='#90EE90')
tablet_name_label.grid(row=2, column=0, padx=10, pady=10)
tablet_name_entry = ttk.Entry(frame, font=font_style)
tablet_name_entry.grid(row=2, column=1, padx=10, pady=10)

manufacturing_date_label = ttk.Label(frame, text="Manufacturing Date:", font=font_style, background='#90EE90')
manufacturing_date_label.grid(row=3, column=0, padx=10, pady=10)
manufacturing_date_entry = ttk.Entry(frame, font=font_style)
manufacturing_date_entry.grid(row=3, column=1, padx=10, pady=10)

expiry_date_label = ttk.Label(frame, text="Expiry Date:", font=font_style, background='#90EE90')
expiry_date_label.grid(row=5, column=0, padx=10, pady=10)
expiry_date_entry = ttk.Entry(frame, font=font_style)
expiry_date_entry.grid(row=5, column=1, padx=10, pady=10)

company_name_label = ttk.Label(frame, text="", font=font_style, background='#90EE90')
company_name_label.grid(row=4, column=0, padx=10, pady=10)
company_name_entry = ttk.Entry(frame, font=font_style)
company_name_entry.grid(row=4, column=1, padx=10, pady=10)

company_email_label = ttk.Label(frame, text="", font=font_style, background='#90EE90')
company_email_label.grid(row=4, column=0, padx=10, pady=10)
company_email_entry = ttk.Entry(frame, font=font_style)
company_email_entry.grid(row=4, column=1, padx=10, pady=10)

contact_no_label = ttk.Label(frame, text="Contact No:", font=font_style, background='#90EE90')
contact_no_label.grid(row=4, column=0, padx=10, pady=10)
contact_no_entry = ttk.Entry(frame, font=font_style)
contact_no_entry.grid(row=4, column=1, padx=10, pady=10)

# Create labels and entry fields
labels_and_entries = [
    ("Tablet Id:", next_tablet_id_label),
    ("Tablet Name:", tablet_name_entry),
    ("Manufacturing Date:", manufacturing_date_entry),
    ("Expiry Date:", expiry_date_entry),
    ("Company Name:", company_name_entry),
    ("Company Email:", company_email_entry),
    ("Contact No:", contact_no_entry),
]

for i, (label_text, entry) in enumerate(labels_and_entries):
    label = ttk.Label(frame, text=label_text, font=font_style, background='#90EE90')
    label.grid(row=i + 1, column=0, padx=10, pady=10)
    entry.grid(row=i + 1, column=1, padx=10, pady=10)

# Create a frame for the buttons
button_frame = ttk.Frame(frame)
button_frame.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Add and configure buttons
add_button = ttk.Button(button_frame, text="Add", command=add_data, style="TButton")
delete_button = ttk.Button(button_frame, text="Delete", command=delete_data, style="TButton")
clear_button = ttk.Button(button_frame, text="Clear", command=clear_fields, style="TButton")
view_all_button = ttk.Button(button_frame, text="View All", command=view_all_data, style="TButton")
view_expiry_button = ttk.Button(button_frame, text="View Expiry", command=view_expired_data, style="TButton")

add_button.grid(row=0, column=0, padx=10, pady=10)
delete_button.grid(row=0, column=1, padx=10, pady=10)
clear_button.grid(row=0, column=2, padx=10, pady=10)
view_all_button.grid(row=0, column=3, padx=10, pady=10)
view_expiry_button.grid(row=0, column=4, padx=10, pady=10)  # Add the "View Expiry" button

# Set the uniform column configuration for button_frame
button_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
# Canvas to display the back button image
canvas = tk.Canvas(root, width=60, height=60, bg='white')
canvas.place(x=20, y=20)  # Position the canvas in the top-left corner

# Draw the circular background for the back button
canvas.create_oval(0, 0, 60, 60, fill='gray', outline='black')

# Load and resize the back button image
back_image = PIL.Image.open("img_1.png")
back_image = back_image.resize((60, 60), PIL.Image.LANCZOS)
back_image = PIL.ImageTk.PhotoImage(back_image)

# Place the image on the canvas to create the circular button
canvas.create_image(30, 30, image=back_image)

# Function to handle the back button click event
def on_back_button_click(event):
    go_to_previous_page()

# Bind the click event to the back button
canvas.bind("<Button-1>", on_back_button_click)

# Canvas to display the next page button image
next_page_canvas = tk.Canvas(root, width=60, height=60)
next_page_canvas.place(x=screen_width - 120, y=20)  # Position the canvas in the top right corner

# Draw the circular background for the next page button
next_page_canvas.create_oval(0, 0, 60, 60)

# Load and resize the next page button image (replace 'next_page_image.png' with your image file)
next_page_image = PIL.Image.open("img_10.png")
next_page_image = next_page_image.resize((60, 60), PIL.Image.LANCZOS)
next_page_image = PIL.ImageTk.PhotoImage(next_page_image)

# Place the image on the canvas to create the circular button
next_page_button = next_page_canvas.create_image(30, 30, image=next_page_image)

# Function to handle the next page button click event
def on_next_page_button_click(event):
    go_to_previous_page2()

next_page_button = tk.Button(root, image=next_page_image, bd=0, command=on_next_page_button_click, padx=0, pady=0)

# Bind the click event to the next page button
next_page_canvas.bind("<Button-1>", on_next_page_button_click)

check_expired_tablets()
# Run the main event loop
root.mainloop()







