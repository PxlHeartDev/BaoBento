import time

def floatToPrice(f: float):
    return f"£{format(f, ',.2f')}"

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def monthToTime(month: int or str, year: int or str): # type: ignore
    if(type(month) == int):
        m = month
    else:
        m = indexFromVal(months, month) + 1
    if(type(year) == int):
        y = year
    else:
        y = int(year)
    return time.mktime(time.struct_time([y, m, 1, 1, 0, 0, 0, 1, 0])) - 1704067200
    
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def truncateText(text: str, length: int):
    if(len(text) <= length + 1):
        return text
    if(text[length-1]) == ' ':
        return f'{text[0:length-1]}...'
    return f'{text[0:length]}...'

def closedWindow(frame):
    global selectedOrder
    selectedOrder = []
    global selectedEmployee
    selectedEmployee = []
    frame.destroy()

def keyFromVal(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val in str(value):
                return key
    except ValueError:
        print("Value not in list")

# There was en edge-case where "Curry" would be found within "Micro Curry" and "Small Curry". This eliminates it
def keyFromValPrecise(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val == str(value):
                return key
    except ValueError:
        print("Value not in list")

def indexFromVal(arr: list, val: any):
    try:
        for i in range(0, len(arr)):
            if val in str(arr[i]):
                return i
    except ValueError:
        print("Value not in list")