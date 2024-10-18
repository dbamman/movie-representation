import os
import cv2
import numpy as np
import sys
from facetracker import FaceTracker
from insightface.app.common import Face
import insightface
from insightface.app import FaceAnalysis

app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

def read_shots(shotFile):

	boundaries={}
	with open(shotFile) as file:
		for line in file:
			cols=line.rstrip().split(" ")
			start=int(cols[0])
			end=int(cols[1])
			boundaries[start]=1

	return boundaries

def read_faces(filename):
	frames={}
	maxFrame=0
	with open(filename) as file:

		for line in file:
			cols=line.rstrip().split("\t")
			fno=int(cols[0])
			if fno > maxFrame:
				maxFrame=fno

			if fno not in frames:
				frames[fno]=[]

			face=np.array(cols[2].split(" "), dtype=float)

			x1=float(face[0])
			y1=float(face[1])
			x2=x1+float(face[2])
			y2=y1+float(face[3])
			conf=float(face[-1])

			landmarks=face[4:-1]
			
			bbox={"x1": x1, "x2":x2, "y1": y1, "y2": y2, "w": float(face[2]), "h": float(face[3]), "confidence":conf, "landmarks": landmarks, "frame":fno, "left_eye_x":float(landmarks[0]), "right_eye_x":float(landmarks[2])}
			frames[fno].append(bbox)
			

	all_frames=[]
	for fno in range(maxFrame):
		if fno in frames:
			all_frames.append(frames[fno])
		else:
			all_frames.append([])

	return all_frames



def get_reps(movieFile, best_frames, outfile, faces, tracks, trackFile):


	rev_tracks={}
	for key in tracks:
		if tracks[key] not in rev_tracks:
			rev_tracks[tracks[key]]=[]
		rev_tracks[tracks[key]].append(key)


	with open(trackFile, "w") as out:
		for track_no in rev_tracks:
			if track_no is not None:
				for frame_no, face_no in rev_tracks[track_no]:
					face=faces[frame_no][face_no]
					out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (track_no, frame_no, face_no, int(face["x1"]), int(face["y1"]), int(face["x2"]), int(face["y2"])))


	with open(outfile, "w") as out:
		cap = cv2.VideoCapture(movieFile)

		reps={}
		for frame_no in sorted(best_frames.keys()):

			cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no-1)
			res, frame = cap.read()

			x1=y1=w=h=0
			for face_no in best_frames[frame_no]:
				try:
					face=faces[frame_no][face_no]

					det_score = face["confidence"]
					kps=face["landmarks"]

					x1=int(face["x1"])
					y1=int(face["y1"])
					w=int(face["w"])
					h=int(face["h"])

					img_region=[x1, y1, w, h]
					face = Face(bbox=img_region, kps=kps.reshape((5,2)), det_score=det_score)

					track=tracks[(frame_no, face_no)]

					for taskname, model in app.models.items():
						if taskname=='recognition':
							model.get(frame, face)

					out.write("%s\t%s\t%s\t%s\n" % (track, frame_no, face_no, ' '.join([str(x) for x in face["embedding"]])))
			
				except Exception as e:
					print("problem with", face_no, frame_no, movieFile, x1,y1,w,h)
					print(e)
					
		cap.release()



shotFile=sys.argv[1]
faceFile=sys.argv[2]
movieFile=sys.argv[3]
outFile=sys.argv[4]
trackFile=sys.argv[5]


# get shot boundaries
boundaries=read_shots(shotFile)	

# get pre-detected faces
faces=read_faces(faceFile)

# get face tracks
tracker=FaceTracker(minIOU=0.3, min_track_length=2, min_track_conf=0.5, num_best=1)
tracks=tracker.get_tracks(faces, boundaries)
track_best_reps, best_frames=tracker.get_best_frames(tracks, faces)

get_reps(movieFile, best_frames, outFile, faces, tracks, trackFile)

