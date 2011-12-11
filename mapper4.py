#!/usr/bin/env python
import sys, glob, os, math
# This is the part of the code that could really from HBase.
# Since this is not available, we create a dictionary from the output of the label calculation task
# and store it in memory for each mapper.
# This is still very quick. The job completes for a little over a minute. E.g.:
# http://hcrc1425n32.inf.ed.ac.uk:50030/jobdetails.jsp?jobid=job_201111200358_2816 
def makedict():
	features = dict()
	for i in range(5):
		features[i] = dict()

	for filename in glob.glob(os.path.join('*.sym')): # we've passed hdfs files with the -cacheFile option, which create symlinks for python to use
		current_file = open(filename, 'r')
		for line in current_file:
			if line:
				feature, probUpper, probLower = line.split('\t', 2)
				i = int(feature[1])
				ft = feature[3:]
				features[i][ft] = (probUpper, probLower[:-1])
	return features

def read_input(file):
    for line in file:
	yield line

def main(separator='\t'):
	features = makedict()
	data = read_input(sys.stdin)
	for line in data:
		try:
			f0, f1, f2, f3, f4 = line.split('\t', 4) # unpack
			if f0 in features[0]:
				prob0 = features[0][f0]
			else:
				prob0 = (0.5, 0.5) # simplification: assuming all evidences are equally distributed
			if f1 in features[1]:
				prob1 = features[1][f1]
			else:
				prob1 = (0.5, 0.5)
			if f2 in features[2]:		
				prob2 = features[2][f2]
			else:
				prob2 = (0.5, 0.5)
			if f3 in features[3]:		
				prob3 = features[3][f3]
			else:
				prob3 = (0.5, 0.5)
			if f4[:-1] in features[4]:
				prob4 = features[4][f4[:-1]]
			else:
				prob4 = (0.5, 0.5)
			# fixing underflow, calculating probabilities. explained in localbayes.py
			probUpper = math.log(float(prob0[0])) + math.log(float(prob1[0])) + math.log(float(prob2[0])) + math.log(float(prob3[0])) + math.log(float(prob4[0]))
			probLower = math.log(float(prob0[1])) + math.log(float(prob1[1])) + math.log(float(prob2[1])) + math.log(float(prob3[1])) + math.log(float(prob4[1]))
			print "%s\t%s\t%s" % (f0, probUpper, probLower)
		except ValueError:
			f0 = line.strip()
			if f0 in features[0]:
				prob0 = features[0][f0]
			else:
				prob0 = (0.5, 0.5)
			probUpper = math.log(float(prob0[0]))
			probLower = math.log(float(prob0[1]))
			print "%s\t%s\t%s" % (f0, probUpper, probLower)
			# it is worth to mention that at this stage, we can just compare the two probabilities
			# and output the 
			

if __name__ == "__main__":
	main()

