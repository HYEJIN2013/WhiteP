
#data = [["a"], ["b",["a"]], ["c",["b",["a"]]], ["d",["c",["b",["a"]]]],"e"]

lista=["a"]
listb=["b",lista]
listc=["c",listb]
listd=["d",listc]
data=[lista,listb,listc,listd,"e"]

print data

def flat(input,output):
    map(lambda x: flat(x,output) if type(x) is list else output.append(x),input)

def flatouput(input,output):
    for elem in input:
        if type(elem) is list:
            flatmap(elem,output)
        else:
            output.append(elem)
            
def flatmap(input):
    ret =[]
    for elem in input:
        ret += flatmap(elem) if type(elem) is list else elem
    return ret

print flatmap(data)
