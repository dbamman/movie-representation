import sys
from scipy.stats import spearmanr
import numpy as np

gold={}

def read_gold(filename):

	leads=[]
	nonleads=[]

	with open(filename) as file:
		file.readline()
		for line in file:
			cols=line.rstrip().split("\t")
			imdb_tt=cols[0]
			idd=cols[3]
			mins=float(cols[8])
			lead=cols[9]

			if idd.lstrip().rstrip() == "" or imdb_tt.lstrip().rstrip() == "":
				continue

			if idd not in gold:
				gold[idd]={}

			gold[idd][imdb_tt]=mins


def proc(filename):

	golds=[]
	preds=[]
	mults=[]
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			imdb_tt=cols[3]		
			mins=float(cols[4])

			if idd in gold and imdb_tt in gold[idd]:
				gold_mins=gold[idd][imdb_tt]

				mult=gold_mins/mins

				mults.append(mult)

				golds.append(gold_mins)
				preds.append(mins)

	rho, pval=spearmanr(golds, preds)
	print("%.3f\t%s\t%s\t%s" % (rho, pval, len(preds), np.median(mults)))


read_gold(sys.argv[1])				
proc(sys.argv[2])