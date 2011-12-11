#!/usr/bin/env python
import sys
from exctools import * # we will ship this with the job

def read_input(file):
    for line in file:
	yield line.split()

def main(separator='\t'):
	# input comes from stdin
	data = read_input(sys.stdin)
	for words in data:
		for word in words:
			result = wordExtractor(word) # clean dirty input
			if result:
				if result[0].isupper():
					# write the results to stdout
       					# what we output here will be the input for the reducer task
					# we attach a feature identifier to each feature we send to stdout to prevent 
					# summing of different features on the receiver side. E.g. F0 'it' for the word 'it' with F3 'it' from 'italy'
					# we output pairs 1	0 for seeing the word uppercase, 0	1 for lowercase
					print "%s%s%d%s%d" % ("F0-" + result.lower(), separator, 1, separator, 0)
					if len(result) > 2:
						print "%s%s%d%s%d" % ("F1-" + result[-2:].lower(), separator, 1, separator, 0)
						print "%s%s%d%s%d" % ("F3-" + result[:2].lower(), separator, 1, separator, 0)
						print "%s%s%d%s%d" % ("F2-" + result[-3:].lower(), separator, 1, separator, 0)
						print "%s%s%d%s%d" % ("F4-" + result[:3].lower(), separator, 1, separator, 0)
				else:
					print "%s%s%d%s%d" % ("F0-" + result.lower(), separator, 0, separator, 1)
					if len(result) > 2:
						print "%s%s%d%s%d" % ("F1-" + result[-2:].lower(), separator, 0, separator, 1)
						print "%s%s%d%s%d" % ("F3-" + result[:2].lower(), separator, 0, separator, 1)
						print "%s%s%d%s%d" % ("F2-" + result[-3:].lower(), separator, 0, separator, 1)
						print "%s%s%d%s%d" % ("F4-" + result[:3].lower(), separator, 0, separator, 1)				
	
if __name__ == "__main__":
    main()
