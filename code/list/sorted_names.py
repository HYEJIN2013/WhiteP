n = input("Enter n:")
n = int(n)
 
names = []
counter = 1
 
while counter <= n:
    name = input("Enter name:")
    names = names +[name]
 
    counter += 1
 
print("Sorted names are: ")
names = sorted(names)
 
for name in names:
    print(name)
