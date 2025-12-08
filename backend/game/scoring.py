from backend.data.dictionaries import *

def score(guess,correct):
    MAX_POINTS = 5000
    weights = [0,.2,.3,.5]
    book_distance = 3
    if guess == correct:
        return MAX_POINTS
    if guess[0] != correct[0]:
        return 0
    for i in range():
        pass
    if guess[1] != correct[1]:
        return max(MAX_POINTS * (1 - (abs(guess[1]-correct[1]))/book_distance), 0)
    if guess[2] != correct[2]:
        return max(MAX_POINTS * (1 - (abs(guess[2]-correct[2]))/book_distance), 0)
    if guess[3] != correct[3]:
        return max(MAX_POINTS * (1 - (abs(guess[3]-correct[3]))/book_distance), 0)
    
print(score([0,0,0,0],[0,0,1,0]))