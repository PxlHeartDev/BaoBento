# Library imports
from tkinter import *
import time
import json
import math

# Explicit imports
from tkinter import messagebox, ttk
from tkinter.simpledialog import askinteger, askstring
from time import strftime

# Me imports
from main import db, cursor, getUserData
from gui import root, createText, createButton, createEntryBox, createDropdown, createCheckbox
from sql import retrieveCustomerOrders, deleteCustomer, updateDetails, updateEmail, updateNotif, updatePassword, addEmployee, deleteEmployee
from orders import Appetiser, Bao, Bento, Classic, Side
from documents import createOrderReceipt
from functions import floatToPrice, ordinal, monthToTime, months, truncateText, closedWindow, keyFromVal, keyFromValPrecise, indexFromVal, genExceptions, monthToInt, isLeapYear

# Global, for use with marking orders
global selectedOrder
selectedOrder = []

def getSelectedOrder():
    return selectedOrder

# Customer settings menu
def createCustomerSettingsToplevel():
    # Notification prefences variables
    emailNotif = IntVar()
    SMSNotif = IntVar()

    # Get the data of the logged in customer
    data = getUserData()
    
    # Get existing notification preferences
    notifPref = bin(data[6]).replace("0b", "").zfill(2)
    emailNotif.set(notifPref[1])
    SMSNotif.set(notifPref[0])

    # Create top level
    CustomerSettings = Toplevel(root, bg='#000000')
    CustomerSettings.geometry('1060x690')
    createText([CustomerSettings], 1, 0, 4, "Settings", "Calibri 35 bold")

    # Notification preferences
    createText([CustomerSettings], 2, 0, 1, "Notification Preferences: ", pady=5, padx=38)
    createText([CustomerSettings], 3, 0, 1, "Note: This preference only affects promotional messages\nConfirmation messages regarding orders or otherwise will always be sent", "Calibri 12", pady=5, padx=38, sticky='n')
    e = createCheckbox([CustomerSettings], 2, 1, 1, "Email", emailNotif, initVal=(notifPref[1] == "1"))
    s = createCheckbox([CustomerSettings], 2, 2, 1, "SMS", SMSNotif, initVal=(notifPref[0] == "1"))
    createButton([CustomerSettings], 3, 1, 1, "Confirm Preferences", lambda:updateNotif(data[0], SMSNotif.get(), emailNotif.get(), CustomerSettings), "Calibri 15", width=18, padx=5, pady=8, sticky='n')
    

    ### Edit details section ###

    # Re-use entry boxes
    from gui import firstName, lastName, number, email, password, conPassword

    # Set the entry boxes
    firstName.set(data[1])
    lastName.set(data[2])
    number.set(data[3])
    email.set(data[4])

    # Personal details
    createText([CustomerSettings], 4, 0, 1, "First Name: ", pady=5, padx=38)
    createEntryBox([CustomerSettings], 4, 1, 1, firstName, width=21)
    createText([CustomerSettings], 5, 0, 1, "Last Name: ", pady=5, padx=38)
    createEntryBox([CustomerSettings], 5, 1, 1, lastName, width=21)
    createText([CustomerSettings], 6, 0, 1, "Ph. Number: ", pady=5, padx=38)
    createEntryBox([CustomerSettings], 6, 1, 1, number, width=21)
    createButton([CustomerSettings], 5, 2, 1, "Update Details", lambda:updateDetails(data[0], firstName.get(), lastName.get(), number.get(), CustomerSettings), "Calibri 15", width=15, padx=5)

    # Email
    createText([CustomerSettings], 7, 0, 1, "Email: ", pady=20, padx=38)
    createEntryBox([CustomerSettings], 7, 1, 1, email, font="Calibri 15", width=31, ipady=9)
    createButton([CustomerSettings], 7, 2, 1, "Update Email", lambda:updateEmail(data[0], email.get(), CustomerSettings), "Calibri 15", width=15, padx=5)

    # Password
    createText([CustomerSettings], 8, 0, 1, "New Password: ", pady=5, padx=38)
    createEntryBox([CustomerSettings], 8, 1, 1, password, width=21, password=True)
    createText([CustomerSettings], 9, 0, 1, "Old Password: ", pady=5, padx=38)
    createEntryBox([CustomerSettings], 9, 1, 1, conPassword, width=21, password=True)
    createButton([CustomerSettings], 8, 2, 1, "Update Password", lambda:updatePassword(data[0], password.get(), conPassword.get(), CustomerSettings), "Calibri 15", width=15, padx=5, rowspan=2)

    # Delete account
    createButton([CustomerSettings], 10, 0, 4, "Delete Account", lambda:deleteCustomer(getUserData()[0], CustomerSettings), "Calibri 18", width=15)
    
    # Back
    createButton([CustomerSettings], 11, 0, 4, "Back", lambda:CustomerSettings.destroy(), "Calibri 18", pady=5, width=20)

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

