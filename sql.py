# Library imports
import time
import tkinter
from tkinter import messagebox
import re

# My imports
from main import db, cursor, refreshCustomerData, getCustomerData

# Create a customer record
def addCustomer(firstName: str, lastName: str, number: str, email: str, password: str, conPassword: str):
    ## Some validation

    # Simple email regex check
    if(not(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))):
        messagebox.showerror("Error", "Email must contain a valid domain")
        return False
    # Simple phone number regex check
    if(not(re.match(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", number))):
        messagebox.showerror("Error", "Invalid phone number")
        return False

    # Password check
    if(len(password) < 8):
        messagebox.showerror("Error", "Password must be 8 characters or greater")
        return False
    if(password != conPassword):
        messagebox.showerror("Error", "Passwords do not match")
        return False

    # Length and presence checks
    values = [[firstName, "First Name", 24], [lastName, "Last Name", 24], [number, "Number", 14], [email, "Email", 48], [password, "Password", 32]]
    for v in values:
        if(not v[0]):
            messagebox.showerror("Error", "One or more field(s) left blank.\nPlease ensure all fields have been filled out.")
            return False
        if(len(v[0]) > v[2]):
            messagebox.showerror("Error", f"{v[1]} is too long, must be less than {v[2]} characters")
            return False

    # Generate an ID as milliseconds since Jan 1 2023, 00:00 UTC+0
    # This may not work on older devices if they do not support milliseconds
    id = int(time.time() * 1000 - 1672531200000)

    # Attempt to add the customer
    cursor.execute(f"""
        INSERT INTO customers (customerID, firstName, lastName, number, email, password, notifPref)
        VALUES
        ({id}, "{firstName}", "{lastName}", "{number}", "{email}", "{password}", 1)
    """)

    # Success message
    messagebox.showinfo("Success",
f"Successfully created your account\n\n\
First Name: {firstName}\n\
Last Name: {lastName}\n\
Phone Number: {number}\n\
Email: {email}\n\
Password: {password}\n")
    return True

def retrieveCustomerOrders(customerID):
    cursor.execute(f"""
        SELECT *  FROM orders WHERE customerID_FK = {customerID}
    """)
    return cursor.fetchall()

def deleteCustomer(customerID, tl):
    if(messagebox.askyesno("Delete Account", "Are you sure you wish to delete your account?", parent=tl)):
        from gui import setFrame, MainMenu, clearBoxes, destroyToplevels
        clearBoxes()
        destroyToplevels()
        setFrame(MainMenu, "Successfully deleted account\nSorry to see you go", "Success")
        cursor.execute(f"DELETE FROM customers WHERE customerID = {customerID}")
        db.commit()

# Create a customer account
def createAccount():
    from gui import getEntryData, customerLogin
    entryData = getEntryData()
    # Check the dropdown status
    cursor.execute(f"SELECT * FROM customers WHERE email = '{entryData[3]}'")
    data = cursor.fetchone()
    if(data): messagebox.showerror("Error", "Email already in use"); return

    cursor.execute(f"SELECT * FROM customers WHERE number = '{entryData[2]}'")
    data = cursor.fetchone()
    if(data): messagebox.showerror("Error", "Phone number already in use"); return

    if(addCustomer(*entryData)):
        customerLogin()
        db.commit()

def updateNotif(customerID, sms, email, tl):
    # Update
    cursor.execute(f"UPDATE customers SET notifPref = {int(f'0b{sms}{email}', 0)} WHERE customerID = {customerID};")
    db.commit()
    refreshCustomerData()
    messagebox.showinfo("Success", "Successfully updated notification preferences", parent=tl)

def updateDetails(customerID, firstName, lastName, number, tl):
    # Length and presence checks
    values = [[firstName, "First Name", 24], [lastName, "Last Name", 24], [number, "Number", 14]]
    for v in values:
        if(not v[0]):
            messagebox.showerror("Error", "One or more field(s) left blank.\nPlease ensure all fields have been filled out.", parent=tl)
            return False
        if(len(v[0]) > v[2]):
            messagebox.showerror("Error", f"{v[1]} is too long, must be less than {v[2]} characters", parent=tl)
            return False
    
    # Simple phone number regex check
    if(not(re.match(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", number))):
        messagebox.showerror("Error", "Invalid phone number", parent=tl)
        return

    # Update
    cursor.execute(f"UPDATE customers SET firstName = '{firstName}', lastName = '{lastName}', number = '{number}' WHERE customerID = {customerID};")
    db.commit()
    refreshCustomerData()
    messagebox.showinfo("Success", "Successfully updated personal details", parent=tl)

def updateEmail(customerID, email, tl):
    # Presence check
    if(not(email)):
        messagebox.showerror("Error", "Email field left blank.\nPlease ensure the field has been filled out.", parent=tl)
        return
    # Length check
    if(len(len(email)) > 48):
        messagebox.showerror("Error", "Email is too long, must be less than 48 characters", parent=tl)
        return
    # Simple email regex check
    if(not(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))):
        messagebox.showerror("Error", "Email must contain a valid domain", parent=tl)
        return

    # Update
    cursor.execute(f"UPDATE customers SET email = '{email}' WHERE customerID = {customerID};")
    db.commit()
    refreshCustomerData()
    messagebox.showinfo("Success", "Successfully updated email", parent=tl)
    
def updatePassword(customerID, newPass, oldPass, tl):
    # Presence check
    if(not(newPass)):
        messagebox.showerror("Error", "Password cannot be left blank", parent=tl)
        return
    # Invalid old password
    if(oldPass != getCustomerData()[5]):
        messagebox.showerror("Failed", "Old password is incorrect, update failed", parent=tl)
        return
    # Length check
    if(len(newPass) < 8):
        messagebox.showerror("Error", "Password must be 8 characters or greater", parent=tl)
        return
    if(len(newPass) > 32):
        messagebox.showerror("Error", "Password must be less than 32 characters", parent=tl)
        return
    # New is old check
    if(newPass == oldPass):
        messagebox.showerror("Error", "New password cannot be old password", parent=tl)
        return
    
    # Update
    cursor.execute(f"UPDATE customers SET password = '{newPass}' WHERE customerID = {customerID};")
    db.commit()
    refreshCustomerData()
    messagebox.showinfo("Success", "Successfully updated password", parent=tl)
