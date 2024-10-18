import sys, os
from math import log2
import numpy as np
from collections import Counter
import random
random.seed(1)

vals={}
minScore=0.18

demo={}

mapper={}
mapper["Black (b)"]="black"
mapper["East Asian (e)"]="east_asian"
mapper["Hispanic/Latino (h)"]="hispanic_latino"
mapper["None of the above (n)"]="other"
mapper["South Asian/Indian (s)"]="south_asian"
mapper["White (w)"]="white"

eths=["black", "east_asian", "hispanic_latino", "south_asian", "white", "other"]


def read_demo(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			if cols[13] != "NA":

				demo[idd]={}
				for val in eths:
					demo[idd][val]=0
				for col in cols[1:11]:
					for val in col.split("#"):
						if val.rstrip() != "This is not a real person - e.g., cartoon character or animal (c)":
							demo[idd][mapper[val]]+=1

				max_v=0
				max_n=None
				for eth in demo[idd]:
					if demo[idd][eth] > max_v:
						max_v=demo[idd][eth]

				# if two eths have the max, sample one at random
				maxes_n=[]

				for eth in demo[idd]:
					if demo[idd][eth] == max_v:
						maxes_n.append(eth)

				max_n=random.sample(maxes_n, 1)[0]

				demo[idd]={}
				for val in eths:
					demo[idd][val]=0

				demo[idd][max_n]=1
	

def read_meta(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			vals[idd]=1			


def read_fps(filename):

	with open(filename) as file:
		cols=file.readline().split("\t")

		frames=int(cols[1])
		fps=float(cols[4])
		return frames, fps



def read_recog(filename):
	recog={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=cols[0]

			actor, score=cols[3].split(" ")[0].split(":")
			recog[trackno]=actor, float(score)

	return recog


def get_tracks(filename):
	tracks={}
	tracks2fno={}
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

			if trackno not in tracks2fno:
				tracks2fno[trackno]=[]
			tracks2fno[trackno].append(fno)
	return tracks, tracks2fno

def get_entropy(vals):
	total=sum(vals.values())
	h=0

	for key in vals:
		p=vals[key]/total

		if p > 0:
			h-=p * log2(p)

	return h

def proc(dataFolder):

	for mov_id in vals:

		actors={}
		eth_counts={}
		for eth in eths:
			eth_counts[eth]={}

		trackFile="%s/%s/%s.tracks.txt" % (dataFolder, mov_id, mov_id)
		recogFile="%s/%s/%s.recog.txt" % (dataFolder, mov_id, mov_id)
		fpsFile="%s/%s/%s.fps.txt" % (dataFolder, mov_id, mov_id)

		recog=read_recog(recogFile)
		tracks, tracks2fno=get_tracks(trackFile)
		total_frames, fps=read_fps(fpsFile)

		face_frames={}

		total_num_addressable_faces_in_frames=0

		for trackno in recog:
			for fno in tracks2fno[trackno]:
				face_frames[fno]=1


		eth_face_track_counts=Counter()

		fno2eth={}
		fno2n=Counter()

		for trackno in recog:

			actor, score=recog[trackno]

			if score > minScore:
				if actor in demo:

					for fno in tracks2fno[trackno]:
						if fno not in fno2eth:
							fno2eth[fno]={}
							for eth in eths:
								fno2eth[fno][eth]=0

						for eth in demo[actor]:
							fno2eth[fno][eth]+=demo[actor][eth]

						fno2n[fno]+=1

		avg_H=[]
		for fno in fno2eth:
			# only calculate entropy over frames where at least two actors with known race/ethnicity are present
			if fno2n[fno] > 1:
				entropy=get_entropy(fno2eth[fno])
				avg_H.append(entropy)

		print("entropy\t%s\t%.3f" % (mov_id, np.mean(avg_H)))
		sys.stdout.flush()




read_meta(sys.argv[1])
read_demo(sys.argv[2])

proc(sys.argv[3])

