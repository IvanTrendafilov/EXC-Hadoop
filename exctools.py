#!/usr/bin/env python
# cleans up dirty input. Strips nonalphanumeric chars, except '-' if it is between words
def wordExtractor(word): 
	result = ""
	word = word.strip()
	position = -1
	found = False
	dcount = False
	for char in word:
		position += 1
		if char.isalnum():
			found = True
			result += char
		elif char == '-' and found and not dcount:
			try:
				if word[position - 1].isalnum() and word[position + 1].isalnum():
					result += char
				dcount = True
			except:
				if found:
					break
		elif found:
			break
	return result
