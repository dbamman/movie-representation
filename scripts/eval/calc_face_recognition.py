import sys
from collections import Counter

# https://stackoverflow.com/questions/25349178/calculating-percentage-of-bounding-box-overlap-for-image-detector-evaluation
def get_iou(bb1, bb2):
	"""
	Calculate the Intersection over Union (IoU) of two bounding boxes.

	Parameters
	----------
	bb1 : dict
		Keys: {'x1', 'x2', 'y1', 'y2'}
		The (x1, y1) position is at the top left corner,
		the (x2, y2) position is at the bottom right corner
	bb2 : dict
		Keys: {'x1', 'x2', 'y1', 'y2'}
		The (x, y) position is at the top left corner,
		the (x2, y2) position is at the bottom right corner

	Returns
	-------
	float
		in [0, 1]
	"""


	# print(bb1, bb2)
	assert bb1['x1'] < bb1['x2']
	assert bb1['y1'] < bb1['y2']
	assert bb2['x1'] < bb2['x2']
	assert bb2['y1'] < bb2['y2']

	# determine the coordinates of the intersection rectangle
	x_left = max(bb1['x1'], bb2['x1'])
	y_top = max(bb1['y1'], bb2['y1'])
	x_right = min(bb1['x2'], bb2['x2'])
	y_bottom = min(bb1['y2'], bb2['y2'])

	if x_right < x_left or y_bottom < y_top:
		return 0.0

	# The intersection of two axis-aligned bounding boxes is always an
	# axis-aligned bounding box
	intersection_area = (x_right - x_left) * (y_bottom - y_top)

	# compute the area of both AABBs
	bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
	bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
	assert iou >= 0.0
	assert iou <= 1.0
	return iou


def matcher(preds, golds):

	minIOU=0.5

	scores={}
	for p_idx, pred in enumerate(preds):

		pred_centroid=(pred["x2"]+pred["x1"])/2, (pred["y2"]+pred["y2"])/2

		for g_idx, gold in enumerate(golds):
			gold_centroid=(gold["x2"]+gold["x1"])/2, (gold["y2"]+gold["y2"])/2
			diff=(gold_centroid[0]-pred_centroid[0])*(gold_centroid[0]-pred_centroid[0]) + (gold_centroid[1]-pred_centroid[1])*(gold_centroid[1]-pred_centroid[1])
			scores[p_idx, g_idx]=diff

	p_taken={}
	g_taken={}

	matches={}

	# sort closest to farthest
	for k, v in sorted(scores.items(), key=lambda item: item[1]):
		# print(k,v)
		p_idx, g_idx=k
		if p_idx not in p_taken and g_idx not in g_taken:
			iou=get_iou(preds[p_idx], golds[g_idx])

			if iou > minIOU:
				p_taken[p_idx]=1
				g_taken[g_idx]=1

				matches[p_idx]=g_idx

	# print()
	return matches, g_taken





def proc(filename, doTrain=False, confidence_level=None):

	frames_by_mov={}
	
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")

			if cols[0] == "ABS":
				# print(cols)
				cat=cols[1]
				img=cols[2]
				face_no=cols[3]
				x1=float(cols[4])
				y1=float(cols[5])
				x2=float(cols[6])
				y2=float(cols[7])
				conf=float(cols[8])

				if cat == "PRED":
					actors=cols[9].split(" ")
					best=actors[0].split(":")
					# print(best)
					actor=best[0]
					recog_score=float(best[1])
				elif cat == "GOLD":
					actor=cols[9]
					recog_score=cols[10]

				
				# if cols[10] != "None":
					# recog_score=float(cols[10])

				movie_idd=cols[11]

				if movie_idd not in frames_by_mov:
					frames_by_mov[movie_idd]={}
				if img not in frames_by_mov[movie_idd]:
					frames_by_mov[movie_idd][img]={}
					frames_by_mov[movie_idd][img]["gold"]=[]
					frames_by_mov[movie_idd][img]["pred"]=[]

				if cat == "PRED":
					frames_by_mov[movie_idd][img]["pred"].append({"x1":x1, "y1":y1, "x2":x2, "y2":y2, "conf":conf, "actor":actor, "recog":recog_score})
				elif cat == "GOLD":
					frames_by_mov[movie_idd][img]["gold"].append({"x1":x1, "y1":y1, "x2":x2, "y2":y2, "conf":conf, "actor":actor, "recog":recog_score})


	correct=0
	total_recall=0
	total_precision=0

	total_precisions=Counter()
	corrects=Counter()


	for movie_idd in frames_by_mov:
		for img in frames_by_mov[movie_idd]:
			matches, g_taken=matcher(frames_by_mov[movie_idd][img]["pred"], frames_by_mov[movie_idd][img]["gold"])

			# assuming a match for the face box so we can evaluate correctness of the ID
			for p_idx in matches:
				g_idx=matches[p_idx]
				pred=frames_by_mov[movie_idd][img]["pred"][p_idx]
				gold=frames_by_mov[movie_idd][img]["gold"][g_idx]

				if gold["actor"].lower() != "unknown":
					total_recall+=1

				for val in range(0,100,1):
					c=float(val/100)
					
					if pred["recog"] > c:
						total_precisions[c]+=1

						if pred["actor"]==gold["actor"]:
							corrects[c]+=1

	maxF1=0
	bestPR=0,0
	best=None

	if doTrain:
		for val in range(0,100,1):
			c=float(val/100)

			recall=precision=F1=0
			if total_recall > 0:
				recall=corrects[c]/total_recall
			if total_precisions[c] > 0:
				precision=corrects[c]/total_precisions[c]
			if recall + precision > 0:
				F1=2*recall*precision/(recall+precision)

			# print("%.3f\t%.3f\t%.3f\t%s\t%s\t%.3f" % (F1, recall, precision, total_recall, total_precisions[c], c))
			if F1 > maxF1:
				maxF1=F1
				bestPR=recall,precision
				best=c

		print("Best confidence on training/dev data: %.3f\t%.3f\t%.3f\t%s\t%s\t%s" % (maxF1, bestPR[0], bestPR[1], best, total_recall, sys.argv[1]))

		return best

	else:

		c=confidence_level

		recall=precision=F1=0
		if total_recall > 0:
			recall=corrects[c]/total_recall
		if total_precisions[c] > 0:
			precision=corrects[c]/total_precisions[c]
		if recall + precision > 0:
			F1=2*recall*precision/(recall+precision)

		print("Test data: %.3f\t%.3f\t%.3f\t%s\t%s\t%.3f" % (F1, recall, precision, total_recall, total_precisions[c], c))


trainFile=sys.argv[1]
testFile=sys.argv[2]

best_conf_from_train=proc(trainFile, doTrain=True)
proc(testFile, doTrain=False, confidence_level=best_conf_from_train)




