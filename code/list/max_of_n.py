n = input("Enter n:")
n = int(n)
 
numbers = []
start = 1
 
while start <= n:
    number = input("Enter number:")
    number = int(number)
    numbers = numbers + [number]
 
    start += 1
 
current_max = numbers[0]
 
for number in numbers:
    if number > current_max:
        current_max = number
 
print("Max is " + str(current_max))
