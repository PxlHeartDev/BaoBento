# Library imports
import time
import calendar

# Explicit imports
from datetime import date

# Num functions
def floatToPrice(f: float):
    return f"£{format(f, ',.2f')}"

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

# Date and time functions
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def monthToTime(month: int or str, year: int or str): # type: ignore
    if(type(month) == int): m = month
    else: m = indexFromVal(months, month) + 1
    if(type(year) == int): y = year
    else: y = int(year)
    return time.mktime(time.struct_time([y, m, 1, 1, 0, 0, 0, 1, 0])) - 1704067200

def genExceptions(day: int or str, month: int or str, year: int or str, working: int, monthMode = 0): # type: ignore
    if(type(day == int)): d = day
    else: d = int(day)
    if(type(month == int)): m = month
    else: m = int(month)
    if(type(year) == int): y = year
    else: y = int(year)
    
    return ordinal(d), months[m-1][0:3] if monthMode == 0 else months[m-1], calendar.day_name[date(y, m, d).weekday()][0:3], ["Not working", "Working"][working], y

def monthToInt(month: int or str):  # type: ignore
    try:
        month = int(month)
        return month
    except ValueError:
        if(len(month) == 3):
            return indexFromVal([m[0:3] for m in months], month.title())
        return indexFromVal(months, month.title())
    
def isLeapYear(year: int):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0: return True
            else: return False
        else: return True
    else: return True

# String functions
def truncateText(text: str, length: int):
    if(len(text) <= length + 1):
        return text
    if(text[length-1]) == ' ':
        return f'{text[0:length-1]}...'
    return f'{text[0:length]}...'


# List and dict functions
def keyFromVal(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val in str(value):
                return key
    except ValueError:
        return -1

# There was en edge-case where "Curry" would be found within "Micro Curry" and/or "Small Curry". This eliminates it
def keyFromValPrecise(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val == str(value):
                return key
    except ValueError:
        return -1

def indexFromVal(arr: list, val: any):
    try:
        for i in range(0, len(arr)):
            if val in str(arr[i]):
                return i
    except ValueError:
        return -1

# Misc
def closedWindow(frame):
    global selectedOrder
    selectedOrder = []
    global selectedEmployee
    selectedEmployee = []
    frame.destroy()