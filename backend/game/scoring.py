from backend.data.dictionaries import *
from math import exp

def calc_score(guess,correct):
    MAX_POINTS = 5000
    D = 200
    weights = [400,100,20,1]
    total = 0
    for i in range(4):
        if guess[i] == correct[i][1]:
            total += 0
        else:
            total += weights[i] * abs(guess[i]-correct[i][1])

    return int(MAX_POINTS * exp(-total/D))


print(calc_score([0,0,0,0],[(0,1),(0,0),(0,0),(0,0)]))