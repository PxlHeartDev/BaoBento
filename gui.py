# Library imports
from tkinter import *

# Explicit imports
from tkinter import messagebox, ttk

# Me imports
from main import db, cursor, setCustomerData
from sql import createAccount


# Functions

# Changes the current frame, displaying a messagebox if requested
def setFrame(frame: Frame, message = '', messageTitle = '', clear = False):
    frame.tkraise()
    if(message or messageTitle):
        messagebox.showinfo(messageTitle, message)
    if(clear):
        clearBoxes()

# Clears all entry boxes
def clearBoxes():
    firstName.set('')
    lastName.set('')
    number.set('')
    email.set('')
    password.set('')
    conPassword.set('')

    username.set('')
    accessKey.set('')

# Create and grid a text element in one or more frames
def createText(frames: list[Frame], row: int, column: int, span: int, text: str, font="Calibri 25", justify = 'center', padx = 0, pady = 0, sticky='news', rowspan=1):
    for f in frames:
        label = Label(f, text=text, fg='#ffed00', bg='#000000', font=font, justify=justify)
        label.grid(row=row, column=column, columnspan=span, padx=padx, pady=pady, sticky=sticky)
    return label

# Create and grid a button in one or more frames
def createButton(frames: list[Frame], row: int, column: int, span: int, text: str, command: None, font="Calibri 25", justify = 'center', fg = 'black', bg = 'white', width = 13, padx = 0, pady = 0, ipadx = 0, ipady = 0, rowspan=1, sticky=''):
    for f in frames:
        button = Button(f, text=text, justify=justify, font=font, fg=fg, bg=bg, width=width, command=command)
        button.grid(row=row, column=column, columnspan=span, rowspan=rowspan, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=sticky)
    return button

# Create and grid an entry box in one or more frames
def createEntryBox(frames: list[Frame], row: int, column: int, span: int, textVar: any, font="Calibri 22", justify = 'center', width = 18, ipadx=0, ipady=2, password=False, rowspan=1):
    for f in frames:
        entryBox = Entry(f, textvariable=textVar, justify=justify, font=font, width=width)
        entryBox.grid(row=row, column=column, columnspan=span, rowspan=rowspan, ipadx=ipadx, ipady=ipady)
        if(password):
            entryBox.config(show='*')

# Create and grid a dropdown menu in one or more frames
def createDropdown(frames: list[Frame], row: int, column: int, span: int, oList: list, selectedVar: StringVar, font: str, defaultText = '', width = 14, padx = 0, pady = 0, sticky=''):
    selectedVar.set(defaultText)
    for f in frames:
        optionsMenu = OptionMenu(f, selectedVar, *oList)
        optionsMenu.config(font=font, width=width)
        optionsMenu.grid(row=row, column=column, columnspan=span, padx=padx, pady=pady, sticky=sticky)
    return optionsMenu
        
# Create and grid a checkbox button in one or more frames
def createCheckbox(frames: list[Frame], row: int, column: int, span: int, text: str, variable, font="Calibri 25", justify = 'center', padx = 0, pady = 0, sticky='news', initVal=False):
    for f in frames:
        checkbox = Checkbutton(f, text=text, fg='#ffed00', bg='#000000', selectcolor='#000000', activebackground='#000000', variable=variable, onvalue=True, offvalue=False, font=font, justify=justify, command=lambda:variable.get())
        checkbox.grid(row=row, column=column, columnspan=span, padx=padx, pady=pady, sticky=sticky)                                                                                     # Don't ask, for some reason beyond my feeble comprehension the state of the checkbox can only
#                                                                                                                                                                                         take a non-falsy initial state when its variable is '.get()'d within the command of the box...
#                                                                                                                                                                                         Like, explicitly that. Retrieved within the command. Even if it's not used. It's like TF2 coconut.
        return checkbox


# Log into an existing customer account
def customerLogin():
    cursor.execute(f"SELECT * FROM customers WHERE email = '{email.get()}'")
    data = cursor.fetchone()
    if(not(data) or data[5] != password.get()):
        messagebox.showerror("Error", "Account not found or password incorrect")
        return
    setFrame(CustomerHome)
    messagebox.showinfo("Successfully logged in", f"Welcome to the Bao&Bento app, {data[1]}")
    setCustomerData(data)
    clearBoxes()

