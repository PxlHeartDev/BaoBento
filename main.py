# Library Imports
import sys
import tkinter
import os

# Explicit imports
import mysql.connector
from mysql.connector import InterfaceError

# Connect to the MySQL database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password123",
        auth_plugin="mysql_native_password"
    )
except InterfaceError:
    print("\nERROR:\nMySQL service is not running\nPlease ensure it is running before starting the program again\n")
    quit()

# Store the data of the currently logged in customer/employee
global userData

# Set the data of the global variable
def setUserData(data = []):
    global userData
    userData = data

# Refresh the data using the current user's ID
def refreshUserData(type: str):
    if(not(type in ['customer', 'employee'])):
        raise ValueError("Invalid argument for `type` in function `refreshUserData()`\nProgrammer error")
    cursor.execute(f"SELECT * FROM {type}s WHERE {type}ID = {userData[0]}")
    setUserData(cursor.fetchone())

# Get the data of the global variable
def getUserData():
    global userData
    return userData

### Database initialization

# Create cursor (used globally in all database CRUD)
cursor = db.cursor()

# This just makes sure it only runs once and not again when imported
if __name__ == "__main__":
    print("Creating database...")

    # Create database and some tables
    cursor.execute("CREATE DATABASE IF NOT EXISTS baobento")
    cursor.execute("USE baobento")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            customerID BIGINT PRIMARY KEY AUTO_INCREMENT,
            firstName VARCHAR(24),
            lastName VARCHAR(24),
            number VARCHAR(14),
            email VARCHAR(48),
            password VARCHAR(32),
            notifPref TINYINT
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            employeeID BIGINT PRIMARY KEY AUTO_INCREMENT,
            firstName VARCHAR(24),
            lastName VARCHAR(24),
            accessKey VARCHAR(32),
            schedule TINYINT,
            exceptions VARCHAR(255)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            orderID BIGINT PRIMARY KEY AUTO_INCREMENT,
            customerID_FK BIGINT NULL, FOREIGN KEY (customerID_FK) REFERENCES baobento.customers(customerID),
            orderData BLOB,
            complete BOOLEAN,
            paid BOOLEAN,
            placementTime BIGINT,
            pickupTime BIGINT,
            note VARCHAR(255)
        )""")
    print("Database successfully created or already exists")

    # Add the owner login
    cursor.execute("SELECT * FROM employees WHERE employeeID = 1")
    if(not(cursor.fetchone())):
        print("\nOwner login not found, creating a default login")
        cursor.execute(f"""
            INSERT INTO employees (employeeID, firstName, lastName, accessKey)
            VALUES
            (1, "Peter", "Cheung", "MrBao123")
        """)
        db.commit()
    
    # Add the NULL customer (for assigning orders with no real customer)
    cursor.execute("SELECT * FROM customers WHERE customerID = 1")
    if(not(cursor.fetchone())):
        print("\nNo NULL customer found, creating one")
        cursor.execute(f"""
            INSERT INTO customers (customerID, firstName, lastName, number, email, password, notifPref)
            VALUES
            (1, "NULL", "CUSTOMER", "1", "r", "", 0)
        """)
        db.commit()

    # Change the directly of the python command terminal
    # Allows the program to run properly outside of VSCode debug
    os.chdir(os.path.dirname(__file__))

    # Version print
    print(f"""
Version Info:
├ Tkinter {tkinter.TkVersion}
├ Python {sys.version.split(' ')[0]}
└ MySQL Server {'.'.join([str(v) for v in db.get_server_version()])}

Working dir: {os.getcwd()}
(Should be the folder where this script is stored. If it isn't, then something went wrong and things will break!)
""")
# Tested fully on:
# Tkinter 8.6
# Python 3.12.0
# MySQL Server 8.0.35

cursor.execute("USE baobento")
# Execute Tkinter code
import gui