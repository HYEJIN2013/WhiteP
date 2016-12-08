import random
def list_even():
    import random
    list1 = random.sample(range(30), random.randint(5,10))
    even_list1 = [num  for num in list1 if num % 2 == 0]
    print even_list1

list_even()

""" pick same elements from two different lists"""
list_a = random.sample(range(30),random.randint(10,15))
list_b = random.sample(range(30),random.randint(10,15))
def pick_common():
    list_c = [a for a in list_a if a in list_b]
    print list_c
    print list_a
    print list_b

pick_common()
