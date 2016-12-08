import time

word = 'abrakadabra'
text = 'abrakadabrakadabrakadabrakadabrakadabra'

def finditer(word, text):
	def checkWord(word, startIndex):
		for index in range(len(word) - 1):
			yield {"char": word[index], "startIndex": startIndex, "done": False}
		yield {"char": word[index + 1], "startIndex": startIndex, "done": True}

	indexes = []
	entries = []

	for index, char in enumerate(text):
		i = 0
		if char == word[0]:
			entries.append(checkWord(word, index))
		while i < len(entries):
			current = next(entries[i])
			if current["done"]:
				indexes.append(current["startIndex"])
				del entries[i]
			elif current['char'] != char:
				del entries[i]
			else:
				i += 1
	return indexes

print(finditer(word, text))