# Owner menu for creating a new order
def createOwnerCreateOrderTopLevel(customerID = 0):
    # Create top level
    OwnerCreateOrder = Toplevel(root, bg='#000000')
    OwnerCreateOrder.geometry('960x690')

    # Title and buttons
    createText([OwnerCreateOrder], 1, 0, 4, "Create Order", "Calibri 35 bold")
    createButton([OwnerCreateOrder], 2, 0, 4, "Appetisers", lambda:createOwnerAddItemTopLevel("appetisers"), "Calibri 30")
    createButton([OwnerCreateOrder], 3, 0, 4, "Baos", lambda:createOwnerAddItemTopLevel("baos"), "Calibri 30")
    createButton([OwnerCreateOrder], 4, 0, 4, "Bentos", lambda:createOwnerAddItemTopLevel("bentos"), "Calibri 30")
    createButton([OwnerCreateOrder], 5, 0, 4, "Classics", lambda:createOwnerAddItemTopLevel("classics"), "Calibri 30")
    createButton([OwnerCreateOrder], 6, 0, 4, "Sides", lambda:createOwnerAddItemTopLevel("sides"), "Calibri 30")

    # Complete the order, asking for some details
    def completeOrder():
        # Ask to assign a customer ID if it's the owner placing the order
        if(customerID == 1): o.assignCustomer(askinteger("Customer ID", "Enter a customer ID to assign the order to. Use 1 if none.", initialvalue=1, parent=OwnerCreateOrder))
        o.completeOrder(
            askinteger("Pickup time", "Please enter a pickup time in seconds since Jan 1 2024, 00:00 UTC+0", parent=OwnerCreateOrder),
            askstring("Notes", "Please enter any notes about the order, such as allergens or specific requests", parent=OwnerCreateOrder)
        )
        messagebox.showinfo("Success", "Successfully placed order", parent=OwnerCreateOrder)
        OwnerCreateOrder.destroy()

    # More buttons
    createButton([OwnerCreateOrder], 7, 0, 4, "View order", lambda:createOrderReceipt(OwnerCreateOrder, o.getOrderContent()))
    createButton([OwnerCreateOrder], 8, 0, 4, "Complete order", completeOrder)


    # Import here to circumvent circular import issues
    from orders import Order, modTypes, sauceDict

    # Order object
    o = Order()
    if(customerID != 0):
        o.assignCustomer(customerID)

    # Sub-function, creates the "Add Item" top level
    def createOwnerAddItemTopLevel(type: str):
        # Create top level
        OwnerAddItem = Toplevel(root, bg='#000000')
        OwnerAddItem.geometry('1200x960')

        # Check the item type
        match(type):
            case("appetisers"):

                # Import
                from orders import appetisers, appetiserPermittedSauces

                # Store the auto-generated UI elements and variables in a list so they can be easily accessed
                UIElements = []
                vars = []
                
                # Sub-sub-function, runs when the appetiser in the dropdown is changed
                def appetiserChanged(*args):
                    # Ignore if it is the init value
                    if('selected' in appetiserSelected.get()): return
                    # Get the appetiser details in full
                    appStuff = appetisers[keyFromVal(appetisers, appetiserSelected.get())]
                    # Re-used options list
                    oListMod = []
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements]
                    
                    # Clear the lists
                    UIElements.clear()
                    vars.clear()

                    # Item description
                    UIElements.append(createText([OwnerAddItem], 3, 0, 4, f'{appStuff['desc']}', 'Calibri 15'))

                    # Generation modifier dropdown(s)
                    for i in range(0, len(appStuff['mod'])):
                        m = appStuff['mod'][i]
                        oListMod.clear()
                        vars.append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements.append(createText([OwnerAddItem], 5+i, 0, 1, f"{m['name']}: "))
                        UIElements.append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListMod, vars[i], "Calibri 15 bold", modTypes[m['modType']][m['default']], 24))

                    # Generate sauce dropdown if sauce is allowed for this item
                    if(appStuff['defaultSauce'] != -1):
                        oListSauce = []
                        for i in appetiserPermittedSauces:
                            oListSauce.append(sauceDict[i])
                        # Replace "Micro Curry" with "Small Curry" if small is the default
                        if(appStuff['defaultSauce'] == 3):
                            oListSauce[2] = "Small Curry"
                        UIElements.append(createDropdown([OwnerAddItem], 5, 2, 1, oListSauce, sauceSelected, "Calibri 15 bold", sauceDict[appStuff['defaultSauce']], 24, 5))
                    # No sauce allowed
                    else:
                        sauceSelected.set("")
                        UIElements.append(createText([OwnerAddItem], 5, 2, 1, "No sauce", "Calibri 20"))
                    
                    # Final button
                    UIElements.append(createButton([OwnerAddItem], 9, 1, 4, "Add Item", addAppetiser, "Calibri 20", pady=5))

                # Add the item to the order
                def addAppetiser():
                    o.addItem(Appetiser(
                        count.get(),
                        keyFromVal(appetisers, appetiserSelected.get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars],
                        keyFromVal(sauceDict, sauceSelected.get()),
                        note.get()))
                    messagebox.showinfo("Success", "Successfully added Appetiser to order", parent=OwnerAddItem)
                    OwnerAddItem.destroy()

                # Overhead vars and UI stuff
                createText([OwnerAddItem], 1, 0, 4, "Appetisers", "Calibri 35 bold")
                oListApp = []
                for a in appetisers.values():
                    oListApp.append(a['name'])
                appetiserSelected = StringVar()
                sauceSelected = StringVar()
                appetiserSelected.trace_add("write", appetiserChanged)
                createText([OwnerAddItem], 2, 0, 1, "Appetiser: ")
                createDropdown([OwnerAddItem], 2, 1, 1, oListApp, appetiserSelected, "Calibri 15 bold", "No appetiser selected", 24)

                count = IntVar()
                createDropdown([OwnerAddItem], 2, 2, 1, [1, 2, 3, 4, 5], count, "Calibri 15 bold", 1, 5)
                
                createText([OwnerAddItem], 4, 0, 2, "Modifiers: ", sticky='s', pady=10)
                createText([OwnerAddItem], 4, 2, 2, "Sauce: ", sticky='s', pady=10)

                note = StringVar()
                createText([OwnerAddItem], 8, 0, 1, "Notes: ", "Calibri 20", pady=10)
                createEntryBox([OwnerAddItem], 8, 1, 2, note, "Calibri 20", width=30, ipadx=30)

            case("baos"):
                # Import
                from orders import baos, baoPermittedSauces, picklesDict

                # Store the auto-generated UI elements and variables in a list so they can be easily accessed
                UIElements = []
                sauceAm = []
                vars = []

                # Runs when the sauce has been changed
                def sauceChanged(*args):
                    [s.destroy() for s in sauceAm]
                    sauceAm.clear()
                    if('No' in sauceSelected.get()):
                        return
                    sauceAm.append(createDropdown([OwnerAddItem], 6, 2, 1, ["Less", "With", "Extra"], vars[0], "Calibri 15 bold", 'With', 15))

                # Runs when the bao meat has been changed
                def baoChanged(*args):
                    # Ignore if it is the init value
                    if('selected' in baoSelected.get()): return
                    # Get the bao details
                    baoStuff = baos[keyFromVal(baos, baoSelected.get())]
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements]
                        
                    # Clear the lists
                    UIElements.clear()
                    vars.clear()

                    # Item description
                    UIElements.append(createText([OwnerAddItem], 3, 0, 4, f'{baoStuff['desc']}', 'Calibri 15'))

                    # Add a new var to the list
                    vars.append(StringVar())
                    
                    # Pickles dropdown
                    oListPickles = []
                    for v in modTypes[1].values():
                        oListPickles.append(v)
                    for i in range(0, 5):
                        vars.append(StringVar())
                        UIElements.append(createText([OwnerAddItem], 5+i, 0, 1, f"{picklesDict[i+1]}: "))
                        UIElements.append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListPickles, vars[i+1], "Calibri 15 bold", modTypes[1][baoStuff['pickles'][i]], 8))

                    # Sauce dropdown
                    oListSauce = []
                    for i in baoPermittedSauces:
                        oListSauce.append(sauceDict[i])
                    UIElements.append(createDropdown([OwnerAddItem], 5, 2, 1, oListSauce, sauceSelected, "Calibri 15 bold", sauceDict[baoStuff['sauce']], 15, 5))
                    
                    # Final button
                    UIElements.append(createButton([OwnerAddItem], 12, 1, 4, "Add Item", addBao, "Calibri 20", pady=5))

                # Add the item to the order
                def addBao():
                    o.addItem(Bao
                            (1, 
                            keyFromVal(baos, baoSelected.get()),
                            keyFromVal(sauceDict, sauceSelected.get()),
                            keyFromVal(modTypes[1], vars[0].get()),
                            [keyFromVal(modTypes[1], m.get()) for m in vars[1:]],
                            note.get()))
                    messagebox.showinfo("Success", "Successfully added Bao to order", parent=OwnerAddItem)
                    OwnerAddItem.destroy()

                # Set all pickles to no
                def noPickles():
                    for v in vars[1:]:
                        v.set("No")

                # Overhead vars and UI stuff
                createText([OwnerAddItem], 1, 0, 4, "Baos", "Calibri 35 bold")
                oListBao = []
                for b in baos.values():
                    oListBao.append(b['name'])
                baoSelected = StringVar()
                sauceSelected = StringVar()
                baoSelected.trace_add("write", baoChanged)
                sauceSelected.trace_add("write", sauceChanged)
                createText([OwnerAddItem], 2, 0, 1, "Bao: ")
                createDropdown([OwnerAddItem], 2, 1, 1, oListBao, baoSelected, "Calibri 15 bold", "No bao selected", 15)

                count = IntVar()
                createDropdown([OwnerAddItem], 2, 2, 1, [1, 2, 3, 4, 5], count, "Calibri 15 bold", 1, 5)

                createText([OwnerAddItem], 4, 0, 3, "Pickles: ", sticky='s', pady=10)
                createText([OwnerAddItem], 4, 2, 2, "Sauce: ", sticky='s', pady=10)

                createButton([OwnerAddItem], 8, 2, 1, "No Pickles", noPickles, "Calibri 15")

                note = StringVar()
                createText([OwnerAddItem], 11, 0, 1, "Notes: ", "Calibri 20", pady=10)
                createEntryBox([OwnerAddItem], 11, 1, 2, note, "Calibri 20", width=30, ipadx=30)

            # The rest of these won't be commented out fully. They're mostly the same with bits changed around
            case("bentos"):

                # Import here because idk honestly man I'm tired, probably circular import circumvention or something
                from orders import bentos, bentoSides, bentoPermittedSauces

                # Store the auto-generated UI elements and variables in a list so they can be easily accessed and cleared out
                UIElements = [[], [], []]
                vars = [[], [], []]
                
                # Sub-sub-function, runs when the bento in the dropdown is changed
                def bentoChanged(*args):
                    # Ignore if it is the init value
                    if('selected' in bentoSelected.get()): return
                    # Get the bento details in full
                    bentoStuff = bentos[keyFromVal(bentos, bentoSelected.get())]
                    bentoSide1 = bentoSides[keyFromVal(bentoSides, bentoSideSelected[0].get())]
                    bentoSide2 = bentoSides[keyFromVal(bentoSides, bentoSideSelected[1].get())]
                    # Re-used options list
                    oListMod = []
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements[0]]
                    
                    # Clear the lists
                    UIElements[0].clear()
                    vars[0].clear()

                    UIElements.append(createText([OwnerAddItem], 3, 0, 4, f'{bentoStuff['desc']}', 'Calibri 15'))

                    for i in range(0, len(bentoStuff['mod'])):
                        m = bentoStuff['mod'][i]
                        oListMod.clear()
                        vars[0].append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements[0].append(createText([OwnerAddItem], 5+i, 0, 1, f"{m['name']}: "))
                        UIElements[0].append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListMod, vars[0][i], "Calibri 15 bold", modTypes[m['modType']][m['default']], 24))

                    oListBento.clear()
                    for a in bentoSides.values():
                        oListBento.append(a['name'])
                    UIElements[0].append(createText([OwnerAddItem], 10, 0, 2, "Side 1: "))
                    UIElements[0].append(createDropdown([OwnerAddItem], 11, 1, 1, oListBento, bentoSideSelected[0], "Calibri 15 bold", bentoSides[bentoStuff['side1'][0]]['name'], 24))
                    
                    UIElements[0].append(createText([OwnerAddItem], 20, 0, 2, "Side 2: "))
                    UIElements[0].append(createDropdown([OwnerAddItem], 21, 1, 1, oListBento, bentoSideSelected[1], "Calibri 15 bold", bentoSides[bentoStuff['side2'][0]]['name'], 24))

                    if(bentoStuff['sauce'] != -1):
                        oListSauce = []
                        for i in bentoPermittedSauces:
                            oListSauce.append(sauceDict[i])
                        UIElements[0].append(createDropdown([OwnerAddItem], 5, 2, 1, oListSauce, sauceSelected, "Calibri 15 bold", sauceDict[bentoStuff['sauce']], 24, 5))
                    else:
                        sauceSelected.set("")
                        UIElements[0].append(createText([OwnerAddItem], 5, 2, 2, "No sauce", "Calibri 20"))
                    UIElements[0].append(createButton([OwnerAddItem], 26, 3, 4, "Add Item", addBento, "Calibri 20", pady=5))


                def bentoSideChanged(side: int):
                    s = side - 1
                    # Ignore if it is the init value
                    if(not(bentoSideSelected[s].get())): return
                    # Get the side details in full
                    bentoSideStuff = bentoSides[keyFromVal(bentoSides, bentoSideSelected[s].get())]
                    # Re-used options list
                    oListMod = []
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements[side]]
                    
                    # Clear the lists
                    UIElements[side].clear()
                    vars[side].clear()

                    for i in range(0, len(bentoSideStuff['mod'])):
                        m = bentoSideStuff['mod'][i]
                        oListMod.clear()
                        vars[side].append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements[side].append(createText([OwnerAddItem], (side*10)+1+i, 2, 1, f"{m['name']}: ", "Calibri 15"))
                        UIElements[side].append(createDropdown([OwnerAddItem], (side*10)+1+i, 3, 1, oListMod, vars[side][i], "Calibri 13 bold", modTypes[m['modType']][m['default']], 18))

                def addBento():
                    o.addItem(Bento(
                        count.get(),
                        keyFromVal(bentos, bentoSelected.get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars[0]],

                        keyFromVal(bentoSides, bentoSideSelected[0].get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars[1]],

                        keyFromVal(bentoSides, bentoSideSelected[1].get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars[2]],
                        keyFromValPrecise(sauceDict, sauceSelected.get()),
                        1,
                        note.get()))
                    messagebox.showinfo("Success", "Successfully added Bento to order", parent=OwnerAddItem)
                    OwnerAddItem.destroy()

                createText([OwnerAddItem], 1, 0, 4, "Bentos", "Calibri 35 bold")
                oListBento = []
                for a in bentos.values():
                    oListBento.append(a['name'])
                bentoSelected = StringVar()
                bentoSideSelected = [StringVar(), StringVar()]
                bentoSelected.trace_add("write", bentoChanged)
                bentoSideSelected[0].trace_add("write", lambda x,y,z:bentoSideChanged(1))
                bentoSideSelected[1].trace_add("write", lambda x,y,z:bentoSideChanged(2))
                sauceSelected = StringVar()
                createText([OwnerAddItem], 2, 0, 1, "Bento: ")
                createDropdown([OwnerAddItem], 2, 1, 1, oListBento, bentoSelected, "Calibri 15 bold", "No bento selected", 24)

                count = IntVar()
                createDropdown([OwnerAddItem], 2, 2, 1, [1, 2, 3, 4, 5], count, "Calibri 15 bold", 1, 5)

                createText([OwnerAddItem], 4, 0, 2, "Modifiers: ", sticky='s', pady=10)
                createText([OwnerAddItem], 4, 2, 2, "Sauce: ", sticky='s', pady=10)

                note = StringVar()
                createText([OwnerAddItem], 26, 0, 1, "Notes: ", "Calibri 20", pady=10)
                createEntryBox([OwnerAddItem], 26, 1, 2, note, "Calibri 20", width=30, ipadx=30)

            case("classics"):
                # Import here because idk honestly man I'm tired, probably circular import circumvention or something
                from orders import classics, classicSides

                # Store the auto-generated UI elements and variables in a list so they can be easily accessed
                UIElements = [[], []]
                vars = [[], []]
                
                # Sub-sub-function, runs when the classic in the dropdown is changed
                def classicChanged(*args):
                    # Ignore if it is the init value
                    if('selected' in classicSelected.get()): return
                    # Get the classic details in full
                    classicStuff = classics[keyFromVal(classics, classicSelected.get())]
                    # Re-used options list
                    oListMod = []
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements[0]]
                    
                    # Clear the lists
                    UIElements[0].clear()
                    vars[0].clear()

                    UIElements.append(createText([OwnerAddItem], 3, 0, 4, f'{classicStuff['desc']}', 'Calibri 15'))

                    for i in range(0, len(classicStuff['mod'])):
                        m = classicStuff['mod'][i]
                        oListMod.clear()
                        vars[0].append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements[0].append(createText([OwnerAddItem], 5+i, 0, 1, f"{m['name']}: "))
                        UIElements[0].append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListMod, vars[0][i], "Calibri 15 bold", modTypes[m['modType']][m['default']], 24))

                    if(classicStuff['side'] != -1):
                        oListSides = []
                        for i in list(classicSides.values()):
                            oListSides.append(i['name'])
                        UIElements[0].append(createDropdown([OwnerAddItem], 5, 3, 1, oListSides, sideSelected, "Calibri 15 bold", classicSides[classicStuff['side']]['name'], 24, 5))
                    else:
                        sideSelected.set("")
                        UIElements[0].append(createText([OwnerAddItem], 5, 2, 1, "No side", "Calibri 20"))
                    
                    UIElements[0].append(createButton([OwnerAddItem], 13, 1, 4, "Add Item", addClassic, "Calibri 20", pady=5))


                def sideChanged(*args):
                    # Ignore if it is the init value
                    if(not(sideSelected.get())): return
                    # Get the side details in full
                    sideStuff = classicSides[keyFromVal(classicSides, sideSelected.get())]
                    # Re-used options list
                    oListMod = []
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements[1]]
                    
                    # Clear the lists
                    UIElements[1].clear()
                    vars[1].clear()

                    for i in range(0, len(sideStuff['mod'])):
                        m = sideStuff['mod'][i]
                        oListMod.clear()
                        vars[1].append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements[1].append(createText([OwnerAddItem], 6+i, 2, 1, f"{m['name']}: ", "Calibri 15"))
                        UIElements[1].append(createDropdown([OwnerAddItem], 6+i, 3, 1, oListMod, vars[1][i], "Calibri 13 bold", modTypes[m['modType']][m['default']], 18))

                def addClassic():
                    o.addItem(Classic(
                        count.get(),
                        keyFromVal(classics, classicSelected.get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars[0]],
                        keyFromVal(classicSides, sideSelected.get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars[1]],
                        note.get()))
                    messagebox.showinfo("Success", "Successfully added Classic to order", parent=OwnerAddItem)
                    OwnerAddItem.destroy()

                createText([OwnerAddItem], 1, 0, 4, "Classics", "Calibri 35 bold")
                oListCla = []
                for a in classics.values():
                    oListCla.append(a['name'])
                classicSelected = StringVar()
                sideSelected = StringVar()
                classicSelected.trace_add("write", classicChanged)
                sideSelected.trace_add("write", sideChanged)
                createText([OwnerAddItem], 2, 0, 1, "Classic: ")
                createDropdown([OwnerAddItem], 2, 1, 1, oListCla, classicSelected, "Calibri 15 bold", "No classic selected", 24)

                count = IntVar()
                createDropdown([OwnerAddItem], 2, 2, 1, [1, 2, 3, 4, 5], count, "Calibri 15 bold", 1, 5)

                createText([OwnerAddItem], 4, 0, 2, "Modifiers: ", sticky='s', pady=10)
                createText([OwnerAddItem], 4, 2, 2, "Side: ", sticky='s', pady=10)

                note = StringVar()
                createText([OwnerAddItem], 12, 0, 1, "Notes: ", "Calibri 20", pady=10)
                createEntryBox([OwnerAddItem], 12, 1, 2, note, "Calibri 20", width=30, ipadx=30)
            case("sides"):

                # Import here because idk honestly man I'm tired, probably circular import circumvention or something
                from orders import sides

                # Store the auto-generated UI elements and variables in a list so they can be easily accessed
                UIElements = []
                vars = []

                def sideChanged(*args):
                    # Ignore if it is the init value
                    if('selected' in sideSelected.get()): return
                    # Get the side details in full
                    sideStuff = sides[keyFromVal(sides, sideSelected.get())]
                    # Re-used options list
                    oListMod = []
                    
                    # Destroy each auto-generated UI element
                    [e.destroy() for e in UIElements]
                    
                    # Clear the lists
                    UIElements.clear()
                    vars.clear()

                    UIElements.append(createText([OwnerAddItem], 3, 0, 4, f'{sideStuff['desc']}', 'Calibri 15'))

                    for i in range(0, len(sideStuff['mod'])):
                        m = sideStuff['mod'][i]
                        oListMod.clear()
                        vars.append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements.append(createText([OwnerAddItem], 5+i, 0, 1, f"{m['name']}: ", "Calibri 15"))
                        UIElements.append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListMod, vars[i], "Calibri 13 bold", modTypes[m['modType']][m['default']], 18))

                    UIElements.append(createButton([OwnerAddItem], 13, 1, 4, "Add Item", addSide, "Calibri 20", pady=5))

                def addSide():
                    o.addItem(Side(
                        count.get(),
                        keyFromVal(sides, sideSelected.get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars],
                        note.get()))
                    messagebox.showinfo("Success", "Successfully added Side to order", parent=OwnerAddItem)
                    OwnerAddItem.destroy()

                createText([OwnerAddItem], 1, 0, 4, "Sides", "Calibri 35 bold")
                oListSid = []
                for a in sides.values():
                    oListSid.append(a['name'])
                sideSelected = StringVar()
                sideSelected.trace_add("write", sideChanged)
                createText([OwnerAddItem], 2, 0, 1, "Side: ")
                createDropdown([OwnerAddItem], 2, 1, 1, oListSid, sideSelected, "Calibri 15 bold", "No side selected", 24)

                count = IntVar()
                createDropdown([OwnerAddItem], 2, 2, 1, [1, 2, 3, 4, 5], count, "Calibri 15 bold", 1, 5)

                createText([OwnerAddItem], 4, 0, 2, "Modifiers: ", sticky='s', pady=10)

                note = StringVar()
                createText([OwnerAddItem], 12, 0, 1, "Notes: ", "Calibri 20", pady=10)
                createEntryBox([OwnerAddItem], 12, 1, 2, note, "Calibri 20", width=30, ipadx=30)



