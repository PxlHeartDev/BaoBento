# Library imports
from tkinter import *
import time
import re
import json
import functools

# Explicit imports
from tkinter import messagebox, ttk
from time import strftime

# Me imports
from main import db, cursor, getCustomerData, refreshCustomerData
from gui import root, createText, createButton, createEntryBox, createDropdown, createCheckbox
from sql import retrieveCustomerOrders, deleteCustomer, updateDetails, updateEmail, updateNotif, updatePassword
from orders import keyFromVal, Appetiser, Bao, Bento, Classic, Side



global selectedOrder
selectedOrder = []

def createCustomerSettingsToplevel():
    # Notification prefences variables
    emailNotif = IntVar()
    SMSNotif = IntVar()

    # Get the data of the logged in customer
    data = getCustomerData()
    
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
    createButton([CustomerSettings], 10, 0, 4, "Delete Account", lambda:deleteCustomer(getCustomerData()[0], CustomerSettings), "Calibri 18", width=15)
    
    # Back
    createButton([CustomerSettings], 11, 0, 4, "Back", lambda:CustomerSettings.destroy(), "Calibri 18", pady=5, width=20)

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def createOwnerCreateOrderTopLevel():
    OwnerCreateOrder = Toplevel(root, bg='#000000')
    OwnerCreateOrder.geometry('960x690')
    createText([OwnerCreateOrder], 1, 0, 4, "Create Order", "Calibri 35 bold")
    createButton([OwnerCreateOrder], 2, 0, 4, "Appetisers", lambda:createOwnerAddItemTopLevel("appetisers"), "Calibri 30")
    createButton([OwnerCreateOrder], 3, 0, 4, "Baos", lambda:createOwnerAddItemTopLevel("baos"), "Calibri 30")

    createButton([OwnerCreateOrder], 4, 0, 4, "View order", lambda:[[print(j) for j in i] for i in o.content.values()])

    from orders import Order, modTypes, sauceDict

    o = Order()

    def createOwnerAddItemTopLevel(type: str):
        OwnerAddItem = Toplevel(root, bg='#000000')
        OwnerAddItem.geometry('960x690')
        match(type):
            case("appetisers"):

                from orders import appetisers, appetiserPermittedSauces

                UIElements = []
                vars = []

                def appetiserChanged(*args):
                    if('selected' in appetiserSelected.get()): return
                    appStuff = appetisers[keyFromVal(appetisers, appetiserSelected.get())]
                    oListMod = []
                    
                    [e.destroy() for e in UIElements]
                            
                    UIElements.clear()
                    vars.clear()

                    for i in range(0, len(appStuff['mod'])):
                        m = appStuff['mod'][i]
                        oListMod.clear()
                        vars.append(StringVar())
                        for v in modTypes[m['modType']].values():
                            oListMod.append(v)
                        UIElements.append(createText([OwnerAddItem], 5+i, 0, 1, f"{m['name']}: "))
                        UIElements.append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListMod, vars[i], "Calibri 15 bold", modTypes[m['modType']][m['default']], 24))

                    if(appStuff['defaultSauce'] != -1):
                        oListSauce = []
                        for i in appetiserPermittedSauces:
                            oListSauce.append(sauceDict[i])
                        if(appStuff['defaultSauce'] == 3):
                            oListSauce[2] = "Small Curry"
                        UIElements.append(createDropdown([OwnerAddItem], 5, 2, 1, oListSauce, sauceSelected, "Calibri 15 bold", sauceDict[appStuff['defaultSauce']], 24, 5))
                    
                    UIElements.append(createButton([OwnerAddItem], 9, 1, 4, "Add Item", addAppetiser, "Calibri 20", pady=5))

                def addAppetiser():
                    o.addItem(Appetiser(
                        count.get(),
                        keyFromVal(appetisers, appetiserSelected.get()),
                        [keyFromVal(modTypes[keyFromVal(modTypes, m.get())], m.get()) for m in vars],
                        keyFromVal(sauceDict, sauceSelected.get()),
                        note.get()))
                    messagebox.showinfo("Success", "Successfully Added appetiser to order", parent=OwnerAddItem)
                    OwnerAddItem.destroy()

                createText([OwnerAddItem], 1, 0, 4, "Appetisers", "Calibri 35 bold")
                oListApp = []
                for a in appetisers.values():
                    oListApp.append(a['name'])
                appetiserSelected = StringVar()
                sauceSelected = StringVar()
                appetiserSelected.trace("w", appetiserChanged)
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
                from orders import baos, baoPermittedSauces, picklesDict

                UIElements = []
                sauceAm = []
                vars = []

                def sauceChanged(*args):
                    [s.destroy() for s in sauceAm]
                    sauceAm.clear()
                    if('No' in sauceSelected.get()):
                        return
                    sauceAm.append(createDropdown([OwnerAddItem], 6, 2, 1, ["Less", "With", "Extra"], vars[0], "Calibri 15 bold", 'With', 15))

                def baoChanged(*args):
                    if('selected' in baoSelected.get()):
                        return
                    baoStuff = baos[keyFromVal(baos, baoSelected.get())]
                    
                    [e.destroy() for e in UIElements]
                        
                    UIElements.clear()
                    vars.clear()

                    vars.append(StringVar())
                    UIElements.append(createText([OwnerAddItem], 101, 0, 1, ""))
                        
                    oListPickles = []
                    for v in modTypes[1].values():
                        oListPickles.append(v)

                    for i in range(0, 5):
                        vars.append(StringVar())
                        UIElements.append(createText([OwnerAddItem], 5+i, 0, 1, f"{picklesDict[i+1]}: "))
                        UIElements.append(createDropdown([OwnerAddItem], 5+i, 1, 1, oListPickles, vars[i+1], "Calibri 15 bold", modTypes[1][baoStuff['pickles'][i]], 8))

                    oListSauce = []
                    for i in baoPermittedSauces:
                        oListSauce.append(sauceDict[i])
                    UIElements.append(createDropdown([OwnerAddItem], 5, 2, 1, oListSauce, sauceSelected, "Calibri 15 bold", sauceDict[baoStuff['sauce']], 15, 5))
                    
                    UIElements.append(createButton([OwnerAddItem], 12, 1, 4, "Add Item", addBao, "Calibri 20", pady=5))


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

                def makePlain():
                    for v in vars[1:]:
                        v.set("No")
                    sauceSelected.set("No sauce")

                createText([OwnerAddItem], 1, 0, 4, "Baos", "Calibri 35 bold")
                oListBao = []
                for b in baos.values():
                    oListBao.append(b['name'])
                baoSelected = StringVar()
                sauceSelected = StringVar()
                baoSelected.trace("w", baoChanged)
                sauceSelected.trace("w", sauceChanged)
                createText([OwnerAddItem], 2, 0, 1, "Bao: ")
                createDropdown([OwnerAddItem], 2, 1, 1, oListBao, baoSelected, "Calibri 15 bold", "No bao selected", 15)

                count = IntVar()
                createDropdown([OwnerAddItem], 2, 2, 1, [1, 2, 3, 4, 5], count, "Calibri 15 bold", 1, 5)

                createText([OwnerAddItem], 4, 0, 3, "Pickles: ", sticky='s', pady=10)
                createText([OwnerAddItem], 4, 2, 2, "Sauce: ", sticky='s', pady=10)

                createButton([OwnerAddItem], 8, 2, 1, "Plain", makePlain, "Calibri 15")

                note = StringVar()
                createText([OwnerAddItem], 11, 0, 1, "Notes: ", "Calibri 20", pady=10)
                createEntryBox([OwnerAddItem], 11, 1, 2, note, "Calibri 20", width=30, ipadx=30)

            case("bentos"):
                pass
            case("classics"):
                pass
            case("sides"):
                pass

    

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


