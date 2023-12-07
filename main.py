# Library Imports
import sys
import tkinter

# mysql.connector must be imported explicitly
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    auth_plugin="mysql_native_password"
)

# Store the data of the currently logged in customer
global customerData

def setCustomerData(data = []):
    global customerData
    customerData = data

def refreshCustomerData():
    cursor.execute(f"SELECT * FROM customers WHERE customerID = {customerData[0]}")
    setCustomerData(cursor.fetchone())

def getCustomerData():
    global customerData
    return customerData

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
            customerID BIGINT PRIMARY KEY,
            firstName VARCHAR(24),
            lastName VARCHAR(24),
            number VARCHAR(14),
            email VARCHAR(48),
            password VARCHAR(32),
            notifPref INT
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            employeeID BIGINT PRIMARY KEY,
            firstName VARCHAR(24),
            lastName VARCHAR(24),
            accessKey VARCHAR(32)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            orderID BIGINT PRIMARY KEY,
            customerID_FK BIGINT NULL, FOREIGN KEY (customerID_FK) REFERENCES baobento.customers(customerID),
            orderData BLOB,
            complete BOOLEAN,
            paid BOOLEAN,
            placementTime BIGINT,
            pickupTime BIGINT,
            note VARCHAR(255)
        )""")
    print("Database successfully created")

    cursor.execute("SELECT * FROM employees WHERE employeeID = 1")
    if(not(cursor.fetchone())):
        print("\nCreating default Owner Profile")
        cursor.execute(f"""
            INSERT INTO employees (employeeID, firstName, lastName, accessKey)
            VALUES
            (1, "Peter", "Cheung", "MrBao123")
        """)
        db.commit()

    # Version print
    print(f"""
Version Info:
├ Tkinter {tkinter.TkVersion}5
├ Python {sys.version.split(' ')[0]}
└ MySQL Server {'.'.join([str(v) for v in db.get_server_version()])}
""")
# Tested fully on:
# Tkinter 8.6
# Python 3.12
# MySQL Server 8.0.35

cursor.execute("USE baobento")
# Execute Tkinter code
import gui