#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


#


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

# Top level that lets the owner view all orders in the system
def createOwnerViewOrdersToplevel():
    OwnerViewOrders = Toplevel(root, bg='#000000')
    OwnerViewOrders.protocol("WM_DELETE_WINDOW", lambda: closedWindow(OwnerViewOrders))
    createText([OwnerViewOrders], 1, 0, 4, "View Orders", "Calibri 35 bold")

    # Main order treeview
    columns = ("oid", "cid", "data", "com", "paid", "ptime", "pktime")
    headings = ("Order ID", "Customer ID", "Order Data", "Completed?", "Paid?", "Placement Time", "Pickup Time")
    widths = (100, 100, 100, 80, 80, 180, 180)

    treeview = ttk.Treeview(OwnerViewOrders, columns=columns, show='headings', padding=1, selectmode='browse')
    treeview.grid(row = 3, column = 0, columnspan=5, padx=10)

    # Second treeview that shows order details
    orderTreeview = ttk.Treeview(OwnerViewOrders, padding=3, columns=["title", "price"], show='headings')
    orderTreeview.grid(row=3, column=5, padx=10, columnspan=2)
    orderTreeview.column("title", anchor='w', width=400)
    orderTreeview.column("price", anchor='w', width=100)
    orderTreeview.heading("title", text='No order selected', anchor='center')

    # Populate the main order treeview 
    def populate(filter=""):
        # Delete all existing rows
        treeview.delete(*treeview.get_children())
        
        # Get orders
        cursor.execute(f"""SELECT * FROM orders {filter}""")
        data = cursor.fetchall()

        for d in data:
            # Item count solving
            itemCount = sum([sum([i['count'] for i in v]) for v in json.loads(d[2]).values()])
            treeview.insert("", END, values=[
                d[0], 
                d[1], 
                f"{itemCount} item{'s' if itemCount > 1 else ''}", 
                "Yes" if d[3] else "No", "Yes" if d[4] else "No", 
                strftime("%a, %d %b %Y %H:%M", time.localtime(d[5] + 1704067200)), 
                strftime("%a, %d %b %Y %H:%M", time.localtime(d[6] + 1704067200))
            ])
            # Bind the select event to the orderSelected() function
            treeview.bind('<<TreeviewSelect>>', lambda event: orderSelected(event, orderTreeview))
        for c, h, w in zip(columns, headings, widths):
            treeview.column(c, anchor='center', width=w)
            treeview.heading(c, text=h, anchor='center')

    # Mark or unmark an order as complete in the system
    def markComplete():
        global selectedOrder
        if(not(selectedOrder)):
            messagebox.showerror("Error", "No order selected", parent=treeview)
            return
        cursor.execute(f"UPDATE orders SET complete = {0 if selectedOrder[3] == 'Yes' else 1} WHERE orderID = {selectedOrder[0]};")
        db.commit()
        
    # Mark or unmark an order as paid for in the system
    def markPaid():
        global selectedOrder
        if(not(selectedOrder)):
            messagebox.showerror("Error", "No order selected", parent=treeview)
            return
        cursor.execute(f"UPDATE orders SET paid = {0 if selectedOrder[4] == 'Yes' else 1} WHERE orderID = {selectedOrder[0]};")
        db.commit()

    # Action buttons
    buttonFont = 'Calibri 18'
    createText([OwnerViewOrders], 4, 0, 1, "Filter:", pady=8)
    createButton([OwnerViewOrders], 4, 1, 1, "All", command=lambda: populate(""), font=buttonFont)
    createButton([OwnerViewOrders], 4, 2, 1, "Active", command=lambda: populate("WHERE complete = 0"), font=buttonFont)
    createButton([OwnerViewOrders], 4, 3, 1, "Complete", command=lambda: populate("WHERE complete = 1"), font=buttonFont)
    createButton([OwnerViewOrders], 4, 4, 1, "Outstanding", command=lambda: populate("WHERE complete = 1 AND paid = 0"), font=buttonFont)

    createButton([OwnerViewOrders], 4, 5, 1, "Mark Complete", command=markComplete, font=buttonFont)
    createButton([OwnerViewOrders], 4, 6, 1, "Mark Paid", command=markPaid, font=buttonFont)
    createText([OwnerViewOrders], 5, 5, 2, "Make sure to check that you have the right\norder and to refresh after marking orders!", font="Calibri 10")

    createButton([OwnerViewOrders], 5, 2, 2, "View Order Receipt", command=lambda:createOrderReceipt(OwnerViewOrders), font=buttonFont, width=20)

    # Populate when the menu opens for the first time
    populate()




