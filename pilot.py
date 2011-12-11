#!/usr/bin/python
import os
basedir = '/user/s0837795/data' #set this according to your fs
hadoop = '/opt/hadoop/hadoop-0.20.2/bin/hadoop' #this is where hadoop is

os.system(hadoop + ' fs -rmr ' + basedir + '/*')
os.system(hadoop + ' jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -input /user/miles/data/large.txt -output '+ basedir +'/tmp -mapper mapper1.py -reducer reducer1.py -file mapper1.py -file reducer1.py -file exctools.py')
os.system('sleep 5')
os.system(hadoop + ' jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -D mapred.reduce.tasks=0 -input '+basedir+'/tmp -output '+ basedir + '/labels -mapper mapper2.py -file mapper2.py')
os.system('sleep 5')
os.system(hadoop + ' jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -D mapred.reduce.tasks=0 -input /user/miles/data/test.txt -output ' + basedir + '/features -mapper mapper3.py -file mapper3.py -file exctools.py')
os.system(hadoop + ' fs -ls '+ basedir + '/features > filestmp')
files = open('filestmp','r')
output = []
for line in files:
	output.append(line[:-1])

os.remove('filestmp')
filens = []
for element in output[1:]:
	if 'log' not in element:
		filens.append(element.split('/')[len(element.split('/'))-1])

cmd = hadoop + ' jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -D mapred.reduce.tasks=0 -input '+basedir+'/features -output '+ basedir +'/tmp2 -mapper mapper4.py -file mapper4.py'
count = 0
for filename in filens:
	cmd += ' -cacheFile hdfs://hcrc1425n30.inf.ed.ac.uk' + basedir + '/labels/' + filename + '#' + str(count) + '.sym'
	count += 1

os.system('sleep 4')
os.system(cmd)
os.system('sleep 5')
os.system(hadoop + ' jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -D mapred.reduce.tasks=0 -input '+basedir+'/tmp2 -output ' + basedir + '/final -mapper mapper5.py -file mapper5.py')
