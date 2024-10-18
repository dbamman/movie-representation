import sys, re
import numpy as np
from scipy.stats import ttest_rel

rev_mapper={"black": "Black", "hispanic_latino":"Hispanic/Latino", "south_asian": "South Asian", "east_asian":"East Asian", "white": "White", "men": "Men", "women": "Women"}

def proc(filename):

	data={}
	with open(filename) as file:
		header=file.readline().split("\t")
		targets={}
		for val in ["lead black", "lead east_asian", "lead hispanic_latino", "lead south_asian", "lead white", "lead men", "lead women"]:
			idx=header.index(val)
			targets[val]=header.index(val), header.index("non-%s" % val)

			data[val]={"lead":[], "nonlead":[]}

		for line in file:
			cols=line.rstrip().split("\t")
			incol=cols[6]
			if incol == "Y":
				for val in targets:
					lead_idx=targets[val][0]
					nonlead_idx=targets[val][1]

					# print(lead_idx, nonlead_idx)
					
					if cols[lead_idx] != "None" and cols[nonlead_idx] != "None":
						lead=cols[lead_idx]
						nonlead=cols[nonlead_idx]

						lv=float(lead)
						nlv=float(nonlead)


						data[val]["lead"].append(lv)
						data[val]["nonlead"].append(nlv)

	for val in data:

		corr=7
		stat, pval=ttest_rel(data[val]["lead"], data[val]["nonlead"])


		plab=""

		if pval < 0.0001/corr:
			plab="***"
		elif pval < 0.001/corr:
			plab="**"
		elif pval < 0.01/corr:
			plab="*"


		lab=rev_mapper[re.sub("^lead ", "", val)]
		# print("%s\t%.3f\t%.3f\t%.3f\t%s" % (lab, np.mean(data[val]["lead"]), np.mean(data[val]["nonlead"]), stat, pval))
		print("%s&%.3f&%.3f&%s \\\\" % (lab, np.mean(data[val]["lead"]), np.mean(data[val]["nonlead"]), plab))


proc(sys.argv[1])		




