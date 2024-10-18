import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import random
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

random.seed(1)


facetimes={}

def read_facetime(filename):

	mov_lead_facetime={}

	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			imdb_tt=cols[3]		
			mins=float(cols[4])
			
			if idd not in mov_lead_facetime or mins > mov_lead_facetime[idd]:
				mov_lead_facetime[idd]=mins

	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			imdb_tt=cols[3]		
			mins=float(cols[4])

			ratio_of_max_screen=mins/mov_lead_facetime[idd]

			facetimes[idd,imdb_tt]=ratio_of_max_screen



def read_gold(filename, outfile):

	runtimes={}

	leads=[]
	nonleads=[]

	data=[]
	with open(outfile, "w") as out:
		with open(filename) as file:
			file.readline()
			for line in file:
				cols=line.rstrip().split("\t")
				imdb_tt=cols[0]
				idd=cols[3]

				if (idd, imdb_tt) in facetimes:

					ratio_of_max_screen=facetimes[idd, imdb_tt]
					lead=cols[9]

					if idd.lstrip().rstrip() == "" or imdb_tt.lstrip().rstrip() == "":
						continue

					if lead == "lead":
						data.append(([ratio_of_max_screen], 1))
						out.write("lead\t%.3f\n" % ratio_of_max_screen)
					elif lead == "non-lead":
						data.append(([ratio_of_max_screen], 0))
						out.write("nonlead\t%.3f\n" % ratio_of_max_screen)

			
			train_X, train_Y, test_X, test_Y=[], [], [], []
			random.shuffle(data)
			n=len(data)
			train_n=int(n*.6)

			for x, y in data[:train_n]:
				train_X.append(x)
				train_Y.append(y)

			for x, y in data[train_n:]:
				test_X.append(x)
				test_Y.append(y)



			model = DecisionTreeClassifier(criterion="entropy", max_depth=2)
			model.fit(train_X, train_Y)
			score=model.score(test_X, test_Y)
			print(score)

			plt.figure(figsize=(20, 10))
			plot_tree(model, feature_names=["ratio_of_max_screen"], class_names=["non-lead", "lead"], filled=True)
			plt.tight_layout()
			plt.savefig("decision_tree.pdf")
			plt.show()

			# golds=[]
			# preds=[]
			# for x, y in zip(test_X, test_Y):
			# 	# if x[0] <= 0.1601850613951683:
			# 	if x[4] <= 0.7479760050773621:
			# 		pred=0
			# 	else:
			# 		pred=1
			# 	preds.append(pred)
			# 	golds.append(y)

			# from sklearn.metrics import accuracy_score
			# print(accuracy_score(preds, golds))

			# from sklearn.tree import _tree

			# def tree_to_code(tree, feature_names):
			#     tree_ = tree.tree_
			#     feature_name = [
			#         feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
			#         for i in tree_.feature
			#     ]
			#     print ("def tree({}):".format(", ".join(feature_names)))

			#     def recurse(node, depth):
			#         indent = "  " * depth
			#         if tree_.feature[node] != _tree.TREE_UNDEFINED:
			#             name = feature_name[node]
			#             threshold = tree_.threshold[node]
			#             print ("{}if {} <= {}:".format(indent, name, threshold))
			#             recurse(tree_.children_left[node], depth + 1)
			#             print ("{}else:  # if {} > {}".format(indent, name, threshold))
			#             recurse(tree_.children_right[node], depth + 1)
			#         else:
			#             print ("{}return {}".format(indent, tree_.value[node]))

			#     recurse(0, 1)
			# tree_to_code(model, ["norm face", "ratio", "rank", "ratio_max", "ratio_of_max_screen"])
			# # print("Leads:\tmean=%.3f sd=%.3f" % (np.mean(leads), np.std(leads)))
			# print("Non-leads:\tmean=%.3f sd=%.3f" % (np.mean(nonleads), np.std(nonleads)))

			# print("Best lead vs. non-lead thresold fit: %.3f" % thres)

read_facetime(sys.argv[2])
read_gold(sys.argv[1], sys.argv[3])				



