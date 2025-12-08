import random
from data.dictionaries import *

def rand_script(dct):
    rand = random.randint(0,len(dct)-1)
    value_taco = list(dct.values())
    keyhole = list(dct.keys())
    if type(value_taco[0]) == str:
        return [keyhole[rand]]
    return [keyhole[rand]] + rand_script(dct[keyhole[rand]])
    
print(rand_script(GOD_DICT))
    
    
