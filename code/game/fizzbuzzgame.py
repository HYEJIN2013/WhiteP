n = 1
try: 
  upper_limit = int(raw_input("Enter a counting limit: ")) 
except ValueError: 
  print "Please enter a numeric value." 
  upper_limit = int(raw_input("Enter a counting limit: ")) 

while n < upper_limit: 
    if n % 3 == 0 and n % 5 == 0:
        print "fizz buzz"
    elif n % 3 == 0:
        print "fizz"
    elif n % 5 == 0:
        print "buzz"
    else:
        print "Fizz buzz counting up to " + str(n)  
    n = n + 1   
