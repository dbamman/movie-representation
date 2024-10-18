import sys
import numpy as np
from scipy.stats import permutation_test

def statistic(x, y, axis):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

def read_top50(filename, colname):

	all_years=[]

	with open(filename) as file:
		header=file.readline().split("\t")
		colnum=header.index(colname)

		for line in file:
			cols=line.rstrip().split("\t")
			if cols[6] == "Y":
				year=cols[0]
				if cols[colnum] == "":
					continue

				val=float(cols[colnum])
		
				all_years.append(val)

	return all_years


def read_award(filename, colname, cat, top50, statify_by_genre=False):

	awards=[]

	with open(filename) as file:
		
		header=file.readline().split("\t")
		colnum=header.index(colname)

		for line in file:
			cols=line.rstrip().split("\t")
			if cols[6] == "Y":
				year=cols[0]

				if cols[colnum] == "" or cols[colnum] == "None":
					continue

				if cols[colnum] != "NA":
					val=float(cols[colnum])

					awards.append(val)


	pval=permutation_test((awards, top50), statistic=statistic, n_resamples=100000, alternative="two-sided", random_state=0).pvalue
	plab=""

	# bonferroni correction

	corr=7
	if pval < 0.0001/corr:
		plab="***"
	elif pval < 0.001/corr:
		plab="**"
	elif pval < 0.01/corr:
		plab="*"

	print("%s&%.3f&%.3f&%s\\\\ " % (cat, np.mean(awards), np.mean(top50), plab))

if __name__ == "__main__":

	cols={"\% Black": "black", "\% East Asian": "east_asian", "\% Hispanic/Latino": "hispanic_latino", "\% South Asian": "south_asian", "\% White":"white", "\% Men": "men", "\% Women":"women"}

	top50File="../data/top50.tsv"
	awardFile="../data/awards.tsv"

	for val in cols:

		top50=read_top50(top50File, cols[val])
		read_award(awardFile, cols[val], val, top50)


