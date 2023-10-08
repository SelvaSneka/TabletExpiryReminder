import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import PIL
from PIL import Image, ImageTk
import os
import mysql.connector
import urllib.parse
import smtplib

def display_expiry_tablets():
    # Connect to the MySQL database (replace with your database configuration)
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="project1"
        )
        cursor = connection.cursor()

        # Execute a SQL query to retrieve expiry tablet data (adjust the query as needed)
        cursor.execute("SELECT * FROM auto WHERE expiry_date <= CURDATE()")

        # Fetch all records
        expiry_tablets = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Create a new window to display the data
        expiry_window = tk.Toplevel(root)
        expiry_window.title("Expiry Tablet Data")

        # Create a treeview widget to display the data in a tabular format
        tree = ttk.Treeview(expiry_window)
        tree["columns"] = ("Tablet ID", "Tablet Name", "Expiry Date","Manufacturing Date", "Company Name", "Company Email")
        tree.heading("#0", text="", anchor="w")
        tree.column("#0", anchor="w", width=1)
        tree.heading("Tablet ID", text="Tablet ID")
        tree.heading("Tablet Name", text="Tablet Name")
        tree.heading("Expiry Date", text="Expiry Date")
        tree.heading("Manufacturing Date", text="Manufacturing Date")
        tree.heading("Company Name", text="Company Name")
        tree.heading("Company Email", text="Company Email")


        # Insert expiry tablet data into the treeview
        for tablet in expiry_tablets:
            tree.insert("", "end", values=(tablet[0], tablet[1], tablet[2], tablet[3], tablet[4], tablet[5]))

        tree.pack(fill="both", expand=True)

    except mysql.connector.Error as error:
        messagebox.showerror("MySQL Error", f"Error: {error}")

def go_to_previous_page():
    root.destroy()  # Close the current window
    os.system("python nextpage.py")

# Function to open Gmail for ordering expired tablets (you can keep this function as it is)
def order_expiry():
    webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=")  # Replace with your email

    email_subject = "Regarding Tablet Order"

    encoded_subject = urllib.parse.quote(email_subject)

    # Construct the Gmail compose URL with the subject
    compose_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={encoded_subject}"

    # Open the Gmail compose window with the subject
    webbrowser.open(compose_url)


# Function to open Gmail for ordering new tablets (you can keep this function as it is)
def order_new():
    webbrowser.open("https://mail.google.com/")  # Replace with your email

# Create the main application window
root = tk.Tk()
root.title("Order Tablet")
root.attributes("-fullscreen", True)  # Set the window to fullscreen

# Load and resize the back button image
back_image = PIL.Image.open("img_1.png")
back_image = back_image.resize((60, 60), PIL.Image.LANCZOS)
back_image = PIL.ImageTk.PhotoImage(back_image)

# Create a frame for the back button with a white background
back_button_frame = tk.Frame(root, background='white')
back_button_frame.pack(side=tk.TOP, anchor=tk.NW)  # Position at the top-left corner

# Canvas to display the back button image
canvas = tk.Canvas(back_button_frame, width=60, height=60, bg='white')
canvas.pack()

# Place the image on the canvas to create the circular button
back_button = canvas.create_image(30, 30, image=back_image)

# ...

# Function to send emails to company email addresses of expiry soon tablets
def send_emails_to_expiry_tablets():
    try:
        # Connect to the MySQL database (replace with your database configuration)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="project1"
        )
        cursor = connection.cursor()

        # Execute a SQL query to retrieve expiry tablet data (adjust the query as needed)
        cursor.execute("SELECT * FROM auto WHERE expiry_date <= CURDATE()")

        # Fetch all records
        expiry_tablets = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Email configuration (replace with your email and SMTP server information)
        sender_email = "selvasneka871@gmail.com"
        sender_password = "imkx gwpx slgw etxd"
        smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
        smtp_port = 587  # Replace with your SMTP port

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to your email account
        server.login(sender_email, sender_password)

        for tablet in expiry_tablets:
            # Extract company email address from the tablet record
            company_email = tablet[5]

            # Compose the email message for the specific tablet
            email_subject = "Regarding Tablet Order"
            email_body = f"Please place an order for the following expired tablet:\n\n"
            email_body += f"Tablet ID: {tablet[0]}\n"
            email_body += f"Tablet Name: {tablet[1]}\n"
            email_body += f"Expiry Date: {tablet[2]}\n"
            email_body += f"Manufacturing Date: {tablet[3]}\n"
            email_body += f"Company Name: {tablet[4]}\n"
            email_body += f"Company Email: {company_email}\n\n"

            # Compose the complete email message
            email_message = f"Subject: {email_subject}\n\n{email_body}"

            # Send the email to the company email address
            server.sendmail(sender_email, company_email, email_message)

        # Quit the server
        server.quit()

        messagebox.showinfo("Emails Sent", "Emails have been sent to the company email addresses of expiry soon tablets!")

    except Exception as e:
        messagebox.showerror("Email Error", f"An error occurred while sending the emails: {str(e)}")

# Function to handle the back button click event
def on_back_button_click(event):
    go_to_previous_page()

# Bind the click event of the back button to the function
canvas.tag_bind(back_button, '<Button-1>', on_back_button_click)

# Create a frame for the content
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Load the background image
background_image = Image.open("img_6.png")  # Replace with your image file
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), PIL.Image.LANCZOS)
background_image = PIL.ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(frame, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create a title label at the top-center
title_label = tk.Label(frame, text="Order Tablet", font=("Times new roman", 40))
title_label.pack(side=tk.TOP, pady=50)

# Create a frame for the buttons
button_frame = tk.Frame(frame, bg='lightgray')
button_frame.pack(side=tk.TOP, pady=20)

# Create "Order Expiry" button
order_expiry_button = tk.Button(button_frame, text="Order Expiry", command=order_expiry, font=("Times new roman", 20))
order_expiry_button.pack(side=tk.LEFT, padx=20)

# Create "Order New" button
order_new_button = tk.Button(button_frame, text="Check Email", command=order_new, font=("Times new roman", 20))
order_new_button.pack(side=tk.LEFT, padx=20)

# Create "Display Expiry Tablets" button
display_expiry_button = tk.Button(button_frame, text="Display Expiry Tablets", command=display_expiry_tablets, font=("Times new roman", 20))
display_expiry_button.pack(side=tk.LEFT, padx=20)

# Create a "Send Emails to Expiry Tablets" button
send_emails_button = tk.Button(button_frame, text="Send Emails to Expiry Tablets", command=send_emails_to_expiry_tablets, font=("Times new roman", 20))
send_emails_button.pack(side=tk.LEFT, padx=20)

# Run the main event loop
root.mainloop()
