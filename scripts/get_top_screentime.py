import sys
from collections import Counter

targets={}
names={}
def read_names(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			names[cols[0]]=cols[1]

def read_meta(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			if cols[6] == "Y":
				idd=cols[4]
				targets[idd]=1

def proc(filename):
	counts=Counter()
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			imdb_id=cols[3]
			mins=float(cols[4])
			counts[imdb_id]+=mins


	for k,v in counts.most_common(100):
		hours=int(v/60)
		mins=round(v-(hours*60))
		name=k
		if k in names:
			name=names[k]
		print("%s\t%s:%s" % (name,hours,str(mins).zfill(2)))			
		# print("%s&%s:%s \\\\" % (names[k],hours,str(mins).zfill(2)))			

read_names(sys.argv[3])
read_meta(sys.argv[1])		
proc(sys.argv[2])