# Log into an employee account
def employeeLogin():
    cursor.execute(f"SELECT * FROM employees WHERE accessKey = '{accessKey.get()}'")
    data = cursor.fetchone()
    if(not(data) or username.get() != f"{data[1][0].lower()}{data[2].lower()}"):
        messagebox.showerror("Error", "Employee not found or access key incorrect")
        return
    if(data[0] != 1):
        setFrame(EmployeeMenu)
        messagebox.showinfo("Successfully logged in", f"Welcome, {data[1]}")
    else:
        setFrame(OwnerMenu)
        messagebox.showinfo("Successfully logged in", f"Logged in as owner\nWelcome, {data[1]}")
    clearBoxes()

# Log out of the system
def logout():
    if(messagebox.askyesno("Log Out", "Are you sure you wish to log out?")):
        destroyToplevels()
        clearBoxes()
        setFrame(MainMenu, "Successfully logged out", "Success")

def destroyToplevels():
    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()


# Return the entry box data as an array
def getEntryData():
    return [firstName.get(), lastName.get(), number.get(), email.get(), password.get(), conPassword.get()]

# Create root window
root = Tk()
root.geometry("1024x576")
root.title("Bao&Bento")
root.configure(background='#000000')

# Global/Input Vars
firstName = StringVar()
lastName = StringVar()
number = StringVar()
email = StringVar()
password = StringVar()
conPassword = StringVar()

username = StringVar()
accessKey = StringVar()



#####
##### Redo the 'No account yet?' and 'Got an account already?' thingies. They look weird.
#####


# Create frames
MainMenu = Frame(root, bg='#000000')

CustomerCreate = Frame(root, bg='#000000')
CustomerLogin = Frame(root, bg='#000000')
CustomerHome = Frame(root, bg='#000000')
CustomerCreateOrder = Frame(root, bg='#000000')
CustomerRewards = Frame(root, bg='#000000')
CustomerOrders = Frame(root, bg='#000000')
CustomerSettings = Frame(root, bg='#000000')

EmployeeMenu = Frame(root, bg='#000000')
EmployeeLogin = Frame(root, bg='#000000')
EmployeeSchedule = Frame(root, bg='#000000')

OwnerMenu = Frame(root, bg='#000000')
OwnerCreateOrder = Frame(root, bg='#000000')
OwnerOrders = Frame(root, bg='#000000')
OwnerManageCustomers = Frame(root, bg='#000000')
OwnerManageEmployees = Frame(root, bg='#000000')
OwnerEditMenu = Frame(root, bg='#000000')


# Grid the frames
for i in (MainMenu,
CustomerCreate, CustomerLogin, CustomerHome,
EmployeeMenu, EmployeeLogin, EmployeeSchedule,
OwnerMenu,
):
    i.grid(row=0, column=0, sticky='news')

#### Main menu frame #####
createButton([CustomerCreate, CustomerLogin, EmployeeLogin], 8, 0, 4, "Main Menu", lambda:[setFrame(MainMenu), clearBoxes()], "Calibri 22", width=40, padx=8, pady=5)

createText([MainMenu, CustomerHome], 0, 0, 3, "Bao&Bento", "Calibri 40 bold", 'center')
createButton([MainMenu], 1, 1, 1, "Customers", lambda:setFrame(CustomerCreate, "Create or log in to a customer account", "Customer Portal"), "Calibri 25")
createButton([MainMenu], 2, 1, 1, "Employees", lambda:setFrame(EmployeeLogin, "Your username will be your first initial then\nyour last name in all lower case (e.g. jdoe),\nand your access key would\nhave been specified by you", "Info"), "Calibri 25")
createButton([MainMenu], 3, 1, 1, "Quit", lambda:root.destroy(), "Calibri 20", pady=5)

##### Customer #####

### Customer Account Creation ###

# Title
createText([CustomerCreate], 0, 0, 4, "Create Account", "Calibri 35 bold")

# Buttons
createButton([CustomerCreate], 1, 3, 1, "Create Account", createAccount, "Calibri 20", width=16, padx=10)
createText([CustomerCreate], 9, 0, 1, "Got an account already?", "Calibri 16", pady=15, sticky='e')
createButton([CustomerCreate], 9, 1, 1, "Log in", lambda:setFrame(CustomerLogin, clear=True), "Calibri 20", width=16, pady=15)

# Data entry section for Customers
createText([CustomerCreate], 1, 0, 1, "First Name: ", pady=5, padx=38)
createEntryBox([CustomerCreate], 1, 1, 1, firstName, width=21)
createText([CustomerCreate], 2, 0, 1, "Last Name: ", pady=5, padx=38)
createEntryBox([CustomerCreate], 2, 1, 1, lastName, width=21)
createText([CustomerCreate], 3, 0, 1, "Ph. Number: ", pady=5, padx=38)
createEntryBox([CustomerCreate], 3, 1, 1, number, width=21)

