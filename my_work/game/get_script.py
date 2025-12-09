import random
from my_work.data.dictionaries import *

def rand_script(dct):
    rand = random.randint(0,len(dct)-1)
    value_taco = list(dct.values())
    keyhole = list(dct.keys())
    if type(value_taco[0]) == str:
        return [(keyhole[rand],rand)]
    return [(keyhole[rand],rand)] + rand_script(dct[keyhole[rand]])
    
print(rand_script(GOD_DICT))
    
    