#


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def createOwnerViewOrdersToplevel():
    OwnerViewOrders = Toplevel(root, bg='#000000')
    OwnerViewOrders.protocol("WM_DELETE_WINDOW", lambda: closedWindow(OwnerViewOrders))
    OwnerViewOrders.geometry('1500x500')
    createText([OwnerViewOrders], 1, 0, 4, "View Orders", "Calibri 35 bold")

    columns = ("oid", "cid", "data", "com", "paid", "ptime", "pktime")
    headings = ("Order ID", "Customer ID", "Order Data", "Completed?", "Paid?", "Placement Time", "Pickup Time")
    widths = (100, 100, 100, 80, 80, 180, 180)

    treeview = ttk.Treeview(OwnerViewOrders, columns=columns, show='headings', padding=1, selectmode='browse')
    treeview.grid(row = 3, column = 0, columnspan=5, padx=10)

    orderTreeview = ttk.Treeview(OwnerViewOrders, padding=3, columns=["title", "price"], show='headings')
    orderTreeview.grid(row=3, column=5, padx=10, columnspan=2)
    orderTreeview.column("title", anchor='w', width=400)
    orderTreeview.column("price", anchor='w', width=100)
    orderTreeview.heading("title", text='No order selected', anchor='center')

    def populate(filter=""):
        treeview.delete(*treeview.get_children())
        
        cursor.execute(f"""SELECT * FROM orders {filter}""")
        data = cursor.fetchall()

        for d in data:
            
            itemCount = sum([sum([i['count'] for i in v]) for v in json.loads(d[2]).values()])
            treeview.insert("", END, values=[
                d[0], 
                d[1], 
                f"{itemCount} item{'s' if itemCount > 1 else ''}", 
                "Yes" if d[3] else "No", "Yes" if d[4] else "No", 
                strftime("%a, %d %b %Y %H:%M:%S", time.localtime(d[5] + 1672531200)), 
                strftime("%a, %d %b %Y %H:%M:%S", time.localtime(d[6] + 1672531200))
            ])
            treeview.bind('<<TreeviewSelect>>', lambda event: orderSelected(event, orderTreeview))
        for c, h, w in zip(columns, headings, widths):
            treeview.column(c, anchor='center', width=w)
            treeview.heading(c, text=h, anchor='center')

    def markComplete():
        global selectedOrder
        if(not(selectedOrder)):
            messagebox.showerror("Error", "No order selected", parent=treeview)
            return
        cursor.execute(f"UPDATE orders SET complete = {0 if selectedOrder[3] == 'Yes' else 1} WHERE orderID = {selectedOrder[0]};")
        db.commit()
        
    def markPaid():
        global selectedOrder
        if(not(selectedOrder)):
            messagebox.showerror("Error", "No order selected", parent=treeview)
            return
        cursor.execute(f"UPDATE orders SET paid = {0 if selectedOrder[4] == 'Yes' else 1} WHERE orderID = {selectedOrder[0]};")
        db.commit()

    buttonFont = 'Calibri 18'
    createText([OwnerViewOrders], 4, 0, 1, "Filter:", pady=8)
    createButton([OwnerViewOrders], 4, 1, 1, "All", command=lambda: populate(""), font=buttonFont)
    createButton([OwnerViewOrders], 4, 2, 1, "Active", command=lambda: populate("WHERE complete = 0"), font=buttonFont)
    createButton([OwnerViewOrders], 4, 3, 1, "Complete", command=lambda: populate("WHERE complete = 1"), font=buttonFont)
    createButton([OwnerViewOrders], 4, 4, 1, "Outstanding", command=lambda: populate("WHERE complete = 1 AND paid = 0"), font=buttonFont)

    createButton([OwnerViewOrders], 4, 5, 1, "Mark Complete", command=markComplete, font=buttonFont)
    createButton([OwnerViewOrders], 4, 6, 1, "Mark Paid", command=markPaid, font=buttonFont)
    createText([OwnerViewOrders], 5, 5, 2, "Make sure to check that you have the right\norder and to refresh after marking orders!", font="Calibri 10")
    
    populate()

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def createOwnerManageCustomersToplevel():
    OwnerManageCustomers = Toplevel(root, bg='#000000')
    OwnerManageCustomers.geometry('1230x500')
    createText([OwnerManageCustomers], 1, 0, 4, "Manage Customers", "Calibri 35 bold")

    columns = ("cid", "fn", "ln", "pn", "em", "pw")
    headings = ("Customer ID", "First Name", "Last Name", "Phone Number", "Email", "Password")

    treeview = ttk.Treeview(OwnerManageCustomers, columns=columns, show='headings', padding=1, selectmode='browse')
    cursor.execute(f"SELECT * FROM customers")
    data = cursor.fetchall()
    for d in data:
        treeview.insert("", END, values=d)
    for c, h in zip(columns, headings):
        treeview.heading(c, text=h)
    treeview.grid(row = 3, column = 0, padx=10)
    treeview.bind('<<TreeviewSelect>>', lambda event: customerSelected(event, treeview))

