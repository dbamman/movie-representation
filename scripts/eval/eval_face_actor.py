import sys, glob, re, os
from ap_evaluator import APEvaluator
import xml.etree.ElementTree as ET
import cv2

splitFile=sys.argv[1]
splits=sys.argv[2].split(",")
dataFolder=sys.argv[3]

goldFolder="%s/gold" % dataFolder


def get_ids(splitFile, split):
	valid_movies={}
	with open(splitFile) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			if cols[1] in split:
				valid_movies[cols[0]]=1

	return valid_movies

def read_recog(filename):
	recog={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=cols[0]
			actor=cols[3]
			score=cols[4]
			recog[trackno]=actor, score

	return recog

def read_voc_xml(filename):

	if not os.path.exists(filename):
		return []


	with open(filename) as file:
		data=file.read()

		# empty file (no faces present)
		if len(data) == 0:
			return []

	tree = ET.parse(filename) 
	root = tree.getroot() 
	bboxes = []
	height = int(root.find("size")[0].text)
	width = int(root.find("size")[1].text)
	channels = int(root.find("size")[2].text)

	for member in root.findall('object'):
		class_name = member[0].text # class name
		class_name=class_name.split(" ")[0]
		class_name=re.sub("-+", "", class_name)
		# bbox coordinates
		xmin = int(member[4][0].text)
		ymin = int(member[4][1].text)
		xmax = int(member[4][2].text)
		ymax = int(member[4][3].text)
		bbox={}
		bbox["x1"]=xmin
		bbox["x2"]=xmax
		bbox["y1"]=ymin
		bbox["y2"]=ymax
		bbox["class"]=class_name
		bbox["centroid"]=(xmin+xmax)/2, (ymin+ymax)/2
		
		bboxes.append(bbox)

	return bboxes

def get_tracks(filename):
	tracks={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=cols[0]
			fno=cols[1]
			faceno=cols[2]
			x1=max(0,int(cols[3]))
			y1=max(0,int(cols[4]))
			x2=int(cols[5])
			y2=int(cols[6])

			if fno not in tracks:
				tracks[fno]=[]
			tracks[fno].append((trackno, faceno, x1,y1,x2,y2))
	return tracks

def get_faces(filename):

	data={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			frameno=cols[0]
			faceno=cols[1]
			conf=float(cols[2].split(" ")[-1])
			data[frameno,faceno]=conf

	return data

def proc(goldFolder, valid):

	ap_eval=APEvaluator()
	
	for mov_id in valid:

		faceFile="%s/faces/%s.faces_detected.txt" % (dataFolder, mov_id)
		trackFile="%s/tracks/%s.tracks.txt" % (dataFolder, mov_id)
		recogFile="%s/recog/%s.recog.txt" % (dataFolder, mov_id)

		recog=read_recog(recogFile)
		tracks=get_tracks(trackFile)
		faces=get_faces(faceFile)

		eval_boxes=[]

		for xml_path in glob.glob("%s/%s/*xml" % (goldFolder, mov_id)):
			pname=re.sub("\.xml$", "", xml_path)
			parts=pname.split("/")[-1].split("_")
			fno=parts[-1]

			bboxes_pred=[]
			if fno in tracks:

				for trackno, faceno, x1,y1,x2,y2 in tracks[fno]:

					actor, score=recog[trackno]
					conf=faces[fno,faceno]
					bbox_pred={"x1": x1, "x2":x2, "y1": y1, "y2": y2, "confidence":conf, "class":actor, "recog_score":score}
					bboxes_pred.append(bbox_pred)

			bboxes_gold=read_voc_xml(xml_path)

			for bbox_gold in bboxes_gold:
				conf=1
				eval_boxes.append((xml_path, bbox_gold["x1"], bbox_gold["y1"], bbox_gold["x2"], bbox_gold["y2"], conf, "GOLD"))
				print ("ABS\tGOLD\t%s\t%s\t%s\t%s\t%s\t%s\t0\t%s\t1\t%s" % (xml_path, 0, bbox_gold["x1"], bbox_gold["y1"], bbox_gold["x2"], bbox_gold["y2"], bbox_gold["class"], mov_id))

			for bbox_pred in bboxes_pred:
				eval_boxes.append((xml_path, bbox_pred["x1"], bbox_pred["y1"], bbox_pred["x2"], bbox_pred["y2"], bbox_pred["confidence"], "PRED"))
				print ("ABS\tPRED\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (xml_path, 0, bbox_pred["x1"], bbox_pred["y1"], bbox_pred["x2"], bbox_pred["y2"], bbox_pred["confidence"], bbox_pred["class"], bbox_pred["recog_score"], mov_id))

		ap_eval.add_mov(eval_boxes, mov_id)

	ap_eval.evaluate_all()



valid_movies=get_ids(splitFile, splits)
proc(goldFolder, valid_movies)