#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

# Owner customer management
def createOwnerManageCustomersToplevel():
    OwnerManageCustomers = Toplevel(root, bg='#000000')
    OwnerManageCustomers.geometry('1230x500')
    createText([OwnerManageCustomers], 1, 0, 4, "Manage Customers", "Calibri 35 bold")

    # Treeview stuff
    columns = ("cid", "fn", "ln", "pn", "em", "pw")
    headings = ("Customer ID", "First Name", "Last Name", "Phone Number", "Email", "Password")

    treeview = ttk.Treeview(OwnerManageCustomers, columns=columns, show='headings', padding=1, selectmode='browse')

    # Get customer data
    cursor.execute(f"SELECT * FROM customers")
    data = cursor.fetchall()

    # Populate treeview
    for d in data:
        treeview.insert("", END, values=d)
    for c, h in zip(columns, headings):
        treeview.heading(c, text=h)
    treeview.grid(row = 3, column = 0, padx=10)

    # Bind the selected event to the customerSelected() function
    treeview.bind('<<TreeviewSelect>>', lambda event: customerSelected(event, treeview))

# Open the moderation top level when a customer is clicked on
def customerSelected(event, tree):
    selected_items = event.widget.selection()
    if selected_items:
        item = selected_items[0]
        record = event.widget.item(item)['values']
        createOwnerModerationToplevel(record)

