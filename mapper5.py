#!/usr/bin/env python
import sys, string
def read_input(file):
    for line in file:
	yield line

def main(separator='\t'):
	data = read_input(sys.stdin)
	for line in data:
		try:
			word, upperProb, lowerProb = line.strip().split('\t', 2)
			if len(word) > 1:
				if float(upperProb) > float(lowerProb): # convert to float from string
					if word:
						ctmp = 0
						for char in word:
							if char.isalpha():
								tmp = word[:ctmp] + string.upper(word[ctmp]) + word[(1+ctmp):]
								break
							ctmp += 1
						print "%s" % (tmp)
				else:
					print "%s" % (word)
			else:
				print "%s" % (word)
		except:
			pass

if __name__ == "__main__":
	main()


