searched_word = input("Enter word:")
 
n = input("Enter n:")
n = int(n)
 
counter = 1
words = []
 
while counter <= n:
    word = input("Enter word:")
    words = words + [word]
 
    counter += 1
 
print(words)
 
word_count = 0
 
for word in words:
    if searched_word == word:
        word_count += 1
 
print(searched_word + " is found" +" " + str(word_count)+ " times")