#############################################################################################################################

# Customer moderation, allows the owner to see orders that a specific customer has placed
# Will soon include other stuff such as blacklisting emails and phone numbers
def createOwnerModerationToplevel(customer: list):
    OwnerManageIndividual = Toplevel(root, bg='#000000')
    createText([OwnerManageIndividual], 1, 0, 4, "Manage Customer", "Calibri 35 bold")
    createText([OwnerManageIndividual], 2, 0, 4, f"{customer[0]}, {customer[1]} {customer[2]}", "Calibri 20 bold")

    # View the customer's individual order history
    createButton([OwnerManageIndividual], 3, 0, 4, "View Order History", lambda:createOwnerViewCustomerOrdersToplevel(customer), "Calibri 18", ipadx=15)

#############################################################################################################################

# View orders filtered by a customer ID
def createOwnerViewCustomerOrdersToplevel(customer):
    OwnerViewCustomerOrders= Toplevel(root, bg='#000000')
    OwnerViewCustomerOrders.protocol("WM_DELETE_WINDOW", lambda: closedWindow(OwnerViewCustomerOrders))
    OwnerViewCustomerOrders.geometry("1500x500")
    createText([OwnerViewCustomerOrders], 1, 0, 4, "Order History", "Calibri 35 bold")
    createText([OwnerViewCustomerOrders], 2, 0, 4, f"{customer[0]}, {customer[1]} {customer[2]}", "Calibri 20 bold")

    # Get customer's orders
    data = retrieveCustomerOrders(customer[0])

    # Treeview stuff
    columns = ("oid", "data", "com", "paid", "ptime", "pktime")
    headings = ("Order ID", "Order Data", "Completed?", "Paid?", "Placement Time", "Pickup Time")
    widths = (100, 100, 80, 80, 180, 180)
    treeview = ttk.Treeview(OwnerViewCustomerOrders, columns=columns, show='headings', padding=1, selectmode='browse')

    orderTreeview = ttk.Treeview(OwnerViewCustomerOrders, padding=3, columns=["title", "price"], show='headings')
    orderTreeview.grid(row=3, column=1, padx=10, columnspan=2)
    orderTreeview.column("title", anchor='w', width=400)
    orderTreeview.column("price", anchor='w', width=100)
    orderTreeview.heading("title", text='No order selected', anchor='center')

    # More treeview stuff
    for d in data:
        itemCount = sum([sum([i['count'] for i in v]) for v in json.loads(d[2]).values()])
        treeview.insert("", END, values=[d[0], f"{itemCount} item{'s' if itemCount > 1 else ''}", "Yes" if d[3] else "No", "Yes" if d[4] else "No",  strftime("%a, %d %b %Y %H:%M", time.localtime(d[5] + 1704067200)), strftime("%a, %d %b %Y %H:%M:%S", time.localtime(d[6] + 1704067200))])
        treeview.bind('<<TreeviewSelect>>', lambda event: orderSelected(event, orderTreeview))
    for c, h, w in zip(columns, headings, widths):
        treeview.column(c, anchor='center', width=w)
        treeview.heading(c, text=h, anchor='center')
    treeview.grid(row = 3, column = 0, padx=10)

#############################################################################################################################

