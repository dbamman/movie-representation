import sys
from collections import Counter
import numpy as np

meta={}

def read_meta(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			imdb=cols[1]
			meta[idd]=imdb

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
				tracks[fno]={}

			tracks[fno][trackno]=faceno, x1,y1,x2,y2

			if trackno not in tracks2fno:
				tracks2fno[trackno]=[]
			tracks2fno[trackno].append(fno)
	return tracks, tracks2fno

def read_fps(filename):

	with open(filename) as file:
		cols=file.readline().split("\t")

		frames=int(cols[1])
		fps=float(cols[4])
		return frames, fps


def proc_all(dataFolder):

	for mov_id in meta:

		trackFile="%s/%s/%s.tracks.txt" % (dataFolder, mov_id, mov_id)
		recogFile="%s/%s/%s.recog.txt" % (dataFolder, mov_id, mov_id)
		fpsFile="%s/%s/%s.fps.txt" % (dataFolder,mov_id,mov_id)

		recog=read_recog(recogFile)
		tracks, tracks2fno=get_tracks(trackFile)
		total_frames, fps=read_fps(fpsFile)

		counts=Counter()

		for trackno in recog:
			actor, score=recog[trackno]
			if score >= 0.18:

				counts[actor]+=len(tracks2fno[trackno])

		imdb=meta[mov_id]

		total_faces=sum(counts.values())
		max_actor_screentime=counts.most_common()[0][1]/total_faces

		for idx, (actor,val) in enumerate(counts.most_common()):
			mins=val/fps/60
			# proportion of all faces in a movie that are this actor's
			
			face_ratio=val/total_faces

			face_ratio_compared_to_max_actor=face_ratio/max_actor_screentime
			print("%s\t%s\t%s\t%s\t%.3f\t%.3f\t%.3f" % (mov_id, imdb, idx, actor, mins, face_ratio, face_ratio_compared_to_max_actor))

			sys.stdout.flush()

read_meta(sys.argv[1])		
proc_all(sys.argv[2])