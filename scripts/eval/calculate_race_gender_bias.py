import sys, re, json
from collections import Counter
import random
import numpy as np

random.seed(1)

mapper={}
mapper["Black (b)"]="black"
mapper["East Asian (e)"]="east_asian"
mapper["Hispanic/Latino (h)"]="latino"
mapper["None of the above (n)"]="other"
mapper["South Asian/Indian (s)"]="south_asian"
mapper["White (w)"]="white"

genders={}
unique_genders={}

movie_years={}

def read_movie_years(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			year=int(cols[3])
			movie_years[idd]=year


def get_gender_for_year(gender_json, year):
	ordered_years=sorted(list(gender_json.keys()))
	if len(ordered_years) == 1:
		return gender_json[ordered_years[0]].split("#")

	for idx, thisyear in enumerate(ordered_years):

		# if we've reach the last value, return that
		if idx == len(ordered_years)-1:
			return gender_json[thisyear].split("#")

		# otherwise check if the target year is between the current year and the next one in the list
		nextyear=ordered_years[idx+1]
		if year >= thisyear and year < nextyear:
			return gender_json[thisyear].split("#")


def str2int(x):
	return {int(k):v for k,v in x.items()}
	
def read_gender(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			gender_json=json.loads(cols[2], object_hook=str2int)
			genders[idd]=gender_json
			for k in gender_json:
				unique_genders[gender_json[k]]=1


cats=["black", "white", "latino", "east_asian", "south_asian", "other"]
targets=["black", "east_asian", "latino", "south_asian", "white", "male", "female"]

ethnicity={}

def read_race(filename):

	with open(filename) as file:
		file.readline()
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]

			ethnicity[idd]={}
			for cat in cats:
				ethnicity[idd][cat]=0

			if cols[13] == "NA":
				continue

			for val in cols[1:11]:
				for e in val.split("#"):
					if e.lstrip().rstrip() != "This is not a real person - e.g., cartoon character or animal (c)":
						ethnicity[idd][mapper[e]]+=1./10


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

			# else:
				# print("MISSING", p_idx in p_taken, g_idx in g_taken, p_idx, g_idx)

	# print()
	return matches, g_taken


c=0.18


def read_data(filename):

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
					if recog_score > c:
						frames_by_mov[movie_idd][img]["pred"].append({"x1":x1, "y1":y1, "x2":x2, "y2":y2, "conf":conf, "actor":actor, "recog":recog_score})
				elif cat == "GOLD":
					if actor.lower().startswith("nm"):
						frames_by_mov[movie_idd][img]["gold"].append({"x1":x1, "y1":y1, "x2":x2, "y2":y2, "conf":conf, "actor":actor, "recog":recog_score})

	return frames_by_mov

def calc(frames_by_mov, frame_list, train_mults=None):

	frame_movs={}
	for movie_idd in frames_by_mov:
		for img in frames_by_mov[movie_idd]:
			frame_movs[img]=movie_idd


	# RACE/ETHNICITY

	assignable_prec=0
	assignable_rec=0
	assignable_cor=0
	
	precs={}
	recs={}
	cor={}

	for cat in cats:
		precs[cat]=0
		recs[cat]=0
		cor[cat]=0

	all_mults={}

	for img in frame_list:
		movie_idd=frame_movs[img]

		for pred in frames_by_mov[movie_idd][img]["pred"]:
			if pred["actor"] in ethnicity:
				assignable_prec+=1
		for gold in frames_by_mov[movie_idd][img]["gold"]:
			if gold["actor"] in ethnicity:
				assignable_rec+=1

		matches, g_taken=matcher(frames_by_mov[movie_idd][img]["pred"], frames_by_mov[movie_idd][img]["gold"])
		p_seen={}
		g_seen={}

		# assuming a match for the face box so we can evaluate correctness of the ID
		for p_idx in matches:
			g_idx=matches[p_idx]
			pred=frames_by_mov[movie_idd][img]["pred"][p_idx]
			gold=frames_by_mov[movie_idd][img]["gold"][g_idx]

			gold_tt=gold["actor"]
			pred_tt=pred["actor"]

			# if both gold and pred are assignable (i.e., in ethnicity), then it's correct

			if gold_tt not in ethnicity or pred_tt not in ethnicity:
				continue

			p_seen[p_idx]=1
			g_seen[g_idx]=1					

			assignable_cor+=1

			if gold_tt in ethnicity:
				for eth in ethnicity[gold_tt]:
					recs[eth]+=ethnicity[gold_tt][eth]

			if pred_tt in ethnicity:
				for eth in ethnicity[pred_tt]:
					precs[eth]+=ethnicity[pred_tt][eth]

					if gold_tt in ethnicity:
						if eth in ethnicity[gold_tt]:
							cor[eth]+=min(ethnicity[gold_tt][eth],ethnicity[pred_tt][eth])

		for idx, pred in enumerate(frames_by_mov[movie_idd][img]["pred"]):
			if idx not in p_seen:

				pred_tt=pred["actor"]
				if pred_tt in ethnicity:
					for eth in ethnicity[pred_tt]:
						precs[eth]+=ethnicity[pred_tt][eth]

		for idx, gold in enumerate(frames_by_mov[movie_idd][img]["gold"]):
			if idx not in g_seen:

				gold_tt=gold["actor"]
				if gold_tt in ethnicity:
					for eth in ethnicity[gold_tt]:
						recs[eth]+=ethnicity[gold_tt][eth]

	if assignable_rec > 0 or assignable_prec > 0:
		prec=rec=F=0
		if assignable_prec > 0:
			prec=assignable_cor/assignable_prec
		if assignable_rec > 0:
			rec=assignable_cor/assignable_rec

		if prec + rec > 0:
			F=(2*prec*rec)/(prec+rec)

		assign_mult=0
		if rec > 0:
			assign_mult=prec/rec


	for cat in cats:
		if recs[cat] > 0 or precs[cat] > 0:
			prec=rec=F=0
			if precs[cat] > 0:
				prec=cor[cat]/precs[cat]
			if recs[cat] > 0:
				rec=cor[cat]/recs[cat]

			if prec + rec > 0:
				F=(2*prec*rec)/(prec+rec)

			mult=0
			if rec > 0:
				mult=prec/rec

			
			gold_rate=recs[cat]/assignable_rec
			pred_rate=precs[cat]/assignable_prec
			
			pred_mult_rate=0
			if train_mults is not None and cat in train_mults:
				pred_mult_rate=pred_rate*train_mults[cat]

			mult_assign_mult=mult/assign_mult
			all_mults[cat]=mult_assign_mult, F, prec, rec, precs[cat], recs[cat], gold_rate, pred_rate, pred_mult_rate
	


	## GENDER

	assignable_prec=0
	assignable_rec=0
	assignable_cor=0
	
	precs={}
	recs={}
	cor={}

	for cat in unique_genders:
		precs[cat]=0
		recs[cat]=0
		cor[cat]=0

	for img in frame_list:
		movie_idd=frame_movs[img]

		movie_year=movie_years[movie_idd]


		for pred in frames_by_mov[movie_idd][img]["pred"]:
			if pred["actor"] in genders:
				assignable_prec+=1
		for pred in frames_by_mov[movie_idd][img]["gold"]:
			if pred["actor"] in genders:
				assignable_rec+=1

		matches, g_taken=matcher(frames_by_mov[movie_idd][img]["pred"], frames_by_mov[movie_idd][img]["gold"])
		p_seen={}
		g_seen={}

		# assuming a match for the face box so we can evaluate correctness of the ID
		for p_idx in matches:
			g_idx=matches[p_idx]
			pred=frames_by_mov[movie_idd][img]["pred"][p_idx]
			gold=frames_by_mov[movie_idd][img]["gold"][g_idx]

			gold_tt=gold["actor"]
			pred_tt=pred["actor"]

			if gold_tt not in genders or pred_tt not in genders:
				continue

			p_seen[p_idx]=1
			g_seen[g_idx]=1

			assignable_cor+=1
		
			if gold_tt in genders:
				for gender in get_gender_for_year(genders[gold_tt], movie_year):
					recs[gender]+=1

			if pred_tt in genders:
				for gender in get_gender_for_year(genders[pred_tt], movie_year):
					precs[gender]+=1

					if gold_tt in genders:
						if gender in get_gender_for_year(genders[gold_tt], movie_year):
							cor[gender]+=1

		for idx, pred in enumerate(frames_by_mov[movie_idd][img]["pred"]):
			if idx not in p_seen:
				pred_tt=pred["actor"]
				if pred_tt in genders:
					for gender in get_gender_for_year(genders[pred_tt], movie_year):
						precs[gender]+=1

		for idx, gold in enumerate(frames_by_mov[movie_idd][img]["gold"]):
			if idx not in g_seen:
				gold_tt=gold["actor"]
				if gold_tt in genders:
					for gender in get_gender_for_year(genders[gold_tt], movie_year):
						recs[gender]+=1

	if assignable_rec > 0 or assignable_prec > 0:
		prec=rec=F=0
		if assignable_prec > 0:
			prec=assignable_cor/assignable_prec
		if assignable_rec > 0:
			rec=assignable_cor/assignable_rec

		if prec + rec > 0:
			F=(2*prec*rec)/(prec+rec)

		assign_mult=0
		if rec > 0:
			assign_mult=prec/rec

	for cat in recs:
		if recs[cat] > 0 or precs[cat] > 0:
			prec=rec=F=0
			if precs[cat] > 0:
				prec=cor[cat]/precs[cat]
			if recs[cat] > 0:
				rec=cor[cat]/recs[cat]

			if prec + rec > 0:
				F=(2*prec*rec)/(prec+rec)

			mult=0
			if rec > 0:
				mult=prec/rec

			mult_assign_mult=mult/assign_mult

			gold_rate=recs[cat]/assignable_rec
			pred_rate=precs[cat]/assignable_prec

			pred_mult_rate=0
			if train_mults is not None and cat in train_mults:
				pred_mult_rate=pred_rate*train_mults[cat]

			all_mults[cat]=mult_assign_mult, F, prec, rec, precs[cat], recs[cat], gold_rate, pred_rate, pred_mult_rate

	return all_mults


def proc(filename, train_mults=None, doTrain=False):
	frames_by_mov=read_data(filename)

	frame_list=[]
	for mov_id in frames_by_mov:
		for fno in frames_by_mov[mov_id]:
			frame_list.append(fno)

	# bootstrap
	big_mults={}
	for i in range(1000):
		choices=random.choices(frame_list, k=len(frame_list))

		allmults=calc(frames_by_mov, choices, train_mults=train_mults)
		for cat in allmults:
			if cat not in big_mults:
				big_mults[cat]=[]
			big_mults[cat].append(allmults[cat])


	labs=["mult", "F", "P", "R", "true_n", "pred_n", "gold_rate", "pred_rate", "pred_mult_rate"]

	outputs={}
	rev_mapper={"black": "Black", "latino":"Hispanic/Latino", "south_asian": "South Asian", "east_asian":"East Asian", "white": "White", "male": "Men", "female": "Women"}

	if doTrain:

		for cat in targets:
			outputs[cat]={}
			for i in [0,1,2,3,6,7,8]:
				newvals=[]
				for val in big_mults[cat]:
					newvals.append(val[i])
				percs=np.percentile(newvals, [2.5, 50, 97.5])	
				outputs[cat][labs[i]]=percs
			print("BOOT %s\tGold_rate: %.3f [%.3f-%.3f], Pred_mult_rate: %.3f [%.3f-%.3f], Pred_rate: %.3f [%.3f-%.3f], Mult: %.3f [%.3f-%.3f]" % (rev_mapper[cat], outputs[cat]["gold_rate"][1], outputs[cat]["gold_rate"][0], outputs[cat]["gold_rate"][2], outputs[cat]["pred_mult_rate"][1], outputs[cat]["pred_mult_rate"][0], outputs[cat]["pred_mult_rate"][2], outputs[cat]["pred_rate"][1], outputs[cat]["pred_rate"][0], outputs[cat]["pred_rate"][2], outputs[cat]["mult"][1], outputs[cat]["mult"][0], outputs[cat]["mult"][2]  ))

	else:
		for cat in targets:
			outputs[cat]={}
			for i in [0,1,2,3,6,7,8]:
				newvals=[]
				for val in big_mults[cat]:
					newvals.append(val[i])
				percs=np.percentile(newvals, [2.5, 50, 97.5])	
				outputs[cat][labs[i]]=percs
			
			print("%s&%.3f {\\small[%.3f-%.3f]}&%.3f {\\small[%.3f-%.3f]}&%.3f {\\small[%.3f-%.3f]}\\\\" % (rev_mapper[cat], outputs[cat]["F"][1], outputs[cat]["F"][0], outputs[cat]["F"][2], outputs[cat]["P"][1], outputs[cat]["P"][0], outputs[cat]["P"][2], outputs[cat]["R"][1], outputs[cat]["R"][0], outputs[cat]["R"][2] ))

		print()

		for cat in targets:
			outputs[cat]={}
			for i in [0,1,2,3,6,7,8]:
				newvals=[]
				for val in big_mults[cat]:
					newvals.append(val[i])
				percs=np.percentile(newvals, [2.5, 50, 97.5])	
				outputs[cat][labs[i]]=percs

			print("%s&%.3f {\\small [%.3f-%.3f]}&%.3f {\\small [%.3f-%.3f]}&%.3f &%.3f {\\small [%.3f-%.3f]}\\\\" % (rev_mapper[cat], outputs[cat]["pred_rate"][1], outputs[cat]["pred_rate"][0], outputs[cat]["pred_rate"][2], outputs[cat]["pred_mult_rate"][1], outputs[cat]["pred_mult_rate"][0], outputs[cat]["pred_mult_rate"][2], outputs[cat]["gold_rate"][1], train_mults[cat], train_mults["%s_lower" % cat], train_mults["%s_upper" % cat]))
			



	return outputs


if __name__ == "__main__":

	read_movie_years(sys.argv[5])
	read_race(sys.argv[1])
	read_gender(sys.argv[2])

	trainData=sys.argv[3]
	testData=sys.argv[4]

	multipliers=proc(trainData, doTrain=True)
	train_mults={}
	for cat in multipliers:
		train_mults[cat]=multipliers[cat]["mult"][1]
		train_mults["%s_%s" % (cat,"lower")]=multipliers[cat]["mult"][0]
		train_mults["%s_%s" % (cat,"upper")]=multipliers[cat]["mult"][2]

	proc(testData, train_mults=train_mults, doTrain=False)






