import string, math
from exctools import *

trainingFile = open('small.txt','r')
features = dict()
# the data structure is organised as a dictionary of dictonaries, e.g. features[0]['italy'] = (5 10) 
# this means we've seen italy as feature 0 (entire word), 5 times uppercase, 10 times lowercase
for i in range(5): 
	features[i] = dict()

allWords = []
for line in trainingFile: # parsing the training file
	if len(line) > 1:
		cleanline = line[0:-1]
	else:
		continue
	line_split = cleanline.split(None)
	for word in line_split:
		result = wordExtractor(word)
		if result:
			allWords.append(result)

for word in allWords: # assigning features & count into features datastructure.
	f = dict()
	f[0], f[1], f[2], f[3], f[4] = word.lower(), word[-2:].lower(), word[-3:].lower(), word[:2].lower(), word[:3].lower()
	in1, in2 = 0, 1
	if word[0].isupper():
		in1 = 1
		in2 = 0
	if len(f[0]) > 1:
		if f[0] in features[0]:
			features[0][f[0]] = (features[0][f[0]][0] + in1, features[0][f[0]][1] + in2)
		else:
			features[0][f[0]] = (1 + in1, 1 + in2) # add one smoothing. Basically we the count from 2.
	if len(f[0]) > 2:	
		for i in range(1, 5):
			if f[i] in features[i]:
				features[i][f[i]] = (features[i][f[i]][0] + in1, features[i][f[i]][1] + in2)
			else:
				features[i][f[i]] = (1 + in1, 1 + in2)  # add one smoothing. Basically we start the count from 2.

# This just converts the observed frequencies of features in the training data to prior probabilities for our model
# e.g. features[0]['italy'] = (5 10) becomes features[0]['italy'] ~= (0.3333 0.6667) by the formula in the assignment
for key in features:
	for key2 in features[key]:
		features[key][key2] = (features[key][key2][0] / float(features[key][key2][0] + features[key][key2][1]), features[key][key2][1] / float(features[key][key2][0] + features[key][key2][1]))

data = open('test.txt','r')
output = ""
for line in data:
	if not (len(line) > 1):
		continue
	cleanline = line.strip()
	line_split = cleanline.split(None)
	for word in line_split:
		result = wordExtractor(word)
		if result:
			f = dict()
			# let's break up the word into features
			f[0], f[1], f[2], f[3], f[4] = result.lower(), result[-2:].lower(), result[-3:].lower(), result[:2].lower(), result[:3].lower()
			upperList, lowerList = [], []
			if f[0] in features[0]:
				upperList.append(features[0][f[0]][0])
				lowerList.append(features[0][f[0]][1])
			else:
				upperList.append(0.50) # simplification: assuming all evidences are equally distributed 
				lowerList.append(0.50)
			if len(f[0]) > 2: # we do not want to add 5 features for short words, e.g. for the word 'an' f0 = f1 = f2 = f3 = f4 = f5
				for i in range(1,5):
					if f[i] in features[i]:
						upperList.append(features[i][f[i]][0])
						lowerList.append(features[i][f[i]][1])
					else:
						upperList.append(0.50)  # simplification: assuming all evidences are equally distributed 
						lowerList.append(0.50)	
			probUpper, probLower = 0, 0
			# fixing possible underflow problems. Basically, since we have an unequality in the form * b * c > e * f * g
			# we can apply log to both sides, without changing the direction of the unequality.
			# proof: we know log(a * b * c) = log(a) + log(b) + log(c), so if we apply log to both sides, we can write the inequality as
			# log(a) + log(b) + log(c) > log(e) + log(f) + log(g) and it will hold for all cases.  
			for element in upperList:
				probUpper += math.log(element)
			for element in lowerList:
				probLower += math.log(element)
			if probUpper > probLower: 
				ctmp = 0
				for char in result: # capitalize the word before we write it to output
					if char.isalpha():
						tmp = result[:ctmp] + string.upper(result[ctmp]) + result[(1+ctmp):]
						break
					ctmp += 1
					tmp = result
				output += tmp + '\n'
			else:
				output += result + '\n'

myfile = open('result.txt','w')
myfile.write(output)
