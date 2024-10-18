import sys
import numpy as np
from skmisc import loess
import random
random.seed(1)

from random import shuffle

def read_data(filename, target_col):

	data={}

	with open(filename) as file:
		header=file.readline().split("\t")
		target_idx=header.index(target_col)
	
		for line in file:
			cols=line.rstrip().split("\t")
			year=int(cols[0])
			incol=cols[6]

			if incol != "Y" or cols[target_idx] == "None" or cols[target_idx] == "NA":
				continue

			val=float(cols[target_idx])
			if year not in data:
				data[year]=[]

			data[year].append(val)

	return data


def proc(data):
	B=10000

	all_preds=[]

	for b in range(B):
		sys.stderr.write("%s\n" % b)
		x=[]
		y=[]
		newdata=[]
			
		for year in data:
			choice=random.choices(data[year], k=len(data[year]))
			for val in choice:
				x.append(year)
				y.append(val)
				newdata.append((year, val))
		shuffle(newdata)
		for xv, yv in newdata:
			x.append(xv)
			y.append(yv)

		x=np.array(x, dtype=float)
		y=np.array(y, dtype=float)

		x_pred = np.arange(1980, 2022.1, .1, dtype=float)

		loess_fit = loess.loess(x, y)
		loess_fit.fit();
		y_pred = loess_fit.predict(x_pred).values

		all_preds.append(y_pred)

	all_preds=np.array(all_preds)

	percs=np.percentile(all_preds, [2.5, 50, 97.5], axis=0)
	perclist=percs.tolist()
	for idx, val in enumerate(np.arange(1980, 2022.1, .1)):
		print("%.1f\t%.5f\t%.10f\t%.5f" % (val, perclist[0][idx], perclist[1][idx], perclist[2][idx]))

data=read_data(sys.argv[1], sys.argv[2])
proc(data)