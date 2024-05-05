# Library imports
import time
from time import strftime

# My imports
from main import db, cursor
from emails import sendEmail
from functions import ordinal, floatToPrice

# Comments won't be very detailed here
# Most things are pretty self-explanatory
# The string manipulation is quite complicated, but it doesn't need to be fully understood. They work

# Modifier types overhead
modTypes = {
    1: {0: "No", 1: "Less", 2: "With", 3: "Extra"},                 # Pepper, onion, etc.
    2: {0: "No", 1: "Yes"},                                         # Basic
    3: {0: "Less hot", 1: "Normal", 2: "More hot"},                 # Spiciness of food
    4: {1: "Normal", 2: "More"},                                    # Spiciness of curry
    5: {0: "No", 1: "Less", 2: "With", 3: "Extra", 4: "Separate"}   # Mayo
}
# Sauces
sauceDict = {
    -1: "",
    0: "No sauce",
    1: "Sweet Chilli Sauce [Vgn]",
    2: "Micro Curry [Veg]",
    3: "Small Curry [Veg]",
    4: "Curry [Veg]",
    5: "Soy Sauce [Vgn]",
    6: "Mayo [Veg]",
    7: "Spicy Mayo [Veg]",
    8: "Hoisin Mayo [Veg]",
    9: "Vegan Mayo [Vgn]",
    10: "Korean Sauce [Vgn]",
    11: "Peking Sauce",
    12: "Sweet and Sour Sauce"
}

### Mods
hot =           {'name': 'Hot',             'modType': 3, 'default': 1}
hotCurry =      {'name': 'Hot',             'modType': 4, 'default': 1}
pepper =        {'name': 'Pepper',          'modType': 1, 'default': 2}
onion =        [{'name': 'Onion',           'modType': 1, 'default': 2}, {'name': 'Onion', 'modType': 2, 'default': 0}]
carrot =        {'name': 'Carrot',          'modType': 1, 'default': 2}
pineapple =     {'name': 'Pineapple',       'modType': 1, 'default': 2}
beanSprout =    {'name': 'Bean Sprouts',    'modType': 1, 'default': 2}
chicken =       {'name': 'Chicken',         'modType': 1, 'default': 2}
pork =          {'name': 'Pork',            'modType': 1, 'default': 2}
egg =           {'name': 'Egg',             'modType': 1, 'default': 2}
wellDone =      {'name': 'Well done',       'modType': 2, 'default': 0}
lemon =         {'name': 'Lemon',           'modType': 2, 'default': 1}
peas =         [{'name': 'Peas', 'modType': 1, 'default': 0}, {'name': 'Peas', 'modType': 1, 'default': 2}]
pickles = [
    {'name': 'White Cabbage', 'modType': 2, 'default': 1}, 
    {'name': 'Cucumber', 'modType': 2, 'default': 1}, 
    {'name': 'Carrots', 'modType': 2, 'default': 1}, 
    {'name': 'Red Cabbage', 'modType': 2, 'default': 1}, 
    {'name': 'Lime', 'modType': 2, 'default': 0}, 
]