# Runs when an order is selected in the order treeview
# Kind of useless because of the receipt system but I kept it because
# 1: I worked hard on it. 2: It's neat I guess. 3: It can be used to quickly check the rough details of an order.
def orderSelected(event, tree):
    selectedItems = event.widget.selection()
    if selectedItems:
        item = selectedItems[0]
        record = event.widget.item(item)['values']
        # Set the selectedOrder global var to the retrieved treeview row
        global selectedOrder
        selectedOrder = record

        # Get order data
        cursor.execute(f"""SELECT *  FROM orders WHERE orderID = {record[0]}""")
        orderData = cursor.fetchone()[2]

        # Treeview stuff
        tree.heading("title", text=f'Order {record[0]}', anchor='center')
        tree.heading("price", text='Price:', anchor='center')

        # Delete old data
        tree.delete(*tree.get_children())

        totalPrice = 0.00

        # Iterate through all the items in the order data
        # Processes the data into readable information and places it in the treeview
        # Modifiers and sides for a particular item will appear when double clicked
        # Price per item, per section, and the total of the order is calculated along the way
        for k, v in json.loads(orderData).items():
            order = tree.insert("", END, values=[f"[{sum([i['count'] for i in v])}] {k.title()}"])
            for jtem in v:
                match(k):
                    case("appetisers"):
                        appItem = Appetiser(jtem['count'], *jtem['details'], jtem['note'])
                        text = appItem.outputPretty()
                        appetisers = tree.insert(order, END, values=[f"    {text['title']}", floatToPrice(text['price'])])
                        if(appItem.note):
                            tree.insert(appetisers, END, values=[f"            Note: {appItem.note}"])
                        if(text['sauce']):
                            tree.insert(appetisers, END, values=[f"            {text['sauce']}"])
                        totalPrice += float(text['price'])
                    case("baos"):
                        baoItem = Bao(jtem['count'], *jtem['details'], jtem['note'])
                        text = baoItem.outputPretty()
                        baos = tree.insert(order, END, values=[f"    {text['title']}", floatToPrice(text['price'])])
                        if(baoItem.note):
                            tree.insert(baos, END, values=[f"            Note: {baoItem.note}"])
                        tree.insert(baos, END, values=[f"            {text['sauce']}"])
                        for p in text['pickles']:
                            tree.insert(baos, END, values=[f"            {p}"])
                        totalPrice += float(text['price'])
                    case("bentos"):
                        bentoItem = Bento(jtem['count'], *jtem['details'], jtem['note'])
                        text = bentoItem.outputPretty()
                        bentos = tree.insert(order, END, values=[f"    {text['title']}", floatToPrice(text['price'])])
                        if(bentoItem.note):
                            tree.insert(bentos, END, values=[f"            Note: {bentoItem.note}"])
                        side1 = tree.insert(bentos, END, values=[f"            {text['side1']}"])
                        for m in text['side1Mod']:
                            tree.insert(side1, END, values=[f"                  {m}"])
                        side2 = tree.insert(bentos, END, values=[f"            {text['side2']}"])
                        for m in text['side2Mod']:
                            tree.insert(side2, END, values=[f"                  {m}"])
                        totalPrice += float(text['price'])
                    case("classics"):
                        classicItem = Classic(jtem['count'], *jtem['details'], jtem['note'])
                        text = classicItem.outputPretty()
                        classics = tree.insert(order, END, values=[f"    {text['title']}", floatToPrice(text['price'])])
                        if(classicItem.note):
                            tree.insert(classics, END, values=[f"            Note: {classicItem.note}"])
                        side = tree.insert(classics, END, values=[f"            {text['side']}"])
                        for m in text['sideMod']:
                            tree.insert(side, END, values=[f"                   {m}"])
                        totalPrice += float(text['price'])
                    case("sides"):
                        sideItem = Side(jtem['count'], *jtem['details'], jtem['note'])
                        text = sideItem.outputPretty()
                        sides = tree.insert(order, END, values=[f"    {text['title']}", floatToPrice(text['price'])])
                        if(sideItem.note):
                            tree.insert(sides, END, values=[f"            Note: {sideItem.note}"])
                        for m in text['sideMod']:
                            tree.insert(sides, END, values=[f"            {m}"])
                        totalPrice += float(text['price'])

        # Total price at the end
        tree.insert("", END, values=[""])
        tree.insert("", END, values=[f"Total: ", floatToPrice(totalPrice)])

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

# Employee management
def createOwnerManageEmployeesToplevel():
    OwnerManageEmployees = Toplevel(root, bg='#000000')
    createText([OwnerManageEmployees], 1, 0, 4, "Manage Employees", "Calibri 35 bold")

    def refresh():
        columns = ("cid", "fn", "ln", "ak")
        headings = ("Employee ID", "First Name", "Last Name", "Access Key")

        treeview = ttk.Treeview(OwnerManageEmployees, columns=columns, show='headings', padding=1, selectmode='browse')
        cursor.execute(f"SELECT * FROM employees")
        data = cursor.fetchall()
        for d in data:
            treeview.insert("", END, values=d)
        for c, h in zip(columns, headings):
            treeview.heading(c, text=h)
        treeview.grid(row = 3, column = 0, padx=10)
        treeview.bind('<<TreeviewSelect>>', lambda event: employeeSelected(event, treeview))



    def createOwnerCreateEmployeeToplevel():
        OwnerCreateEmployee = Toplevel(root, bg='#000000')
        OwnerCreateEmployee.geometry('1230x500')
        createText([OwnerCreateEmployee], 1, 0, 4, "Add Employee", "Calibri 35 bold")

        firstName = StringVar()
        lastName = StringVar()
        accessKey = StringVar()
        conAccessKey = StringVar()

        createText([OwnerCreateEmployee], 2, 0, 1, "First Name: ", pady=5, padx=38)
        createEntryBox([OwnerCreateEmployee], 2, 1, 1, firstName, width=21)
        createText([OwnerCreateEmployee], 3, 0, 1, "Last Name: ", pady=5, padx=38)
        createEntryBox([OwnerCreateEmployee], 3, 1, 1, lastName, width=21)
        createText([OwnerCreateEmployee], 4, 0, 1, "Access Key:", pady=5, padx=38)
        createEntryBox([OwnerCreateEmployee], 4, 1, 1, accessKey, width=21)
        createText([OwnerCreateEmployee], 5, 0, 1, "Confirm Key:", pady=5, padx=38)
        createEntryBox([OwnerCreateEmployee], 5, 1, 1, conAccessKey, width=21)

        def confirmAddEmployee():
            addEmployee(firstName.get(), lastName.get(), accessKey.get(), conAccessKey.get(), OwnerCreateEmployee)
            refresh()
        
        createButton([OwnerCreateEmployee], 6, 0, 2, "Create Profile", confirmAddEmployee)
    
    refresh()

    createButton([OwnerManageEmployees], 4, 0, 1, "Add Employee", createOwnerCreateEmployeeToplevel, pady=1)

    # Runs when an employee is selected in the treeview
    def employeeSelected(event, tree):
        selected_items = event.widget.selection()
        if selected_items:
            item = selected_items[0]
            record = event.widget.item(item)['values']
            if(record[0] != 1):
                createOwnerManageEmployeeToplevel(record)
            else:
                messagebox.showerror("Error", "Can't manage owner account", parent=OwnerManageEmployees)

    def createOwnerManageEmployeeToplevel(employee: list):
        OwnerManageEmployee = Toplevel(root, bg='#000000')
        createText([OwnerManageEmployee], 1, 0, 5, "Manage Employee", "Calibri 35 bold")
        createText([OwnerManageEmployee], 2, 0, 5, f"{employee[0]}, {employee[1]} {employee[2]}", "Calibri 20 bold")

        schedVars = [BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()]

        cursor.execute(f"SELECT schedule FROM employees WHERE employeeID = {employee[0]}")
        data = cursor.fetchone()[0]
        sched = bin(data).replace("0b", "").zfill(7)

        createText([OwnerManageEmployee], 3, 1, 1, "Usual schedule", "Calibri 18")
        createText([OwnerManageEmployee], 3, 2, 4, "Exceptions (Click any to delete)", "Calibri 18")
        # Checkboxes
        createCheckbox([OwnerManageEmployee], 4, 1, 1, "Mondays",    schedVars[0], initVal = sched[0])
        createCheckbox([OwnerManageEmployee], 5, 1, 1, "Tuesdays",   schedVars[1], initVal = sched[1])
        createCheckbox([OwnerManageEmployee], 6, 1, 1, "Wednesdays", schedVars[2], initVal = sched[2])
        createCheckbox([OwnerManageEmployee], 7, 1, 1, "Thursdays",  schedVars[3], initVal = sched[3])
        createCheckbox([OwnerManageEmployee], 8, 1, 1, "Fridays",    schedVars[4], initVal = sched[4])
        createCheckbox([OwnerManageEmployee], 9, 1, 1, "Saturdays",  schedVars[5], initVal = sched[5])
        createCheckbox([OwnerManageEmployee], 10, 1, 1, "Sundays",   schedVars[6], initVal = sched[6])

        # Exceptions treeview
        columns = ("d", "m", "y", "w")
        headings = ("Day", "Month", "Year", "Working?")
        widths = (100, 100, 100, 100)

        exceptionTreeview = ttk.Treeview(OwnerManageEmployee, columns=columns, show='headings', padding=1, selectmode='browse')
        exceptionTreeview.grid(row=4, column=2, columnspan=5, rowspan=6, padx=10, ipady=35)

        def exceptionSelected(event, tree):
            selected_items = event.widget.selection()
            if selected_items:
                item = selected_items[0]
                cursor.execute(f"SELECT exceptions FROM employees WHERE employeeID = {employee[0]}")
                exceptions = cursor.fetchone()[0]
                

                index = exceptionTreeview.index(item)
                exceptions = exceptions.split(',')
                exceptions.pop(index)
                exc = ""

                for e in exceptions:
                    exc += f"{e}, "
                exc = exc.removesuffix(", ")
                
                cursor.execute(f"UPDATE employees SET exceptions = \"{exc}\" WHERE employeeID = {employee[0]}")
                db.commit()

                exceptionTreeview.delete(item)
                populate()
            
        exceptionTreeview.bind('<<TreeviewSelect>>', lambda event: exceptionSelected(event, exceptionTreeview))

        def populate():
            # Delete all existing rows
            exceptionTreeview.delete(*exceptionTreeview.get_children())
            
            # Get orders
            cursor.execute(f"""SELECT exceptions FROM employees WHERE employeeID = {employee[0]}""")
            exceptions = cursor.fetchone()[0]

            if(not(exceptions)): return
            for i in exceptions.split(','):
                dmnw = str(i).split('/')
                d, m, n, w, y = genExceptions(int(dmnw[0]), int(dmnw[1]), int(dmnw[2]), int(dmnw[3]), 1)
                exceptionTreeview.insert("", END, values=[
                    d, m, y, w
                ])
            for c, h, w in zip(columns, headings, widths):
                exceptionTreeview.column(c, anchor='center', width=w)
                exceptionTreeview.heading(c, text=h, anchor='center')

        def saveSchedule():
            cursor.execute(f"UPDATE employees SET schedule = {int(f'0b{''.join([str(int(i.get())) for i in schedVars])}', 0)} WHERE employeeID = {employee[0]}")
            db.commit()
            messagebox.showinfo("Success", "Employee usual schedule updated", parent=OwnerManageEmployee)

        createButton([OwnerManageEmployee], 15, 1, 1, "Save Schedule", saveSchedule, "Calibri 18", ipadx=15)

        def confirmDeleteEmployee():
            deleteEmployee(employee[0], OwnerManageEmployee)
            refresh()

        createButton([OwnerManageEmployee], 20, 0, 5, "Delete Employee", confirmDeleteEmployee, "Calibri 18", ipadx=15)

        def addException():
            try:
                d = day.get()
                m = monthToInt(month.get())
                y = year.get()
                w = int(working.get())
            except TclError:
                messagebox.showerror("Error", "Invalid value entered", parent=OwnerManageEmployee)
                return

            monthLengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if(isLeapYear(y)): monthLengths[1] = 29

            if(y < 2024 or y > 2050):
                messagebox.showerror("Error", "Invalid year", parent=OwnerManageEmployee)
                return
            if(m < 1 or m > 12):
                messagebox.showerror("Error", "Invalid month", parent=OwnerManageEmployee)
                return
            if(d < 1 or d > monthLengths[m - 1]):
                messagebox.showerror("Error", "Invalid day", parent=OwnerManageEmployee)
                return
            
            cursor.execute(f"SELECT exceptions FROM employees WHERE employeeID = {employee[0]}")
            data = cursor.fetchone()[0]
            if(not(data)): data = ""
            exceptions = f"{d}/{m}/{y}/{w},{data}".removesuffix(',')
            cursor.execute(f"UPDATE employees SET exceptions = \"{exceptions}\" WHERE employeeID = {employee[0]}")
            db.commit()

            populate()

        day = IntVar()
        createText([OwnerManageEmployee], 9, 2, 1, "Day (num)", "Calibri 18")
        createEntryBox([OwnerManageEmployee], 10, 2, 1, day, "Calibri 18")

        month = StringVar()
        createText([OwnerManageEmployee], 9, 3, 1, "Month (\"Jan\", \"January\" or num)", "Calibri 18")
        createEntryBox([OwnerManageEmployee], 10, 3, 1, month, "Calibri 18")

        year = IntVar()
        createText([OwnerManageEmployee], 9, 4, 1, "Year (num)", "Calibri 18")
        createEntryBox([OwnerManageEmployee], 10, 4, 1, year, "Calibri 18")

        working = BooleanVar()
        createText([OwnerManageEmployee], 9, 5, 1, "Working?", "Calibri 18")
        createCheckbox([OwnerManageEmployee], 10, 5, 1, "", working, "Calibri 18")

        createButton([OwnerManageEmployee], 11, 3, 2, "Add Exception", addException, "Calibri 18")

        populate()
        

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
    
