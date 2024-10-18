import sys
import random
import numpy as np
random.seed(1)

def bootstrap(data, B=1000):
	vals=[]
	for b in range(B):
		choice=random.choices(data, k=len(data))
		val=np.mean(choice)
		vals.append(val)
	return np.percentile(vals, [2.5, 50, 97.5])


def proc(filename, val):

	data={}
	with open(filename) as file:
		head=file.readline().split("\t")
		column_number=head.index(val)
		for line in file:
			cols=line.rstrip().split("\t")

			year=int(cols[0])

			rate=cols[column_number]

			if rate == "None" or rate == "":
				continue

			rate=float(rate)


			if year not in data:
				data[year]=[]
			data[year].append(rate)


	for year in range(1980,2023):
		# print(data[year])
		lower, mid, upper=bootstrap(data[year])
		print("%s\t%s\t%.3f\t%.3f\t%.3f" % (val, year, mid, lower, upper))


for val in ["black", "east_asian", "hispanic_latino", "south_asian", "white", "men", "women"]:
	proc(sys.argv[1], val)

