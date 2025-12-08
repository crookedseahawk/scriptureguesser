import re

path = "prep.csv"
old_file = "old.csv"
new_file = "new.csv"


def divide(path):
    with open(path) as f:
        all_of_it = f.read()
    ind = all_of_it.find("The New Testament of the King James Bible")
    old_test = all_of_it[:ind]
    new_test = all_of_it[ind:]
    return old_test,new_test

old,new = divide(path)

def write_files(old,new):
    with open(old_file,"w") as o:
        o.write(old)
    with open(new_file,"w") as n:
        n.write(new)

write_files(old,new)

def conquer(string,file):
    ind = 0
    boolean = True
    f = open(file, "w")
    for i in range(len(string)):
        try:
            int(string[i])
            if boolean == True:
                pass
            else:
                pass
            i+=4
        except:
            pass
    f.close()


def format(s):
    if s[3] == " ":
        print(s[2] + s[1] + ' "' + s[4:] + '",')
    else:
        print(s[2:4] + s[1] + ' "' + s[5:] + '",')

