#!/usr/bin/env python
import sys

# input comes from stdin
separator = '\t'
for line in sys.stdin:
	line = line.strip()
	feature, uppercount, lowercount = line.split('\t', 2) #unpack
	uppercount = int(uppercount)
	lowercount = int(lowercount)
	total = uppercount + lowercount
	# calculate using the standard formula
	print '%s%s%s%s%s' % (feature, separator, (uppercount / float(total)), separator, (lowercount / float(total)))
