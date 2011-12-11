#!/usr/bin/env python

from operator import itemgetter
import sys

current_feature = None
current_uppercount = 0
current_lowercount = 0
feature = None

# input comes from stdin
separator = '\t'
for line in sys.stdin:
	# remove leading and trailing whitespace
	line = line.strip()

	# unpack the input we got from mapper1.py
	feature, ucount, lcount = line.split('\t', 2)

	# convert feature count (currently a string) to int
	try:
		ucount = int(ucount)
		lcount = int(lcount)
	except ValueError:
	# we've got junk, so discard this line
		continue

	# this IF-switch only works because Hadoop sorts map output
	# Hadoop sorts map output by key before it passes it to the reducer
	if current_feature == feature:
		current_uppercount += ucount
		current_lowercount += lcount
	else:
		if current_feature:
			# write result to STDOUT
			print '%s%s%s%s%s' % (current_feature, separator, current_uppercount, separator, current_lowercount)
		current_uppercount = ucount+1 # add one smoothing
		current_lowercount = lcount+1 # add one smoothing
		current_feature = feature

# do output the last feature if needed
if current_feature == feature:
	print '%s\t%s\t%s' % (current_feature, current_uppercount, current_lowercount)