appetiserPermittedSauces = [0, 1, 2, 5]
appetisers = {
    1:  {'name': 'Spring Rolls',              'price': 4.00,  'mod': [],   'defaultSauce': 1,  'desc': "Shredded duck and veg in delicious Korean sauce wrapped in a crispy egg sheet"},
    2:  {'name': 'Thai Spring Rolls [Veg]',   'price': 4.00,  'mod': [],   'defaultSauce': 1,  'desc': "Noodle, mushroom, and veg wrapped in a crispy egg sheet"},
    3:  {'name': 'Teriyaki Wings',            'price': 6.00,  'mod': [],   'defaultSauce': -1, 'desc': "Deep fried chicken wings slathered in a delicious teriyaki sauce"},
    4:  {'name': 'Korean Wings',              'price': 6.00,  'mod': [],   'defaultSauce': -1, 'desc': "Deep fried chicken wings coated in a spicy Korean sauce"},
    5:  {'name': 'Thai Prawn Crackers [Vgn]', 'price': 3.50,  'mod': [],   'defaultSauce': -1, 'desc': "A big bag of crispy, flavourful thai prawn crackers"},
    6:  {'name': 'Gyoza',                     'price': 7.00,  'mod': [wellDone],              'defaultSauce': 5,  'desc': "Delectable homemade gyoza dumplings"},
    7:  {'name': 'Honey Ribs',                'price': 7.00,  'mod': [wellDone, lemon],       'defaultSauce': -1, 'desc': "Pork ribs doused with honey with a sliced lemon"},
    8:  {'name': 'Peking Ribs',               'price': 7.00,  'mod': [wellDone],              'defaultSauce': -1, 'desc': "Pork ribs covered with a hot and spicy peking sauce"},
    9:  {'name': 'Salted Chilli Chicken',     'price': 6.00,  'mod': [pepper, onion[0], hot], 'defaultSauce': -1, 'desc': "Crispy shredded chicken with sliced pepper and onion, all mixed with spicy salt and chilli flakes"},
    10: {'name': 'Spice Bowl',                'price': 6.50,  'mod': [pepper, onion[0], hot], 'defaultSauce': 3,  'desc': "A bowl of spicy potato wedges, popcorn chicken, and chicken chunks with a helping of sliced pepper and onion"},
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
        return {"count": self.count, "details": [self.appetiser, self.mod, self.sauce], "note": self.note}

    def outputPretty(self):
        appetiser = appetisers[self.appetiser]
        final = {"title": "", "mod": [], "sauce": "", "price": appetiser['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{appetiser['name']}{'' if self.sauce == appetiser['defaultSauce'] and all([(d['default'] == m) for (d, m) in zip(appetiser['mod'], self.mod)]) else ' (Mod.)'}"
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
    1: {'name': 'Chicken',   'price': 7.50, 'pickles': [2, 0, 2, 2, 0], 'sauce': 7, 'desc': "2 salted chilli chicken baos with spicy mayo"},
    2: {'name': 'Duck',      'price': 8.00, 'pickles': [2, 0, 2, 2, 2], 'sauce': 8, 'desc': "2 aromatic duck confit baos with tangy hoisin sauce and sweet hoisin mayo"},
    3: {'name': 'Rib',       'price': 7.50, 'pickles': [0, 2, 2, 2, 0], 'sauce': 8, 'desc': "2 pulled slow cooked rib baos with sweet tangy peking sauce and sweet hoisin mayo"},
    4: {'name': 'Pork',      'price': 7.50, 'pickles': [0, 2, 2, 2, 2], 'sauce': 8, 'desc': "2 baos of tender braised pork in a delicious tangy sauce with sweet hoisin mayo"},
    5: {'name': 'Veggie [Veg]',    'price': 7.00, 'pickles': [2, 0, 2, 2, 2], 'sauce': 7, 'desc': "2 tempura sweet potato baos with spicy mayo"},
    6: {'name': 'Vegan [Vgn]',     'price': 7.00, 'pickles': [2, 0, 2, 2, 2], 'sauce': 9, 'desc': "2 baos of pulled jackfruit marinated in a classic Chinese bbq sauce with vegan hoisin mayo"},
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
        return {"count": self.count, "details": [self.meat, self.sauce, self.sauceMod, self.pickles], "note": self.note}

    def outputPretty(self):
        meat = baos[self.meat]['name']
        default = list(baos[self.meat].values())[2:4]
        final = {"title": "", "sauce": "", "pickles": ["", "", "", "", ""], "price": baos[self.meat]['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{meat} Bao {'' if self.sauce == default[1] and self.pickles == default[0] else ' (Mod.)'}"
        final['sauce'] = f"No sauce" if self.sauce == 0 else f"{modTypes[1][self.sauceMod]} {sauceDict[self.sauce]}"
        for p, i in zip(self.pickles, range(0, 5)):
            final['pickles'][i] = f"{modTypes[1][p]} {picklesDict[i+1]}"
        return final


# This takes from sides instead of the sauces
bentoPermittedSauces = [4, 5, 6, 7, 8, 9, 10]
bentos = {
    1:  {'name': 'Salted Chilli Chicken',    'price': 9.30, 'mod': [pepper, onion[0], hot],                 'sauce': 4,  'side1': [1, []], 'side2': [2, []], 'desc': "Crispy shredded chicken with sliced pepper and onion, all mixed with spicy salt and chilli flakes"},   
    2:  {'name': 'Honey Chilli Chicken',     'price': 9.30, 'mod': [pepper, onion[0], hot],                 'sauce': -1, 'side1': [1, []], 'side2': [2, []], 'desc': "Shredded chicken with sliced pepper and onion tossed in our sweet chilli sauce"},     
    3:  {'name': 'Peking Chicken',           'price': 9.30, 'mod': [pepper, onion[0]],                      'sauce': -1, 'side1': [1, []], 'side2': [2, []], 'desc': "Shredded chicken with sliced pepper and onion coated with a sweet and tangy peking sauce"},
    4:  {'name': 'Honey Beef',               'price': 9.30, 'mod': [pepper, onion[0], hot],                 'sauce': -1, 'side1': [1, []], 'side2': [2, []], 'desc': "Triple cooked shredded beef with sliced pepper and onion tossed in our sweet chilli sauce"}, 
    5:  {'name': 'Peking Beef',              'price': 9.30, 'mod': [pepper, onion[0]],                      'sauce': -1, 'side1': [1, []], 'side2': [2, []], 'desc': "Tripled cooked shredded beef with sliced pepper and onion coated with a sweet and tangy peking sauce"}, 
    6:  {'name': 'Sriracha Noodles',         'price': 9.30, 'mod': [pepper, onion[0], pork, chicken, hot],  'sauce': -1, 'side1': [5, []], 'side2': [6, [1, 1, 1, 1, 1]], 'desc': "Noodles with Chinese bbq pork and chicken tossed in a spicy Thai sriracha sauce"},
    7:  {'name': 'Teriyaki Noodles [Veg]',   'price': 9.30, 'mod': [carrot, beanSprout, onion[0], peas[1]], 'sauce': -1, 'side1': [1, []], 'side2': [6, [1, 1, 1, 1, 0]], 'desc': "Thicker noodles with carrot and beansprouts tossed in a tangy teriyaki sauce"},
    8:  {'name': 'Katsu Chicken',            'price': 9.30, 'mod': [pickles[0]],                            'sauce': 4,  'side1': [1, []], 'side2': [2, []], 'desc': "Panko fried chicken breast on a bed of white cabbage"},
    9:  {'name': 'Korean Fried Chicken',     'price': 9.30, 'mod': [pickles[0]],                            'sauce': 6,  'side1': [5, []], 'side2': [2, []], 'desc': "Spicy, crispy fried chicken strips on a bed of white cabbage"},
    10: {'name': 'Squid',                    'price': 9.80, 'mod': [pepper, onion[0], hot],                 'sauce': 4,  'side1': [1, []], 'side2': [2, []], 'desc': "Breaded shredded squid with sliced pepper and onion, all mixed with spicy salt and chilli flakes"}
}
bentoSides = {
    1: {'name': 'Spring Rolls',         'mod': []},
    2: {'name': 'Steamed Rice [Vgn]',   'mod': []},
    3: {'name': 'Fried Rice [Veg]',     'mod': [egg, peas[0]]},
    4: {'name': 'Noodles',              'mod': [chicken, onion[0], beanSprout]},
    5: {'name': 'Hot Wings',            'mod': []},
    6: {'name': 'Pickles [Vgn]',        'mod': pickles[0:5]}
}

class Bento():
    def __init__(self, count: int, main: int, mainMod: list[int], side1: int, side1Mod: list[int], side2: int, side2Mod: list[int], sauce: int, sauceMod: list[int], note: str):
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
        return {"count": self.count, "details": [self.main, self.mainMod, self.side1, self.side1Mod, self.side2, self.side2Mod, self.sauce, self.sauceMod], "note": self.note}

    def outputPretty(self):
        main = bentos[self.main]['name']
        side1 = bentoSides[self.side1]['name']
        side2 = bentoSides[self.side2]['name']
        default = bentos[self.main]
        final = {"title": "", "mainMod": [], "side1": "", "side1Mod": [], "side2": "", "side2Mod": [], "sauce": "", "sauceMod": [], "price": bentos[self.main]['price'] * self.count}
        final['title'] = f"{f'🔴 ' if self.note else ''}{f'{self.count} ' if self.count > 1 else ''}{main}{'' if all([self.mainMod == [d['default'] for d in default['mod']], self.sauce == default['sauce'], all([(d['default'] == m) for (d, m) in zip(sides[self.sauce]['mod'], self.sauceMod)]), [self.side1, self.side1Mod] == default['side1'], [self.side2, self.side2Mod] == default['side2']]) else ' (Mod.)'}"
        for i in range(0, len(bentos[self.main]['mod'])):
            final['mainMod'].append(f"{modTypes[bentos[self.main]['mod'][i]['modType']][self.mainMod[i]]} {bentos[self.main]['mod'][i]['name']}")
        
        final['side1'] = side1 if all([1 for m in bentoSides[self.side1]['mod']]) else f"{side1} (Mod.)"
        for i in range(0, len(self.side1Mod)):
            final['side1Mod'].append(f"{modTypes[bentoSides[self.side1]['mod'][i]['modType']][self.side1Mod[i]]} {bentoSides[self.side1]['mod'][i]['name']}")

        final['side2'] = side2 if all([1 for m in bentoSides[self.side2]['mod']]) else f"{side2} (Mod.)"
        for i in range(0, len(self.side2Mod)):
            final['side2Mod'].append(f"{modTypes[bentoSides[self.side2]['mod'][i]['modType']][self.side2Mod[i]]} {bentoSides[self.side2]['mod'][i]['name']}")

        final['sauce'] = f"{sides[self.sauce]['name']}{'' if all((d['default'] == m) for (d, m) in zip(sides[self.sauce]['mod'], self.sauceMod)) else ' (Mod.)'}"
        for i in range(0, len(self.sauceMod)):
            final['sauceMod'].append(f"{sides[self.sauce]['mod'][i]['name']}")

        return final



classics = {
    1:  {'name': 'Sweet & Sour Chicken',  'price': 7.80, 'mod': [pepper, onion[0], pineapple], 'side': 1, 'desc': "Crispy fried chicken chunks coated with a delicious sweet & sour sauce with sliced pepper, onion, and pineapple"},
    2:  {'name': 'Honey Chilli Chicken',  'price': 8.20, 'mod': [pepper, onion[0], hot],       'side': 1, 'desc': "Shredded chicken with sliced pepper and onion tossed in our sweet chilli sauce"},     
    3:  {'name': 'Peking Chicken',        'price': 8.20, 'mod': [pepper, onion[0]],            'side': 1, 'desc': "Shredded chicken with sliced pepper and onion coated with a sweet and tangy peking sauce"},
    4:  {'name': 'Honey Chilli Beef',     'price': 8.20, 'mod': [pepper, onion[0], hot],       'side': 1, 'desc': "Triple cooked shredded beef with sliced pepper and onion tossed in our sweet chilli sauce"}, 
    5:  {'name': 'Peking Beef',           'price': 8.20, 'mod': [pepper, onion[0]],            'side': 1, 'desc': "Triple cooked shredded beef with sliced pepper and onion coated with a sweet and tangy peking sauce"},
    6:  {'name': 'Black Bean Chicken',    'price': 7.80, 'mod': [pepper, onion[0], hot],       'side': 1, 'desc': "Pieces of chicken in a rich black bean sauce with a hint of chilli"},
    7:  {'name': 'Chicken Fried Rice',    'price': 7.80, 'mod': [egg, peas[1]],                'side': -1, 'desc': "Wok-fried chicken atop our delicious egg-fried rice"},
    8:  {'name': 'Chicken Curry',         'price': 7.80, 'mod': [onion[0], peas[1], hot],      'side': 1, 'desc': "Pieces of chicken with onion and pepper, slathered with our signature curry"},
    9:  {'name': 'Veggie Curry [Veg]',    'price': 7.80, 'mod': [pepper, onion[0], peas[1], beanSprout, hot],  'side': 1,  'desc': "Assorted wok-fried vegetables slathered with our signature curry"},
    10: {'name': 'Satay Chicken',         'price': 7.80, 'mod': [pepper, onion[0], carrot, hot],                     'side': -1, 'desc': "Crispy fried chicken chunks doused with a sweet tangy Malaysian satay sauce"},
    11: {'name': 'Sriracha Noodle',       'price': 7.80, 'mod': [pepper, onion[0], pork, chicken, hot],              'side': -1, 'desc': "Noodles with Chinese bbq pork and chicken tossed in a spicy Thai sriracha sauce"},
    12: {'name': 'Teriyaki Noodle [Veg]', 'price': 7.80, 'mod': [carrot, beanSprout, onion[0], peas[1]],       'side': -1, 'desc': "Thicker noodles with carrot and beansprouts tossed in a tangy teriyaki sauce"},
}

classicSides = {
    0: {'name': 'No side',              'mod': []},
    1: {'name': 'Steamed Rice [Vgn]',   'mod': []},
    2: {'name': f'Fried Rice [Veg]',    'mod': [egg, peas[0]]},
    3: {'name': 'Noodles',              'mod': [chicken, onion[0], beanSprout]},
}

class Classic():
    def __init__(self, count: int, classic: int, classicMod: list[int], side: int, sideMod: list[int], note: str):
        self.type = "classics"
        self.count = count
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
    1:  {'name': 'Steamed Rice [Vgn]',          'price': 2.50, 'mod': [],                              'desc': "Soft steamed rice that goes with everything"},
    2:  {'name': 'Fried Rice [Veg]',            'price': 3.00, 'mod': [egg, peas[0]],                  'desc': "Delicious egg-fried rice with a soy aroma and a choice for peas"},
    3:  {'name': 'Noodles',                     'price': 3.50, 'mod': [chicken, onion[0], beanSprout], 'desc': "Wok-fried egg noodles with chicken, onion, and beansprouts"},
    4:  {'name': 'Curry [Veg]',                 'price': 2.00, 'mod': [hotCurry, onion[1]],            'desc': "Our signature mildly-spicy curry"},
    5:  {'name': 'Small Curry [Veg]',           'price': 1.50, 'mod': [hotCurry, onion[1]],            'desc': "Our signature mildly-spicy curry"},
    6:  {'name': 'Korean Sauce [Veg]',          'price': 2.00, 'mod': [],                              'desc': "A tub of our tangy Korean barbecue sauce"},
    7:  {'name': 'Sweet Chilli Sauce [Vgn]',    'price': 2.00, 'mod': [hotCurry],                      'desc': "A small tub of our sweet chilli sauce"},
    8:  {'name': 'Soy Sauce [Vgn]',             'price': 2.00, 'mod': [],                              'desc': "A small tub of our black vinegar and soy sauce"},
    9:  {'name': 'Peking Sauce [Vgn]',          'price': 2.00, 'mod': [hotCurry],                      'desc': "A small tub of our hot and spicy peking sauce"},
    10: {'name': 'Sweet and Sour Sauce [Vgn]',  'price': 2.00, 'mod': [hotCurry],                      'desc': "A small tub of our deliciously tangy sweet and sour sauce"},
    11: {'name': 'Coke [Vgn]',                  'price': 2.00, 'mod': [],                              'desc': "A 330ml can of Coca-Cola"},
    12: {'name': 'Water [Vgn]',                 'price': 2.00, 'mod': [],                              'desc': "A 500ml bottle of still water"},
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
        self.customerID = 0

    # Assign a customer ID to the order
    def assignCustomer(self, ID: int):
        self.customerID = ID

    # Add an item to the order
    def addItem(self, item: object):
        self.content[item.type].append(item.returnObject())

    # Remove an item from the order
    def delItem(self, type: str, index: int):
        self.content[type].pop(index)

    # Checks if the order is blank
    def isBlank(self):
        if self.content == {"appetisers": [], "baos": [], "bentos": [], "classics": [], "sides": []}:
            return True
        return False

    # Get the plain content of the order
    def getOrderContent(self):
        return self.content

    # Return the order as a string
    def returnOrder(self):
        return f"{self.customerID}, '{str(self.content).replace("'", '"')}', 0, 0, {int(time.time() - 1704067200)}"
    
    # Get the total price of the order
    def getTotalPrice(self):
        price = 0.00
        for t in ["appetisers", "baos", "bentos", "classics", "sides"]:
            for c in self.content[t]:
                price += float(getType[t][c['details'][0]]['price']) * float(c['count'])
        return price

    # Complete the order and add it to the system
    # Also sends an email to the customer
    def completeOrder(self, pickupTime: int, note: str):
        from documents import createOrderReceipt
        order = self.returnOrder()
        cursor.execute(f"""
            INSERT INTO orders (customerID_FK, orderData, complete, paid, placementTime, pickupTime, note)
            VALUES
            ({order}, {pickupTime}, '{note}')
        """)
        db.commit()
        cursor.execute(f"SELECT orderID FROM orders ORDER BY orderID")
        orderID = cursor.fetchall()[-1][0]
        
        if(self.customerID):
            createOrderReceipt(order = orderID)
            cursor.execute(f"SELECT email FROM customers WHERE customerID = {self.customerID}")
            email = cursor.fetchone()[0]
            placementTime = time.localtime(int(time.time()))
            pickupTime = time.localtime(pickupTime + 1704067200)
            # This can be commented out later
            extra = "(If you have received this email and don't know what it is you can safely ignore it. I am just a student testing out my school project and your email happened to match up with random test emails I've entered.)"
            sendEmail(email,
                        "Order Receipt",
                        f"Thank you for your patronage! Please find your order receipt attached.\
                            \n{extra}\
                            \n\
                            \nPlaced: {strftime("%A", placementTime)} {ordinal(int(strftime("%d", placementTime)))} {strftime("%B, %Y at %H:%M", placementTime)}\
                            \nPickup Time: {strftime("%A", pickupTime)} {ordinal(int(strftime("%d", pickupTime)))} {strftime("%B, %Y at %H:%M", pickupTime)}\
                            \nPrice: {floatToPrice(self.getTotalPrice())}",
                            f"documents/orderReceipts/{orderID}.docx")

# Returns the category of the item from a string
getType = {
    "appetisers": appetisers,
    "baos": baos,
    "bentos": bentos,
    "classics": classics,
    "sides": sides
}