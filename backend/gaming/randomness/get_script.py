import random
from ...data.dictionaries import *

def rand_script(dct):
    rand = random.randint(0,len(dct)-1)
    value_taco = list(dct.values())
    if type(value_taco[0]) == str:
        return [value_taco[rand]]
    keyhole = list(dct.keys())
    return [keyhole[rand]] + rand_script[keyhole[rand]]
    
print(rand_script(GOD_DICT))
    
    