def customerSelected(event, tree):
    selected_items = event.widget.selection()
    if selected_items:
        item = selected_items[0]
        record = event.widget.item(item)['values']
        createOwnerModerationToplevel(record)

#############################################################################################################################

def createOwnerModerationToplevel(customer: list):
    OwnerManageIndividual = Toplevel(root, bg='#000000')
    createText([OwnerManageIndividual], 1, 0, 4, "Manage Customer", "Calibri 35 bold")
    createText([OwnerManageIndividual], 2, 0, 4, f"{customer[0]}, {customer[1]} {customer[2]}", "Calibri 20 bold")
    createButton([OwnerManageIndividual], 3, 0, 4, "View Order History", lambda:createOwnerViewCustomerOrdersToplevel(customer), "Calibri 18", ipadx=15)

#############################################################################################################################

def createOwnerViewCustomerOrdersToplevel(customer):
    OwnerViewCustomerOrders= Toplevel(root, bg='#000000')
    OwnerViewCustomerOrders.protocol("WM_DELETE_WINDOW", lambda: closedWindow(OwnerViewCustomerOrders))
    OwnerViewCustomerOrders.geometry("1500x500")
    createText([OwnerViewCustomerOrders], 1, 0, 4, "Order History", "Calibri 35 bold")
    createText([OwnerViewCustomerOrders], 2, 0, 4, f"{customer[0]}, {customer[1]} {customer[2]}", "Calibri 20 bold")

    data = retrieveCustomerOrders(customer[0])

    columns = ("oid", "data", "com", "paid", "ptime", "pktime")
    headings = ("Order ID", "Order Data", "Completed?", "Paid?", "Placement Time", "Pickup Time")
    widths = (100, 100, 80, 80, 180, 180)
    treeview = ttk.Treeview(OwnerViewCustomerOrders, columns=columns, show='headings', padding=1, selectmode='browse')

    orderTreeview = ttk.Treeview(OwnerViewCustomerOrders, padding=3, columns=["title", "price"], show='headings')
    orderTreeview.grid(row=3, column=1, padx=10, columnspan=2)
    orderTreeview.column("title", anchor='w', width=400)
    orderTreeview.column("price", anchor='w', width=100)
    orderTreeview.heading("title", text='No order selected', anchor='center')

    for d in data:
        itemCount = sum([sum([i['count'] for i in v]) for v in json.loads(d[2]).values()])
        treeview.insert("", END, values=[d[0], f"{itemCount} item{'s' if itemCount > 1 else ''}", "Yes" if d[3] else "No", "Yes" if d[4] else "No",  strftime("%a, %d %b %Y %H:%M:%S", time.localtime(d[5] + 1672531200)), strftime("%a, %d %b %Y %H:%M:%S", time.localtime(d[6] + 1672531200))])
        treeview.bind('<<TreeviewSelect>>', lambda event: orderSelected(event, orderTreeview))
    for c, h, w in zip(columns, headings, widths):
        treeview.column(c, anchor='center', width=w)
        treeview.heading(c, text=h, anchor='center')
    treeview.grid(row = 3, column = 0, padx=10)

#############################################################################################################################

def orderSelected(event, tree):
    selectedItems = event.widget.selection()
    if selectedItems:
        item = selectedItems[0]
        record = event.widget.item(item)['values']
        global selectedOrder
        selectedOrder = record
        cursor.execute(f"""SELECT *  FROM orders WHERE orderID = {record[0]}""")
        orderData = cursor.fetchone()[2]

        tree.heading("title", text=f'Order {record[0]}', anchor='center')
        tree.heading("price", text='Price:', anchor='center')

        tree.delete(*tree.get_children())

        totalPrice = 0.00

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
                        side = tree.insert(bentos, END, values=[f"            {text['side']}"])
                        tree.insert(side, END, values=[f"                   {text['sideMod']}"])
                        totalPrice += float(text['price'])
                    case("sides"):
                        pass
                        totalPrice += float(text['price'])

        tree.insert("", END, values=[""])
        tree.insert("", END, values=[f"Total: ", floatToPrice(totalPrice)])

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def floatToPrice(f: float):
    return f"£{format(f, ',.2f')}"

def closedWindow(frame):
    global selectedOrder
    selectedOrder = []
    frame.destroy()

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################