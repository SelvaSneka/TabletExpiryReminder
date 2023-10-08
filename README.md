# TabletExpiryReminder
This project provides medication expiry reminders, streamlines tablet orders via company email with preset subjects,automatic content when click send email button and simplifies tablet management, including addition, deletion, and data collection for expired tablets.
Backend - Mysql Workbench 8.0 CE
Table1 - "user1" with column like, [ID, username , password]
Table2 - "auto" with column like, [ tablet_id, tablet_name, manufacturing_date, expiry_date , company_name, company_email, contact_no ](1,2,3,4,5,6,7 - understand the order of number is the order of column)
Set the column Data Type as for 1) Auto-increment primary key 2) varchar(45) 3) datetime 4) datetime 5) varchar(45) 6) varchar(45) 7) varchar(10)
Frontend - Python
Using tkinter
Import all the libraries.
