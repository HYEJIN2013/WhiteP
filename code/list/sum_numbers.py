n = input("Enter n: ")
n = int(n)
 
start = 0
numbers = []
 
while start < n:
    number = input()
    number = int(number)
     
    numbers = numbers + [number]
 
    start += 1
 
 
sum = 0
 
for number in numbers:
    sum = sum + number
 
print("Total sum is: " + str(sum))