# Graph generation
def createOwnerReportsToplevel():
    # Import item details
    from orders import appetisers, baos, bentos, classics, sides

    # Create toplevel
    OwnerReports = Toplevel(root, bg='#000000')
    OwnerReports.protocol("WM_DELETE_WINDOW", lambda: closedWindow(OwnerReports))
    createText([OwnerReports], 1, 0, 4, "Reports", "Calibri 35 bold")

    # Dropdown data
    oList = ["All Time", "Current Month", "Current Year"]
    oListMonth = ["Whole Year"]

    # Store the auto-generated UI elements in a list so they can be easily access
    UIElements = [[], [], []]

    # Populate the rest of the period list with the years from 2024 to current year
    for y in range(2024, int(strftime("%Y")) + 1):
        oList.append(strftime("%Y", time.struct_time([y, 1, 1, 0, 0, 0, 0, 1, 0])))

    # Some variables
    selectedPeriod = StringVar()
    selectedMonth = StringVar()
    selectedItemCat = StringVar()

    # Period dropdown
    createDropdown([OwnerReports], 2, 0, 2, oList, selectedPeriod, "Calibri 20", "All Time")

    [e.destroy() for e in UIElements[1]]
    UIElements[1].clear()
    # Category selection dropdown
    oListItemCats = ["Appetisers", "Baos", "Bentos", "Classics", "Sides"]
    UIElements[1].append(createDropdown([OwnerReports], 5, 2, 1, oListItemCats, selectedItemCat, "Calibri 20", "Appetisers"))
    UIElements[1].append(createText([OwnerReports], 6, 2, 1, "Note: Generating an item trend graph for a specific\nmonth won't yield particularly useful results", "Calibri 15"))

    # Runs when the period of report changes
    def periodChanged(*args):
        [e.destroy() for e in UIElements[0]]
        UIElements[0].clear()
        # If it isn't a specific year, don't do anything
        if(selectedPeriod.get() in ["All Time", "Current Month", "Current Year"]):
            return
        oListMonth = ["Whole Year"]
        # How many months should it go to?
        # If the current year is greater than the selected year, set the month limit to 13
        if(int(strftime("%Y")) > int(selectedPeriod.get())): r = 13
        # Else set the month limit to the current month 
        # This becomes "January to last month" because range is x to y-1. This is intended behaviour
        else: r = int(strftime("%m"))
        # Month dropdown
        for m in range(1, r):
            oListMonth.append(strftime("%B", time.struct_time([y, m, 1, 0, 0, 0, 0, 1, 0])))
        UIElements[0].append(createDropdown([OwnerReports], 2, 2, 2, oListMonth, selectedMonth, "Calibri 20", "Whole Year"))

    # Runs when the item category changes
    cat = [{}]
    def itemCatChanged(*args):
        [e.destroy() for e in UIElements[2]]
        UIElements[2].clear()
        match(selectedItemCat.get()):
            case("Appetisers"):
                cat[0] = appetisers
            case("Baos"):
                cat[0] = baos
            case("Bentos"):
                cat[0] = bentos
            case("Classics"):
                cat[0] = classics
            case("Sides"):
                cat[0] = sides
    # Traces
    selectedPeriod.trace_add("write", periodChanged)
    selectedItemCat.trace_add("write", itemCatChanged)

    # Run each function for the first time
    periodChanged()
    itemCatChanged()
    
    # Generate a bar chart for sold items
    def generateSoldFoodItemsGraph():
        title, timeRange = graphTitle()

        title = f"{selectedItemCat.get()}\n{title}"
                   
        graphData = {}

        for i in list(cat[0].values()):
            graphData.update({i['name']: 0})

        # Defines between what two times data should be considered
        curTimeCheck = timeRange[0]
        while curTimeCheck < timeRange[1]:
            # Do some black magic with time and time structs
            curTime = time.localtime(curTimeCheck)
            timeNext = curTime
            timeNext = time.struct_time([timeNext.tm_year, timeNext.tm_mon + 1, *timeNext[2:9]])
            curTimeCheck = time.mktime(timeNext)

            # Get orders where their time is within the ranges
            cursor.execute(f"""SELECT orderData FROM orders WHERE placementTime > {time.mktime(curTime)} AND placementTime < {time.mktime(timeNext)}""")
            data = cursor.fetchall()

            # For each order, add the item count to the item count stored of the graph data
            for dat in data:
                d = json.loads(str(dat[0]).removeprefix('b\'').removesuffix('\''))[selectedItemCat.get().lower()]
                for i in d:
                    try:
                        graphData[cat[0][i['details'][0]]['name']] += i['count']
                    except IndexError:
                        graphData[cat[0][i['details'][0]]['name']].append(i['count'])
        # Plot it
        plotBarChart(title, "Item", "Qty Sold", graphData)

    # Generate a line chart of item counts for each month within thhe given period
    def generateItemTrendGraph():
        title, timeRange = graphTitle()
        
        title = f"{selectedItemCat.get()}\n{title}"
        
        graphData = {}
        xLabels = []

        #  Add each item to the list with a count of 0 for each
        for i in list(cat[0].values()):
            graphData.update({i['name']: []})

        curTimeCheck = timeRange[0]
        m = 0
        # Defines between what two times data should be considered
        while curTimeCheck < timeRange[1]:
            for i in list(cat[0].values()):
                graphData[i['name']].extend([0])
            curTime = time.localtime(curTimeCheck)
            # Generate the month labels
            xLabels.append(f'{strftime("%b, %Y", time.localtime(curTimeCheck + 1704067200))}')
            timeNext = curTime
            # I used day as 2 here instead of 1 because the time library doesn't like it sometimes with leapyears
            # It used to display "February" twice with no "December"
            timeNext = time.struct_time([timeNext.tm_year, timeNext.tm_mon + 1, 2, 0, 0, 0, *timeNext[6:9]])
            curTimeCheck = time.mktime(timeNext)

            # Get orders where their time is within the ranges
            cursor.execute(f"""SELECT orderData FROM orders WHERE placementTime > {time.mktime(curTime)} AND placementTime < {time.mktime(timeNext)}""")
            data = cursor.fetchall()
            
            # For each order, add the item count to the item count stored of the graph data for the given month
            for dat in data:
                d = json.loads(str(dat[0]).removeprefix('b\'').removesuffix('\''))[selectedItemCat.get().lower()]
                for i in d:
                    graphData[cat[0][i['details'][0]]['name']][m] += i['count']
            m = m + 1
        plotLineChart(title, "Month, Year", "Qty Sold", graphData, xLabels)

    # Data is in the form of {'Item name': count, 'Item name': count, ...}
    def plotBarChart(graphName: str, xName: str, yName: str, data: dict):
        import matplotlib.pyplot as mpl
        
        fig = mpl.figure(figsize=(14.0, 8.0))
        graph = fig.subplots()

        count = 0
        for k, v in data.items():
            if(v) != 0:
                graph.bar(truncateText(k, math.floor(25-(1.3 * len(data.items())))), v, 0.9).set_label(k)
                count += 1
        
        # Set labels
        graph.set_xlabel(xName)
        graph.set_ylabel(yName)
        graph.set_title(graphName)
        graph.set_xlim(0.6)
        graph.axis([-0.6, count, 0, max([i for i in data.values()]) + 1])

        try:
            graph.set_yticks([y for y in range(0, max([i for i in data.values()]) + 1)])
            # Show the legend
            graph.legend()
            
            # Show the plot in a separate window
            mpl.show()
        except ValueError:
            messagebox.showerror("Error", "No items in category for given time range", parent=OwnerReports)

    # Data is in the form of {'Item name': [month1 count, month2 count, month3 count...], 'Item name': [month1 count, month2 count, month3 count...], ...}
    # xLabels are a list of the months
    def plotLineChart(graphName: str, xName: str, yName: str, data: dict, xLabels: list[str]):
        import matplotlib.pyplot as mpl
        
        fig = mpl.figure(figsize=(14.0, 8.0))
        graph = fig.subplots()


        count = (len(list(data.values())))/-150
        for k, v in data.items():
            mpl.plot([i for i in range(0, len(v))], [adj + count for adj in v], label=k)
            count += 1/75
        
        graph.set_xlabel(xName)
        graph.set_ylabel(yName)
        graph.set_title(graphName)
        graph.set_xlim(0.6)
        graph.axis([0, count, 0, max([max([0, *i]) for i in data.values()]) + 1])

        try:
            graph.set_xticks([i for i in range(0, len(xLabels))], xLabels)
            graph.set_yticks([y for y in range(0, max([max([0, *i]) for i in data.values()]) + 1)])
            # Show the legend
            graph.legend()
            
            # Show the plot in a separate window
            mpl.show()
        except ValueError:
            messagebox.showerror("Error", "No items in category for given time range", parent=OwnerReports)
    
    def graphTitle():
        monYr = time.localtime()
        timeRange = [0, time.time() - 1704067200]
        match(selectedPeriod.get()):
            case("Current Month"):
                timeRange = [monthToTime(monYr.tm_mon, monYr.tm_year), monthToTime(monYr.tm_mon + 1, monYr.tm_year)]
                title = f"For the month of {strftime("%B")}\nAs of the {ordinal(int(strftime("%d")))}"
            case("Current Year"):
                timeRange = [monthToTime(1, monYr.tm_year), monthToTime(1, time.localtime().tm_year + 1)]
                title = f"For the year of {strftime("%Y")}\nAs of the {ordinal(int(strftime("%d")))} of {strftime("%B")}"
            case("All Time"):
                title = f"All current data"
            case(_):
                if(selectedMonth.get() == "Whole Year"):
                    timeRange = [monthToTime(1, selectedPeriod.get()), monthToTime(1, int(selectedPeriod.get()) + 1) - 86400]
                    if(int(selectedPeriod.get()) == int(strftime("%Y"))):
                        title = f"For the year of {strftime("%Y", time.localtime(timeRange[0] + 1704067200))}\nAs of the {ordinal(int(strftime("%d")))} of {strftime("%B")}"
                    else:
                        title = f"For the year of {strftime("%Y", time.localtime(timeRange[0] + 1704067200))}"
                else:
                    timeRange = [monthToTime(indexFromVal(months, selectedMonth.get()) + 1, selectedPeriod.get()), monthToTime(indexFromVal(months, selectedMonth.get()) + 2, selectedPeriod.get())]
                    title = f"For the month of {strftime("%B, %Y", time.localtime(timeRange[0] + 1704067200))}"
        return title, timeRange
        


    # createButton([OwnerReports], 4, 0, 2, "Sold Food Items - Quantities", lambda:generateSoldFoodItemsReport(), "Calibri 20", width=30)
    createButton([OwnerReports], 5, 0, 2, "Sold Food Items", lambda:generateSoldFoodItemsGraph(), "Calibri 20", width=30)
    createButton([OwnerReports], 6, 0, 2, "Item Trends", lambda:generateItemTrendGraph(), "Calibri 20", width=30)

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################