# Library imports
import time

# My imports
from main import db, cursor

modTypes = {
    1: {0: "No", 1: "Less", 2: "With", 3: "Extra"},                 # Pepper, onion, etc.
    2: {0: "No", 1: "Yes"},                                         # Basic
    3: {0: "Less hot", 1: "Normal", 2: "More hot"},                 # Spiciness of food
    4: {1: "Normal", 2: "More"},                                    # Spiciness of curry
    5: {0: "No", 1: "Less", 2: "With", 3: "Extra", 4: "Separate"}   # Mayo
}
sauceDict = {
    -1: "",
    0: "No sauce",
    1: "Sweet Chilli Sauce",
    2: "Micro Curry",
    3: "Small Curry",
    4: "Curry",
    5: "Soy Sauce",
    6: "Mayo",
    7: "Spicy Mayo",
    8: "Hoisin Mayo",
    9: "Vegan Mayo",
    10: "Korean Sauce",
    11: "Peking Sauce",
    12: "Sweet and Sour Sauce"
}

### Mods
hot =           {'name': 'Hot',             'modType': 3, 'default': 1}
hotCurry =      {'name': 'Hot',             'modType': 4, 'default': 1}
pepper =        {'name': 'Pepper',          'modType': 1, 'default': 2}
onion =        [{'name': 'Onion',           'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 2, 'default': 0}]
beanSprout =    {'name': 'Bean Sprouts',    'modType': 1, 'default': 2}
chicken =       {'name': 'Chicken',         'modType': 1, 'default': 2}
pork =          {'name': 'Pork',            'modType': 1, 'default': 2}
egg =           {'name': 'Egg',             'modType': 1, 'default': 2}
wellDone =      {'name': 'Well done',       'modType': 2, 'default': 0}
lemon =         {'name': 'Lemon',           'modType': 2, 'default': 1}
peas = [{'name': 'Peas', 'modType': 1, 'default': 0}, {'name': 'Peas', 'modType': 1, 'default': 2}]
pickles = [
    {'name': 'White Cabbage', 'modType': 2, 'default': 1}, 
    {'name': 'Cucumber', 'modType': 2, 'default': 1}, 
    {'name': 'Carrots', 'modType': 2, 'default': 1}, 
    {'name': 'Red Cabbage', 'modType': 2, 'default': 1}, 
    {'name': 'Lime', 'modType': 2, 'default': 0}, 
]



appetiserPermittedSauces = [0, 1, 2, 5]
appetisers = {
    1:  {'name': 'Spring Rolls',            'price': 4.00,  'mod': [],   'defaultSauce': 1},
    2:  {'name': 'Thai Spring Rolls',       'price': 4.00,  'mod': [],   'defaultSauce': 1},
    3:  {'name': 'Teriyaki Wings',          'price': 6.00,  'mod': [],   'defaultSauce': -1},
    4:  {'name': 'Korean Wings',            'price': 6.00,  'mod': [],   'defaultSauce': -1},
    5:  {'name': 'Thai Prawn Crackers',     'price': 3.50,  'mod': [],   'defaultSauce': -1},
    6:  {'name': 'Gyoza',                   'price': 7.00,  'mod': [wellDone],              'defaultSauce': 5},
    7:  {'name': 'Honey Ribs',              'price': 7.00,  'mod': [wellDone, lemon],       'defaultSauce': -1},
    8:  {'name': 'Peking Ribs',             'price': 7.00,  'mod': [wellDone],              'defaultSauce': -1},
    9:  {'name': 'Salted Chilli Chicken',   'price': 6.00,  'mod': [pepper, onion[0], hot],    'defaultSauce': -1},
    10: {'name': 'Spice Bowl',              'price': 6.50,  'mod': [pepper, onion[0], hot],    'defaultSauce': 3},
}

class Appetiser:
    def __init__(self, count: int, appetiser: int, mod: list[int], sauce: int, note: str):
        self.type = "appetisers"
        self.count = count
        self.appetiser = appetiser
        self.mod = mod
        self.sauce = sauce

        self.note = note

    def returnObject(self):
        return {"count": self.count, "details": [self.appetiser, self.mod, self.sauce], "price": appetisers[self.appetiser]['price'] * self.count, "note": self.note}

    def outputPretty(self):
        appetiser = appetisers[self.appetiser]
        final = {"title": "", "mod": [], "sauce": "", "price": appetiser['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{appetiser['name']}{'' if self.sauce == appetiser['defaultSauce'] and all([(d == m) for (d, m) in zip(appetiser['mod'], self.mod)]) else ' (Mod.)'}"
        final['sauce'] = f"{f'{sauceDict[self.sauce]}' if self.sauce else 'No sauce'}"
        return final



baoPermittedSauces = [0, 6, 7, 8, 9]
picklesDict = {
    1: "White Cabbage",
    2: "Red Cabbage",
    3: "Carrot",
    4: "Cucumber",
    5: "Red Onion"
}

baos = {
    1: {'name': 'Chicken',   'price': 7.50, 'pickles': [2, 0, 2, 2, 0], 'sauce': 7},
    2: {'name': 'Duck',      'price': 8.00, 'pickles': [2, 0, 2, 2, 2], 'sauce': 8},
    3: {'name': 'Rib',       'price': 7.50, 'pickles': [0, 2, 2, 2, 0], 'sauce': 8},
    4: {'name': 'Pork',      'price': 7.50, 'pickles': [0, 2, 2, 2, 2], 'sauce': 8},
    5: {'name': 'Veggie',    'price': 7.00, 'pickles': [2, 0, 2, 2, 2], 'sauce': 7},
    6: {'name': 'Vegan',     'price': 7.00, 'pickles': [2, 0, 2, 2, 2], 'sauce': 9},
}

class Bao:
    def __init__(self, count: int, meat: int, sauce: int, sauceMod: int, pickles: list[int], note: str):
        self.type = "baos"
        self.count = count
        self.meat = meat
        self.sauce = sauce
        self.sauceMod = sauceMod
        self.pickles = pickles

        self.note = note


    def returnObject(self):
        return {"count": self.count, "details": [self.meat, self.sauce, self.sauceMod, self.pickles], "price": baos[self.meat]['price'] * self.count, "note": self.note}

    def outputPretty(self):
        meat = baos[self.meat]['name']
        default = list(baos[self.meat].values())[2:4]
        final = {"title": "", "sauce": "", "pickles": ["", "", "", "", ""], "price": baos[self.meat]['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{meat} Bao {'' if self.sauce == default[0] and self.pickles == default[1] else ' (Mod.)'}"
        final['sauce'] = f"No sauce" if self.sauce == 0 else f"{modTypes[1][self.sauceMod]} {sauceDict[self.sauce]}"
        for p, i in zip(self.pickles, range(0, 5)):
            final['pickles'][i] = f"{modTypes[1][p]} {picklesDict[i+1]}"
        return final



bentoPermittedSauces = [0, 4, 10, 11, 12]
bentos = {
    1: {'name': 'Salt & Chilli Chicken',    'price': 9.30, 'mod': [pepper, onion[0], hot],                 'sauce': 4,  'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },
    2: {'name': 'Peking Chicken',           'price': 9.30, 'mod': [pepper, onion[0], hot],                 'sauce': -1, 'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },
    3: {'name': 'Sriracha Noodles',         'price': 9.30, 'mod': [pepper, onion[0], pork, chicken, hot],  'sauce': -1, 'sauceMod': 1, 'side1': [5, []], 'side2': [6, [1, 1, 1, 1, 1]], },
    4: {'name': 'Teriyaki Noodles',         'price': 9.30, 'mod': [pepper, onion[0], chicken],             'sauce': -1, 'sauceMod': 1, 'side1': [1, []], 'side2': [6, [1, 1, 1, 1, 0]], },
    5: {'name': 'Honey Beef',               'price': 9.30, 'mod': [pepper, onion[0], hot],                 'sauce': -1, 'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },      
    6: {'name': 'Katsu Chicken',            'price': 9.30, 'mod': [pickles[0]],                         'sauce': 4,  'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },
    7: {'name': 'Korean Fried Chicken',     'price': 9.30, 'mod': [pickles[0]],                         'sauce': 10, 'sauceMod': 1, 'side1': [5, []], 'side2': [2, []] },
    8: {'name': 'Squid',                    'price': 9.80, 'mod': [pepper, onion[0], hot],                 'sauce': 4,  'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], }
}
bentoSides = {
    1: {'name': 'Spring Rolls', 'mod': [], },
    2: {'name': 'Steamed Rice', 'mod': [], },
    3: {'name': 'Fried Rice',   'mod': [egg, peas[0]], },
    4: {'name': 'Noodles',      'mod': [chicken, onion[0], beanSprout], },
    5: {'name': 'Hot Wings',    'mod': [], },
    6: {'name': 'Pickles',      'mod': pickles[0:5], }
}

class Bento():
    def __init__(self, count: int, main: int, mainMod: [int], side1: int, side1Mod: [int], side2: int, side2Mod: [int], sauce: int, sauceMod: [int], note: str):
        self.type = "bentos"
        self.count = count
        self.main = main
        self.mainMod = mainMod
        self.side1 = side1
        self.side2 = side2
        self.side1Mod = side1Mod
        self.side2Mod = side2Mod
        self.sauce = sauce
        self.sauceMod = sauceMod

        self.note = note

    def returnObject(self):
        return {"count": self.count, "details": [self.main, self.mainMod, self.side1, self.side1Mod, self.side2, self.side2Mod, self.sauce, self.sauceMod], "price": bentos[self.main]['price'] * self.count, "note": self.note}

    def outputPretty(self):
        main = bentos[self.main]['name']
        side1 = bentoSides[self.side1]['name']
        side2 = bentoSides[self.side2]['name']
        default = bentos[self.main]
        final = {"title": "", "mainMod": [], "side1": "", "side1Mod": [], "side2": "", "side2Mod": [], "price": bentos[self.main]['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{main}{'' if all([self.mainMod == [d['default'] for d in default['mod']], self.sauce == default['sauce'], self.sauceMod == default['sauceMod'], [self.side1, self.side1Mod] == default['side1'], [self.side2, self.side2Mod] == default['side2']]) else ' (Mod.)'}"
        for i in range(0, len(bentos[self.main]['mod'])):
            final['mainMod'].append(f"{modTypes[bentos[self.main]['mod'][i]['modType']][self.mainMod[i]]} {bentos[self.main]['mod'][i]['name']}")
        
        final['side1'] = side1 if all([1 for m in bentoSides[self.side1]['mod']]) else f"{side1} (Mod.)"
        for i in range(0, len(self.side1Mod)):
            final['side1Mod'].append(f"{modTypes[bentoSides[self.side1]['mod'][i]['modType']][self.side1Mod[i]]} {bentoSides[self.side1]['mod'][i]['name']}")

        final['side2'] = side2 if all([1 for m in bentoSides[self.side2]['mod']]) else f"{side2} (Mod.)"
        for i in range(0, len(self.side2Mod)):
            final['side2Mod'].append(f"{modTypes[bentoSides[self.side2]['mod'][i]['modType']][self.side2Mod[i]]} {bentoSides[self.side2]['mod'][i]['name']}")
        return final



classics = {
    1: {'name': 'Sweet & Sour Chicken', 'price': 7.80, 'mod': [pepper, onion[0]],          'side': 1},
    2: {'name': 'Honey Chilli Chicken', 'price': 8.20, 'mod': [pepper, onion[0], hot],     'side': 1},
    3: {'name': 'Peking Chicken',       'price': 8.20, 'mod': [pepper, onion[0]],          'side': 1},
    4: {'name': 'Honey Chilli Beef',    'price': 8.20, 'mod': [pepper, onion[0], hot],     'side': 1},
    5: {'name': 'Peking Beef',          'price': 8.20, 'mod': [pepper, onion[0]],          'side': 1},
    6: {'name': 'Black Bean Chicken',   'price': 7.80, 'mod': [pepper, onion[0], hot],     'side': 1},
    7: {'name': 'Chicken Curry',        'price': 7.80, 'mod': [onion[0], peas[1], hot],    'side': 1},
    8: {'name': 'Veggie Curry',         'price': 7.80, 'mod': [pepper, onion[0], peas[1], beanSprout, hot], 'side': 1},
    9: {'name': 'Satay Chicken',        'price': 7.80, 'mod': [pepper, onion[0], hot],     'side': 1}
}

classicSides = {
    0: {'name': 'No side',      'mod': []},
    1: {'name': 'Steamed Rice', 'mod': []},
    2: {'name': 'Fried Rice',   'mod': [egg, peas[0]]},
    3: {'name': 'Noodles',      'mod': [chicken, onion[0], beanSprout]},
}

class Classic():
    def __init__(self, count: int, classic: int, classicMod: list[int], side: int, sideMod: list[int], note: str):
        self.type = "classics"
        self.count = count
        # SSCh | HCh | PeBe | BBCh | ChC | ChCHo | SatCh
        self.classic = classic
        self.classicMod = classicMod
        self.side = side
        self.sideMod = sideMod

        self.note = note

    def returnObject(self):
        return {"count": self.count, "details": [self.classic, self.classicMod, self.side, self.sideMod], "note": self.note}

    def outputPretty(self):
        classic = classics[self.classic]
        side = classicSides[self.side]
        final = {"title": "", "classicMod": [], "side": "", "sideMod": [], "price": classic['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{classic['name']}{'' if all([self.classicMod == [d['default'] for d in classic['mod']], self.side == classic['side'], self.side == classic['side'], self.sideMod == [m['default'] for m in side['mod']]]) else ' (Mod.)'}"
        for i in range(0, len(classic['mod'])):
            final['classicMod'].append(f"{modTypes[classics[self.classic]['mod'][i]['modType']][self.classicMod[i]]} {classics[self.classic]['mod'][i]['name']}")
        final['side'] = side['name'] if all([1 for m in classicSides[self.side]['mod']]) else f"{side['name']} (Mod.)"
        for i in range(0, len(side['mod'])):
            final['sideMod'].append(f"{modTypes[classicSides[self.side]['mod'][i]['modType']][self.sideMod[i]]} {classicSides[self.side]['mod'][i]['name']}")
        return final


sides = {
    1: {'name': 'Steamed Rice', 'price': 2.50, 'mod': []},
    2: {'name': 'Fried Rice',   'price': 3.00, 'mod': [egg, peas[0]]},
    3: {'name': 'Noodles',      'price': 3.50, 'mod': [chicken, onion[0], beanSprout]},
    4: {'name': 'Curry',        'price': 2.00, 'mod': [hotCurry, onion[1]]},
    5: {'name': 'Small Curry',  'price': 2.00, 'mod': [hotCurry, onion[1]]},
    6: {'name': 'Korean Sauce', 'price': 2.00, 'mod': []},
    7: {'name': 'Coke',         'price': 2.00, 'mod': []}
}
class Side():
    def __init__(self, count: int, side: int, sideMod: list[int], note: str):
        self.type = "sides"
        self.count = count
        self.side = side
        self.sideMod = sideMod

        self.note = note

    def returnObject(self):
        return {"count": self.count, "details": [self.side, self.sideMod], "note": self.note}
    
    def outputPretty(self):
        side = sides[self.side]
        final = {"title": "", "sideMod": [], "price": sides[self.side]['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{side['name']}{'' if self.returnObject()['details'][1] == [i['default'] for i in side['mod']] else ' (Mod.)'}"
        for i in range(0, len(side['mod'])):
            final['sideMod'].append(f"{modTypes[sides[self.side]['mod'][i]['modType']][self.sideMod[i]]} {sides[self.side]['mod'][i]['name']}")
        return final

class Order():
    def __init__(self):
        self.content = {"appetisers": [], "baos": [], "bentos": [], "classics": [], "sides": []}
        self.customerID = 1

    def assignCustomer(self, ID: int):
        self.customerID = ID

    def addItem(self, item: object):
        self.content[item.type].append(item.returnObject())

    def delItem(self, type: str, index: int):
        self.content[type].pop(index)

    def getOrderContent(self):
        return self.content

    def returnOrder(self):
        return f"{int(time.time() * 1000 - 1704067200000)}, {self.customerID}, '{str(self.content).replace("'", '"')}', 0, 0, {int(time.time() - 1704067200)}"

    def completeOrder(self, pickupTime: int, note: str):
        cursor.execute(f"""
            INSERT INTO orders (orderID, customerID_FK, orderData, complete, paid, placementTime, pickupTime, note)
            VALUES
            ({self.returnOrder()}, {pickupTime}, '{note}')
        """)
        db.commit()

def keyFromVal(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val in str(value):
                return key
    except ValueError:
        print("Value not in list")

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

o = Order()
o.assignCustomer(1)
# o.addItem(Bao(1, 1, 2, 1, [0, 2, 3, 2, 2], ""))
# o.addItem(Bao(1, 1, 2, 1, [1, 0, 1, 1, 0], ""))
# o.completeOrder(1704067200)
# o.addItem(Bento(1, 1, [1, 1, 3 ], 1, [     ], 3, [ 2, 0             ], 1, 0, ""))
# print(Classic(1, 1, [2, 0,], 2, [1, 1], "").outputPretty())
# print(Bento(1, 2, [2, 2, 2, 2, 1], 5, [], 6, [1, 1, 1, 1, 1], 0, 1, '').outputPretty())

# o.completeOrder(1704067200, "")