# Also used for login
createText([CustomerCreate, CustomerLogin], 4, 0, 1, "Email: ", pady=5, padx=38)
createEntryBox([CustomerCreate, CustomerLogin], 4, 1, 1, email, font="Calibri 15", width=31, ipady=9)
createText([CustomerCreate, CustomerLogin], 5, 0, 1, "Password: ", pady=5, padx=38)
createEntryBox([CustomerCreate, CustomerLogin], 5, 1, 1, password, width=21, password=True)

createText([CustomerCreate], 6, 0, 1, "Confirm Password: ", pady=5, padx=38)
createEntryBox([CustomerCreate], 6, 1, 1, conPassword, width=21, password=True)

### Customer Login ###
createText([CustomerLogin], 0, 0, 4, "Customer Login", "Calibri 35 bold")
createButton([CustomerLogin], 4, 3, 1, "Login", customerLogin, "Calibri 18", rowspan=2, padx=6)
createText([CustomerLogin], 9, 0, 1, "No account yet?", "Calibri 16", pady=5, sticky='e')
createButton([CustomerLogin], 9, 1, 1, "Create Account", lambda:setFrame(CustomerCreate, clear=True), "Calibri 20", width=16, padx=10, rowspan=6)

### Customer Home ###
createText([CustomerHome], 1, 0, 4, "Home", "Calibri 35 bold")
createButton([CustomerHome], 2, 0, 1, "Menu/Create an Order", lambda:setFrame(CustomerCreateOrder), "Calibri 18", ipadx=38)
createButton([CustomerHome], 3, 0, 1, "Rewards", lambda:setFrame(CustomerRewards), "Calibri 18", ipadx=38)
createButton([CustomerHome], 4, 0, 1, "View Orders", lambda:setFrame(CustomerOrders), "Calibri 18", ipadx=38)
createButton([CustomerHome], 5, 0, 1, "Settings", lambda:createCustomerSettingsToplevel(), "Calibri 18", ipadx=38)
createButton([CustomerHome], 6, 0, 1, "Logout", lambda:logout(), "Calibri 18", ipadx=38)

##### Employee #####

### Login ###
createText([EmployeeLogin], 0, 0, 4, "Employee Login", "Calibri 35 bold")
createText([EmployeeLogin], 1, 0, 1, "Username: ", pady=5, padx=38)
createEntryBox([EmployeeLogin], 1, 1, 1, username, width=21)
createText([EmployeeLogin], 2, 0, 1, "Access Key: ", pady=5, padx=38)
createEntryBox([EmployeeLogin], 2, 1, 1, accessKey, width=21, password=True)
createButton([EmployeeLogin], 1, 3, 1, "Login", employeeLogin, "Calibri 18", padx=5)

# ##### Menu #####
# createText([EmployeeMenu], 1, 0, 4, "Employee Portal", "Calibri 35 bold")
# createButton([EmployeeMenu], 2, 0, 1, "Schedule", lambda:setFrame(EmployeeSchedule), "Calibri 18")
# createButton([EmployeeMenu], 3, 0, 1, "Logout", lambda:logout(), "Calibri 18")



##### Owner #####

### Menu ###
createText([OwnerMenu], 1, 0, 4, "Bao&Bento Management", "Calibri 35 bold")
createButton([OwnerMenu], 2, 0, 4, "Create an Order", lambda:createOwnerCreateOrderTopLevel(), "Calibri 18", ipadx=20)
createButton([OwnerMenu], 3, 0, 4, "View Orders", lambda:createOwnerViewOrdersToplevel(), "Calibri 18", ipadx=20)
createButton([OwnerMenu], 4, 0, 4, "Manage Customers", lambda:createOwnerManageCustomersToplevel(), "Calibri 18", ipadx=20)
createButton([OwnerMenu], 5, 0, 4, "Manage Employees", lambda:setFrame(OwnerManageEmployees), "Calibri 18", ipadx=20)
createButton([OwnerMenu], 6, 0, 4, "Logout", lambda:logout(), "Calibri 18", ipadx=20)

# Imported at the bottom to avoid a circular import error
from toplevels import *

# Initialize the GUI!
setFrame(MainMenu)
root.mainloop()