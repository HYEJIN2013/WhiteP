n = input("Enter n:")
n = int(n)
  
numbers = []
start = 1
  
while start <= n:
    number = input("Enter number:")
    number = int(number)
    numbers = numbers + [number]
  
    start += 1
  
current_min = numbers[0]
  
for number in numbers:
    if number < current_min:
        current_min = number
  
print("Min is " + str(current_min))
