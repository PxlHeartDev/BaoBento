# Library imports
import time

# My imports
from main import db, cursor

modTypes = {
    1: {0: "No", 1: "Less", 2: "With", 3: "Extra"},                 # Pepper, onion, etc.
    2: {0: "No", 1: "Yes"},                                         # Well done
    3: {0: "Less hot", 1: "Normal", 2: "More hot"},                 # Spiciness of food
    4: {0: "Normal", 1: "Hot", 2: "+ Onions", 3: "Hot + Onions"},   # Curry
    5: {0: "No", 1: ""}                                             # Basic thingy
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
    11: "Peking Sauce"
}
# for a, p, m in zip(appDict.items(), prices.items(), appModDict.items()):
#     print(f"""{a[0]}: \
# {{'name': '{a[1]}', \
# 'price': {p[1]}0, \
# 'mod': {[{'name': f'{o}', 'modType': 1, 'default': 2,} for o in [n[1] for n in m[1].items()]]}, \
# 'defaultSauce': -1}},\
# """)

appetiserPermittedSauces = [0, 1, 2, 5]
appetisers = {
    1:  {'name': 'Spring Rolls',            'price': 4.00,  'mod': [],   'defaultSauce': 1},
    2:  {'name': 'Thai Spring Rolls',       'price': 4.00,  'mod': [],   'defaultSauce': 1},
    3:  {'name': 'Teriyaki Wings',          'price': 6.00,  'mod': [],   'defaultSauce': -1},
    4:  {'name': 'Korean Wings',            'price': 6.00,  'mod': [],   'defaultSauce': -1},
    5:  {'name': 'Thai Prawn Crackers',     'price': 3.50,  'mod': [],   'defaultSauce': -1},
    6:  {'name': 'Peking Beef',             'price': 6.00,  'mod': [],   'defaultSauce': -1},
    7:  {'name': 'Gyoza',                   'price': 7.00,  'mod': [{'name': 'Well done', 'modType': 2, 'default': 0}],    'defaultSauce': 3},
    8:  {'name': 'Honey Ribs',              'price': 7.00,  'mod': [{'name': 'Well done', 'modType': 2, 'default': 0}],    'defaultSauce': -1},
    9:  {'name': 'Peking Ribs',             'price': 7.00,  'mod': [{'name': 'Well done', 'modType': 2, 'default': 0}],    'defaultSauce': -1},
    10: {'name': 'Salted Chilli Chicken',   'price': 6.00,  'mod': [{'name': 'Pepper', 'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 1, 'default': 2}, {'name': 'Hot', 'modType': 3, 'default': 1}],  'defaultSauce': -1},
    11: {'name': 'Spice Bowl',              'price': 6.50,  'mod': [{'name': 'Pepper', 'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 1, 'default': 2}, {'name': 'Hot', 'modType': 3, 'default': 1}],  'defaultSauce': 3},
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

baoPermittedSauces = [0, 6, 7, 8, 9]
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
        meat = self.meatDict[self.meat]
        default = self.defaults[self.meat]
        final = {"title": "", "sauce": "", "pickles": ["", "", "", "", ""], "price": baos[self.meat]['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{meat} Bao {'' if self.returnObject()['details'] == default else ' (Mod.)'}"
        final['sauce'] = f"No sauce" if self.sauce == 0 else f"{modTypes[1][self.sauceMod]}{sauceDict[self.sauce]}"
        for p, i in zip(self.pickles, range(0, 5)):
            final['pickles'][i] = f"{modTypes[1][p]}{self.picklesDict[i+1]}"
        return final


mainDict = {
    1: "Salt & Chilli Chicken",
    2: "Sriracha Noodles",
    3: "Teriyaki Noodles",
    4: "Honey Beef",
    5: "Katsu Chicken",
    6: "Korean Fried Chicken",
    7: "Squid"
}
prices = {
    1: 9.30,
    2: 9.30,
    3: 9.30,
    4: 9.30,
    5: 9.30,
    6: 9.30,
    7: 9.80
}
mainModDict = {
    1: {1: "Pepper", 2: "Onion", 3: "Hot"},
    2: {1: "Pepper", 2: "Onion", 3: "Pork", 4: "Chicken", 5: "Hot"},
    3: {1: "Chicken"},
    4: {1: "Hot"},
    5: {1: "White Cabbage"},
    6: {1: "White Cabbage"},
    7: {1: "Pepper", 2: "Onion", 3: "Hot"}
}
sideDict = {
    1: "Spring Rolls",
    2: "Steamed Rice",
    3: "Fried Rice",
    4: "Noodles",
    5: "Hot Wings",
    6: "Pickles"
}

sideModDict = {
    1: {},
    2: {},
    3: {1: "Egg", 2: "Peas"},
    4: {1: "Chicken", 2: "Veg"},
    5: {},
    6: {1: "White Cabbage", 2: "Cucumber", 3: "Carrots", 4: "Red Cabbage", 5: "Lime"}
}
defaults = {
    1: [1, [1, 1, 1     ], 1, [     ], 2, [              ], 1],
    2: [2, [1, 1, 1, 1  ], 5, [     ], 6, [1, 1, 1, 1, 1 ], 0],
    3: [3, [1, 1        ], 1, [     ], 6, [1, 1, 1, 1, 0 ], 0],
    4: [4, [1           ], 1, [     ], 2, [              ], 0],
    5: [5, [1           ], 1, [     ], 2, [              ], 1],
    6: [6, [1           ], 5, [     ], 2, [              ], 3],
    7: [7, [1, 1, 1     ], 1, [     ], 2, [              ], 1]
}
bentos = {
    1: {'name': 'Salt & Chilli Chicken',    'price': 9.30, 'mod': [{'name': 'Pepper', 'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 1, 'default': 2}, {'name': 'Hot', 'modType': 3, 'default': 2}],     'sauce': 1, 'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },
    2: {'name': 'Sriracha Noodles',         'price': 9.30, 'mod': [{'name': 'Pepper', 'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 1, 'default': 2}, {'name': 'Pork', 'modType': 1, 'default': 2}, {'name': 'Chicken', 'modType': 1, 'default': 2}, {'name': 'Hot', 'modType': 3, 'default': 2}], 'sauce': 0, 'sauceMod': 1, 'side1': [5, []], 'side2': [6, [1, 1, 1, 1, 1]], },
    3: {'name': 'Teriyaki Noodles',         'price': 9.30, 'mod': [{'name': 'Chicken', 'modType': 1, 'default': 2}],            'sauce': 0, 'sauceMod': 1, 'side1': [1, []], 'side2': [6, [1, 1, 1, 1, 0]], },
    4: {'name': 'Honey Beef',               'price': 9.30, 'mod': [{'name': 'Hot', 'modType': 3, 'default': 2}],                'sauce': 0, 'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },      
    5: {'name': 'Katsu Chicken',            'price': 9.30, 'mod': [{'name': 'White Cabbage', 'modType': 1, 'default': 2}],      'sauce': 1, 'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], },
    6: {'name': 'Korean Fried Chicken',     'price': 9.30, 'mod': [{'name': 'White Cabbage', 'modType': 1, 'default': 2}],      'sauce': 3, 'sauceMod': 1, 'side1': [5, []], 'side2': [2, []] },
    7: {'name': 'Squid',                    'price': 9.80, 'mod': [{'name': 'Pepper', 'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 1, 'default': 2}, {'name': 'Hot', 'modType': 3, 'default': 2}],     'sauce': 1, 'sauceMod': 1, 'side1': [1, []], 'side2': [2, []], }
}
bentoSides = {
    1: {'name': 'Spring Rolls', 'mod': [], },
    2: {'name': 'Steamed Rice', 'mod': [], },
    3: {'name': 'Fried Rice',   'mod': [{'name': 'Egg', 'modType': 1}, {'name': 'Peas', 'modType': 1}], },
    4: {'name': 'Noodles',      'mod': [{'name': 'Chicken', 'modType': 1}, {'name': 'Veg', 'modType': 1}], },
    5: {'name': 'Hot Wings',    'mod': [], },
    6: {'name': 'Pickles',      'mod': [{'name': 'White Cabbage', 'modType': 5}, {'name': 'Cucumber', 'modType': 5}, {'name': 'Carrots', 'modType': 5}, {'name': 'Red Cabbage', 'modType': 5}, {'name': 'Lime', 'modType': 5}], }
}
# for a, p, m, d in zip(mainDict.items(), prices.items(), mainModDict.values(), defaults.values()):
#     print(f"""{a[0]}: \
# {{'name': '{a[1]}', \
# 'price': {p[1]}0, \
# 'mod': {[f"{{'name': '{n}', 'modType': 1, 'default': 2}}" for n in m.values()]}, \
# 'sauce': {d[6]}, \
# 'sauceMod': 1, \
# 'side1': {{}}, \
# 'side2': {{}}, \
# }},\
# """.replace('"', ''))
# print("-----")
# for a, m, d in zip(sideDict.items(), sideModDict.values(), defaults.values()):
#     print(f"""{a[0]}: \
# {{'name': '{a[1]}', \
# 'mod': {[f"{{'name': '{n}', 'modType': 1, 'default': 1}}" for n in m.values()]}, \
# }},\
# """.replace('"', ''))
class Bento():
    def __init__(self, count: int, main: int, mainMod: [int], side1: int, side1Mod: [int], side2: int, side2Mod: [int], sauce: int, note: str):
        self.type = "bentos"
        self.count = count
        # SC | SN | TN | HB | KC | KFC | Sq
        self.main = main
        # Xpep + Xoni + >hot + <hot
        self.mainMod = mainMod
        # SpRo | StRi | FRi | No | HW
        self.side1 = side1
        self.side2 = side2
        # Contextual: Examples would be Eggs/Peas for Fried Rice or Veg in the Noodles
        self.side1Mod = side1Mod
        self.side2Mod = side2Mod
        # Cu | CuHo | Ko | SCh | Soy | M | SM | HM | VM | Pk
        self.sauce = sauce

        self.note = note

        self.price = self.prices[self.main]


    def returnObject(self):
        return {"count": self.count, "details": [self.main, self.mainMod, self.side1, self.side1Mod, self.side2, self.side2Mod, self.sauce], "price": self.price * self.count, "note": self.note}

    def outputPretty(self):
        main = self.bentos[self.main]
        mainMod = self.mainModDict[self.main]
        side1 = self.sideDict[self.side1]
        side1Mod = self.sideModDict[self.side1]
        side2 = self.sideDict[self.side2]
        side2Mod = self.sideModDict[self.side2]
        default = self.defaults[self.main]
        final = {"title": "", "mainMod": [], "side1": "", "side1Mod": [], "side2": "", "side2Mod": [], "price": self.price * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{main}{'' if self.returnObject()['details'] == default else ' (Mod.)'}"
        for i, v in mainMod.items():
            if(v == 'Hot'):
                final['mainMod'].append(f"{self.amountDict[self.mainMod[i-1]] if self.mainMod[i-1] >= 2 else ''}{'Hot' if self.mainMod[i-1] >= 2 else ''}")
            else:
                final['mainMod'].append(f"{self.amountDict[self.mainMod[i-1]]}{mainMod[i]}")
        final['side1'] = side1 if default[3] == self.side1Mod else f"{side1} (Mod.)"
        for i in range(0, len(side1Mod)):
            final['side1Mod'].append(f"{self.amountDict[self.side1Mod[i]]}{side1Mod[i+1]}")
        final['side2'] = side2 if default[5] == self.side2Mod else f"{side2} (Mod.)"
        for i in range(0, len(side2Mod)):
            final['side2Mod'].append(f"{self.amountDict[self.side2Mod[i]]}{side2Mod[i+1]}")
        return final

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

        self.prices = {
            1: 7.80,
            2: 8.20,
            3: 8.20,
            4: 7.80,
            5: 7.80,
            6: 7.80
        }

        self.price = self.prices[self.classic]

        self.classicDict = {
            1: "Sweet & Sour Chicken",
            2: "Honey Chilli Chicken",
            3: "Peking Beef",
            4: "Black Bean Chicken",
            5: "Chicken Curry",
            6: "Satay Chicken"
        }

        self.classicModDict = {
            1: {1: "Pepper", 2: "Onion"},
            2: {1: "Pepper", 2: "Onion"},
            3: {},
            4: {},
            5: {1: "Onion", 2: "Peas", 3: "Hot"},
            6: {1: "Hot"}
        }

        self.sideDict = {
            0: "No side",
            1: "Steamed Rice",
            2: "Fried Rice",
            3: "Noodles",
        }

        self.sideModDict = {
            0: {},
            1: {},
            2: {1: "Egg", 2: "Peas"},
            3: {}
        }

        self.amountDict = {
            0: "No ",
            1: "",
            2: "Extra ",
            3: "Less "
        }

        self.defaults = {
            1: [1, [1, 1    ], 1, [ ]],
            2: [2, [1, 1    ], 1, [ ]],
            3: [3, [        ], 1, [ ]],
            4: [4, [        ], 1, [ ]],
            5: [5, [1, 1, 1 ], 1, [ ]],
            6: [6, [1       ], 1, [ ]]
        }

        self.sideModDefaults = {
            0: [],
            1: [],
            2: [1, 1],
            3: []
        }

    def returnObject(self):
        return {"count": self.count, "details": [self.classic, self.classicMod, self.side, self.sideMod], "note": self.note}
    
    def outputPretty(self):
        classic = self.classicDict[self.classic]
        classicMod = self.classicModDict[self.classic]
        side = self.sideDict[self.side]
        sideMod = self.sideModDict[self.side]
        default = self.defaults[self.classic]
        final = {"title": "", "classicMod": [], "side": "", "sideMod": [], "price": self.price * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{classic}{'' if self.returnObject()['details'] == default else ' (Mod.)'}"
        for i, v in classicMod.items():
            if(v == 'Hot'):
                final['classicMod'].append(f"{self.amountDict[self.classicMod[i-1]] if self.classicMod[i-1] >= 2 else ''}{'Hot' if self.classicMod[i-1] >= 2 else ''}")
            else:
                final['classicMod'].append(f"{self.amountDict[self.classicMod[i-1]]}{classicMod[i]}")
        final['side'] = side if self.sideModDefaults[self.side] == self.sideMod else f"{side} (Mod.)"
        for i in range(0, len(sideMod)):
            final['sideMod'].append(f"{self.amountDict[self.sideMod[i]]}{sideMod[i+1]}")
        return final

class Side():
    def __init__(self, count: int, side: int, sideMod: list[int], note: str):
        self.type = "sides"
        self.count = count
        # StRi | FRi | FRPe | FREg | FREgPe | No
        self.side = side
        self.sideMod = sideMod

        self.note = note

        self.prices = {
            1: 2.50,
            2: 3.00,
            3: 3.50,
            4: 2.00,
            5: 2.00,
            6: 2.00
        }
        
        self.sideDict = {
            1: "Steamed Rice",
            2: "Fried Rice",
            3: "Noodles",
            4: "Curry",
            5: "Korean Sauce",
            6: "Coke"
        }

        self.amountDict = {
            0: "No ",
            1: "",
            2: "Extra ",
            3: "Less "
        }
        
        self.sideModDict = {
            1: {},
            2: {1: "Egg", 2: "Peas"},
            3: {},
            4: {1: "Hot", 2: "Small", 3: "+Onion"},
            5: {},
            6: {}
        }

        self.defaults = {
            1: [],
            2: [1, 1],
            3: [],
            4: [1, 1, 0],
            5: [],
            6: []
        }

    def returnObject(self):
        return {"count": self.count, "details": [self.side, self.sideMod], "note": self.note}
    
    def outputPretty(self):
        side = self.sideDict[self.side]
        sideMod = self.sideModDict[self.side]
        default = self.defaults[self.side]
        final = {"title": "", "sideMod": [], "price": self.price * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{side}{'' if self.returnObject()['details'] == default else ' (Mod.)'}"
        for i, v in sideMod.items():
            if(v == 'Hot'):
                final['sideMod'].append(f"{self.amountDict[self.sideMod[i-1]] if self.sideMod[i-1] >= 2 else ''}{'Hot' if self.classicMod[i-1] >= 2 else ''}")
            else:
                final['sideMod'].append(f"{self.amountDict[self.sideMod[i-1]]}{sideMod[i]}")

class Order():
    def __init__(self):
        self.content = {"appetisers": [], "baos": [], "bentos": [], "classics": [], "sides": []}
        self.customerID = 0

    def assignCustomer(self, ID: int):
        self.customerID = ID

    def addItem(self, item: object):
        self.content[item.type].append(item.returnObject())

    def delItem(self, item: object, index: int):
        self.content[item.type].pop(index)

    def returnOrder(self):
        return self.content

    def completeOrder(self, pickupTime: int, note: str):
        cursor.execute(f"""
            INSERT INTO orders (orderID, customerID_FK, orderData, complete, paid, placementTime, pickupTime, note)
            VALUES
            ({int(time.time() * 1000 - 1672531200000)}, {self.customerID}, '{str(self.content).replace("'", '"')}', 0, 0, {int(time.time() - 1672531200)}, {pickupTime}, '{note}')
        """)
        db.commit()

def keyFromVal(dict: dict, val: any):
    try:
        for key, value in dict.items():
            if val in str(value):
                return key
    except ValueError:
        print("Value not in list")


o = Order()
# o.addItem(Appetiser(2, 1, 1, ""))
# o.addItem(Appetiser(3, 7, 4, ""))
# o.addItem(Appetiser(1, 3, 2, ""))
# o.addItem(Bao(1, 1, 2, 1, [0, 2, 3, 2, 2], ""))
# o.addItem(Bao(1, 1, 2, 1, [1, 0, 1, 1, 0], ""))
# o.completeOrder(1672531200)
# o.addItem(Bento(1, 1, [1, 1, 3 ], 1, [     ], 3, [ 2, 0             ], 1, ""))
# print(Classic(1, 1, [2, 0,], 2, [1, 1], "").outputPretty())
#o.completeOrder(1672531200, "")