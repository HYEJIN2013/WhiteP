n = input("Enter n:")
n = int(n)
 
counter = 1
numbers = []
 
while counter <= n:
    number = input("Enter number:")
    number = int(number)
 
    numbers = numbers + [number]
 
    counter += 1
 
print(numbers)
 
sum = 0
 
for number in numbers:
    sum = sum + number
 
avg = sum/len(numbers)
 
print("Avg is " + str(avg))
