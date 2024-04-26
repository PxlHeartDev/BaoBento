# Library imports
import time
import calendar

# Explicit imports
from datetime import date

# Num functions
def floatToPrice(f: float):
    return f"£{format(f, ',.2f')}"

# Using a day, generate a pretty form
# 1st, 2nd, 3rd, 4th, 5th, etc.
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

# Used in date and time functions
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Convert a month and a year to a time int
def monthToTime(month: int or str, year: int or str): # type: ignore
    if(type(month) == int): m = month
    else: m = indexFromVal(months, month) + 1
    if(type(year) == int): y = year
    else: y = int(year)
    return time.mktime(time.struct_time([y, m, 1, 1, 0, 0, 0, 1, 0])) - 1704067200

# Convert a day, month, year, boolean, and mode of month (abb. or full) to a prettified exception string
def genExceptions(day: int or str, month: int or str, year: int or str, working: int, monthMode = 0): # type: ignore
    if(type(day == int)): d = day
    else: d = int(day)
    if(type(month == int)): m = month
    else: m = int(month)
    if(type(year) == int): y = year
    else: y = int(year)
    
    return ordinal(d), months[m-1][0:3] if monthMode == 0 else months[m-1], calendar.day_name[date(y, m, d).weekday()][0:3], ["Not working", "Working"][working], y

# Convert a text month to an int of 1-12
def monthToInt(month: int or str):  # type: ignore
    try:
        month = int(month)
        return month
    except ValueError:
        if(len(month) == 3):
            return indexFromVal([m[0:3] for m in months], month.title()) + 1
        return indexFromVal(months, month.title()) + 1

# Boolean for if a year should be a leapyear
# Yes if divisible by 4, but not if divisible by 100, but not not if divisible by 400
def isLeapYear(year: int):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0: return True
            else: return False
        else: return True
    else: return True

# String functions

# Truncate a text to a certain length
def truncateText(text: str, length: int):
    if(len(text) <= length + 1):
        return text
    # Minor aesthetic thing. Doesn't let the last character be a space
    if(text[length-1]) == ' ':
        return f'{text[0:length-1]}...'
    return f'{text[0:length]}...'


# List and dict functions

# Get the key of a value from a dictionary where the dictionary's entry *contains* the val as a string, and is not perfectly equal to it
def keyFromVal(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val in str(value):
                return key
    except ValueError:
        return -1

# Get the index of a value in an array
def indexFromVal(arr: list, val: any):
    try:
        for i in range(0, len(arr)):
            if val in str(arr[i]):
                return i
    except ValueError:
        return -1

# Misc

# Runs when a window is closed
def closedWindow(frame):
    global selectedOrder
    selectedOrder = []
    global selectedEmployee
    selectedEmployee = []
    frame.destroy()