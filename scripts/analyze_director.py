import sys
import numpy as np
import random

random.seed(1)

def bootstrap(data, B=1000):
	vals=[]
	for b in range(B):
		choice=random.choices(data, k=len(data))
		val=np.mean(choice)
		vals.append(val)
	return np.percentile(vals, [2.5, 50, 97.5])


def proc(filename):

	dir_men=[]
	dir_women=[]

	seen={}

	with open(filename) as file:
		header=file.readline().split("\t")
		men_idx=header.index("men")
		women_idx=header.index("women")
		director_idx=header.index("director gender")
		
		for line in file:
			cols=line.rstrip().split("\t")
			inn=cols[6]
			idd=cols[4]

			if idd in seen:
				continue

			seen[idd]=1

			if inn != "Y":
				continue

			# print(cols)
			
			men=float(cols[men_idx])
			women=float(cols[women_idx])

			director_gender=cols[director_idx].split(";")

			uniq_dirs_gends={}
			for gend in director_gender:
				uniq_dirs_gends[gend]=1

			for gend in uniq_dirs_gends:
				if gend == "male" or gend == "trans male":
					dir_men.append(women)
				if gend == "female" or gend == "trans female":
					dir_women.append(women)


	m_lower, m_mid, m_upper=bootstrap(dir_men)
	w_lower, w_mid, w_upper=bootstrap(dir_women)

	print("%s\t%.3f\t%.3f\t%.3f\t%s" % ("men", m_mid, m_lower, m_upper, len(dir_men)))
	print("%s\t%.3f\t%.3f\t%.3f\t%s" % ("women", w_mid, w_lower, w_upper, len(dir_women)))


proc(sys.argv[1])				