import string, copy, os, sys
from exctools import *
f= open(sys.argv[1],'r')
f2 = open('test-truth.txt','r')
list1 = []
list2 = []
for line in f:
	result = wordExtractor(line)
	if result:
		list1.append(result)
		
for line in f2:
	result = wordExtractor(line)
	if result:
		list2.append(result)
		
f.close()
f2.close()
count = 0
total = len(list2)
for element in list1:
	if element in list2:
		list2.remove(element)
		count += 1

print "Accuracy: ", (count / float(total)) * 100
