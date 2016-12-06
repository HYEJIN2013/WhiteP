import random
import dbm
import pickle
import sys

inp = 0
trys = 0
minn = 0
maxn = 0
get_inp = True
ntg = 0

def save():
    dump1 = pickle.dumps(minn)
    dump2 = pickle.dumps(maxn)
    dbs = dbm.open("save.db", "c")
    dbs["min"] = dump1
    dbs["max"] = dump2

def load():
    dbs = dbm.open("save.db", "c")
    load1 = pickle.loads(dbs["min"])
    load2 = pickle.loads(dbs["max"])
    return [load1, load2]

def inputnumber():
    print("Please type a number between %s and %s" % (minn, maxn))
    return int(input("Type number here: "))
    
def checknumber(number):
    if inp > ntg:
        print("Try lower")
        return False
    if inp < ntg:
        print("Try higher")
        return False
    if inp == ntg:
        print("Good job, you took %s try(s), press enter..." % trys)
        input()
        return True

print("Please use numbers (without decimals) when inputing")
while get_inp:
    inp = input("Do you want to save or load (s or l)")
    if inp == "s":
        while(get_inp):
            try:
                minn = int(input('Set min: '))
                maxn = int(input('Set max: '))
                get_inp = False
            except ValueError:
                print('Invald input')
        save()
    elif inp == "l":
        loads = load()
        maxn = loads[0]
        minn = loads[1]
        get_inp = False
    else:
        print("Invald input")
ntg = random.randint(minn, maxn)
while True:
    inp = inputnumber()
    if checknumber(inp):
        ntg = random.randint(minn, maxn)
        trys = 0
        sys.exit()
    else:
        trys = trys + 1
