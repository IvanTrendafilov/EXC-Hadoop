#!/usr/bin/env python
import sys
from exctools import *
def read_input(file):
    for line in file:
	yield line

def main(separator='\t'):
	# input comes from stdin
	data = read_input(sys.stdin)
	for word in data:
		result = wordExtractor(word)
		# Similarly to the local implementation, create five features if the word is more than 2 characters, one otherwise
		if result:
			if len(result) > 2:
				print "%s%s%s%s%s%s%s%s%s" % (result.lower(), separator, result[-2:].lower(), separator, result[-3:].lower(), separator, result[:2].lower(), separator, result[:3].lower())
			else:
				print "%s" % (result.lower())

if __name__ == "__main__":
    main()
